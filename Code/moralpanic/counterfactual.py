"""The 2x2 counterfactual design and the panic index (spec §10).

Alarm has two manufactured sources, claims-making and othering, and each can be
switched off independently: claims-making by silencing both actors (rho = 0),
othering by setting omega = 0. Every run is therefore executed four times on the
identical seed.

Claims-making is switched off by REACH, never by depth. Setting alpha = 0 would
leave a targeted agent still counting the actor as a maximally alarmed contact
in E_i, so the "null" run would not be null (spec §3.1, §7.4).
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Dict, List, Optional, Sequence

import numpy as np

from .config import RunConfig
from .measures import exposure_concentration
from .model import Model, RunResult, initialise
from .rng import Streams

NULL = "null"
CLAIMS = "claims"
OTHERING = "othering"
FULL = "full"
ARMS = (NULL, CLAIMS, OTHERING, FULL)


def _arm_config(config: RunConfig, arm: str) -> RunConfig:
    """Derive one arm of the 2x2 from the full configuration (spec §10.1)."""
    claims_on = arm in (CLAIMS, FULL)
    othering_on = arm in (OTHERING, FULL)

    actor_d = config.actor_d if claims_on else config.actor_d.silenced()
    actor_c = config.actor_c if claims_on else config.actor_c.silenced()
    parameters = config.parameters if othering_on else config.parameters.without_othering()

    return replace(config, actor_d=actor_d, actor_c=actor_c, parameters=parameters)


@dataclass
class Decomposition:
    """The exact four-way decomposition of aggregate alarm (spec §10.1).

    At every step:

        a_bar = warranted + claims_alone + othering_alone + interaction

    The decomposition is exact but is NOT a partition into non-negative shares:
    any term except `warranted` may be negative, and where that happens it is
    reported rather than suppressed.

    The three manufactured terms are kept separate and never merged. Merging the
    interaction into either side makes H2 unfalsifiable in one direction.
    """

    warranted: np.ndarray
    claims_alone: np.ndarray
    othering_alone: np.ndarray
    interaction: np.ndarray
    panic_index: np.ndarray

    def total(self) -> np.ndarray:
        return self.warranted + self.claims_alone + self.othering_alone + self.interaction

    def check_exact(self, observed: np.ndarray, tol: float = 1e-10) -> None:
        residual = np.max(np.abs(self.total() - observed))
        if residual > tol:
            raise AssertionError(f"decomposition is not exact: residual {residual:.3e}")

    def check_interaction_zero_at_first_step(self, tol: float = 1e-12) -> None:
        """Spec §10.1: the interaction term is identically zero at t = 1.

        All four runs share the state at t = 0, so Phi_i(0), kappa_i(0) and
        g^X_i(0) coincide and the alternating sum vanishes term by term. The
        interaction can first become non-zero at t = 2, and only because
        claims-making has moved positions and thereby changed the distances
        othering reads. This is what guarantees the interaction carries no
        component of the population's initial dispersion.

        Holds only when C1 is satisfied so that no clip binds.
        """
        if self.interaction.size < 2:
            return
        value = abs(float(self.interaction[1]))
        if value > tol:
            raise AssertionError(
                f"interaction at t=1 is {value:.3e}, expected 0 (spec §10.1). "
                "Check that C1 holds and that all four arms share one seed."
            )


@dataclass
class CounterfactualResult:
    """One seed's worth of the 2x2 design, with everything derived from it."""

    seed: int
    runs: Dict[str, RunResult]
    decomposition: Decomposition

    @property
    def full(self) -> RunResult:
        return self.runs[FULL]

    @property
    def structure(self) -> Dict[str, float]:
        return self.full.structure

    # -- derived measures (spec §10.2, §10.3) ------------------------------ #

    def panic_episode(
        self, pi_star: float = 0.5, q_star: float = 0.5, window: int = 10
    ) -> Optional[int]:
        """Onset step of the first panic episode, or None (spec §10.2).

        An episode requires BOTH conditions to hold for `window` consecutive
        steps: disproportion (Pi >= pi_star) and volume (q >= q_star). Requiring
        both separates panic from widespread but proportionate concern, and from
        successful manipulation of a small minority.
        """
        meets = (self.decomposition.panic_index >= pi_star) & (
            self.full.series("amplifying") >= q_star
        )
        return _first_sustained(meets, window)

    def handover_step(
        self, hold: int = 10, t_off: Optional[int] = None, require_active: bool = True
    ) -> Optional[int]:
        """First step at which the interaction exceeds claims-alone (spec §10.3).

        Defined against claims-making alone rather than a merged endogenous
        share, so it measures when entrepreneur-CREATED division outweighs the
        entrepreneur's own signal, and cannot be satisfied by division that
        pre-existed the episode.

        **Evaluated only while the entrepreneur is speaking.** Once it withdraws,
        claims-alone falls to zero and the criterion is met by any positive
        interaction whatever, which is arithmetic rather than a handover: under
        the polarized regime the unguarded version fires at t_off + 1 in every
        seed. `t_off` defaults to the entrepreneur's own `active_until`, so the
        guard needs no extra bookkeeping from the caller; pass
        `require_active=False` to recover the unguarded definition.
        """
        ahead = self.decomposition.interaction > self.decomposition.claims_alone
        if require_active:
            if t_off is None:
                t_off = self.full.config.actor_d.active_until
            if t_off is not None:
                ahead = ahead.copy()
                ahead[int(t_off):] = False
        return _first_sustained(ahead, hold)

    def persistence(self, t_off: int, fraction: float = 0.5) -> Dict[str, object]:
        """Steps after `t_off` until Pi falls below `fraction` of its value there.

        Returned censored rather than assigned the run length: averaging
        censored durations understates persistence (spec §10.3). This measures
        decay only while C stays silent, which is the case in Experiment B.
        """
        pi = self.decomposition.panic_index
        if t_off >= pi.size:
            raise ValueError("t_off falls outside the run")
        target = pi[t_off] * fraction
        after = pi[t_off:]
        below = np.flatnonzero(after < target)
        if below.size == 0:
            return {"duration": after.size, "censored": True}
        return {"duration": int(below[0]), "censored": False}

    def null_peak(self) -> float:
        """max_t of the null run's mean alarm (spec §10.2).

        The panic index divides by 1 - a_bar_null, so this is the conditioning
        of the denominator, recorded per run rather than assumed safe. At the
        operating point it stays below 0.1.
        """
        return float(np.max(self.decomposition.warranted))

    def pre_existing_division(self) -> np.ndarray:
        """The othering-alone curve (spec §10.3).

        Under the consensual default it should stay near zero. Where it does
        not, the handover result for that regime is attenuated rather than a
        clean test.
        """
        return self.decomposition.othering_alone

    def interaction_channels(self) -> Dict[str, np.ndarray]:
        """Contrast that separates the interaction's two channels (spec §10.1).

        One channel is othering over newly created distance; the other is
        reweighting, because a campaign pushes agents past their thresholds and
        through kappa makes the already-divided louder.
        """
        return {
            "othering_full": self.runs[FULL].series("mean_othering"),
            "othering_only": self.runs[OTHERING].series("mean_othering"),
        }

    def exposure_concentration(self) -> float:
        """Var_i( sum_t g^D_i(t) ) in the full run (spec §10.3)."""
        return exposure_concentration(self.full.reach_counts_d)

    def panic_incidence_grid(
        self,
        pi_stars: Sequence[float] = (0.1, 0.2, 0.3, 0.4, 0.5),
        q_stars: Sequence[float] = (0.1, 0.2, 0.3, 0.4, 0.5),
        windows: Sequence[int] = (5, 10, 20),
    ) -> Dict[str, Optional[int]]:
        """Onset step under every cut of the panic criterion (spec §10.2).

        Pi*, q* and W are conventions rather than findings, so the spec asks for
        results over a grid of all three: how much the boundary between calm and
        panic depends on where it is drawn is itself part of the contribution.
        Keys are ``f"{pi_star:.2f}_{q_star:.2f}_{window}"``.
        """
        pi = self.decomposition.panic_index
        q = self.full.series("amplifying")
        grid: Dict[str, Optional[int]] = {}
        for pi_star in pi_stars:
            for q_star in q_stars:
                meets = (pi >= pi_star) & (q >= q_star)
                for window in windows:
                    onset = _first_sustained(meets, window)
                    grid[f"{pi_star:.2f}_{q_star:.2f}_{window}"] = (
                        None if onset is None else int(onset)
                    )
        return grid

    def boundary_diagnostics(self) -> Dict[str, float]:
        """How much of the measured polarization is boundary pile-up (spec §14.2).

        `bimodality` includes the atoms the clip accumulates at +/-1;
        `bimodality_interior` excludes them. A large gap, or a large
        `boundary_fraction`, means the raw coefficient is reading the artifact
        rather than emergent structure, and the run should be replicated under
        `BoundMode.TANH`.
        """
        full = self.full
        return {
            "bimodality": float(full.series("bimodality")[-1]),
            "bimodality_interior": float(full.series("bimodality_interior")[-1]),
            "boundary_fraction": float(full.series("boundary_fraction")[-1]),
            "clip_events": float(full.structure.get("clip_events", 0.0)),
            "clip_rate": float(
                full.structure.get("clip_events", 0.0)
                / max(1, full.n_steps * full.positions_final.size)
            ),
        }


def _first_sustained(flags: np.ndarray, window: int) -> Optional[int]:
    """First index where `flags` is True for `window` consecutive entries."""
    if window <= 0:
        raise ValueError("window must be positive")
    if flags.size < window:
        return None
    run_length = 0
    for index, flag in enumerate(flags):
        run_length = run_length + 1 if flag else 0
        if run_length == window:
            return int(index - window + 1)
    return None


def run_counterfactual_set(config: RunConfig) -> CounterfactualResult:
    """Execute the four arms of the 2x2 on one seed (spec §10.1).

    All four arms are built from the same `Streams`, so they share the network,
    the initial positions, the initial alarm and the thresholds, and they draw
    the same per-step noise. The shared initial state is asserted rather than
    assumed (spec §15).
    """
    config.parameters.require_stable()

    runs: Dict[str, RunResult] = {}
    fingerprint = None

    for arm in ARMS:
        arm_config = _arm_config(config, arm)
        streams = Streams.from_seed(config.seed)
        initial = initialise(arm_config, streams)

        if fingerprint is None:
            fingerprint = initial.fingerprint()
        elif initial.fingerprint() != fingerprint:
            raise AssertionError(
                f"arm '{arm}' does not share the initial state of the other arms; "
                "common random numbers are broken (spec §15)"
            )

        runs[arm] = Model(arm_config, streams, initial).run()

    warranted = runs[NULL].series("mean_alarm")
    claims = runs[CLAIMS].series("mean_alarm")
    othering = runs[OTHERING].series("mean_alarm")
    full = runs[FULL].series("mean_alarm")

    decomposition = Decomposition(
        warranted=warranted,
        claims_alone=claims - warranted,
        othering_alone=othering - warranted,
        interaction=full - claims - othering + warranted,
        panic_index=(full - warranted) / (1.0 - warranted),
    )
    decomposition.check_exact(full)

    return CounterfactualResult(seed=config.seed, runs=runs, decomposition=decomposition)


def counterfactual_validity(
    config: RunConfig, n_replicates: int = 5, ratio: float = 0.10
) -> Dict[str, object]:
    """When do the four arms stop being comparable? (spec §14.2, artifact 2)

    The decomposition of spec §10.1 -- and therefore H2 -- assumes the four runs
    stay comparable, which holds only under common random numbers and only while
    trajectories have not diverged chaotically. The check the spec asks for is
    that the counterfactual runs stay within Monte Carlo error of their own
    replicates, with the step at which they separate beyond that tolerance
    reported, and Pi and the handover time reported only up to that step.

    Operationalised as follows. Each arm is replicated `n_replicates` times with
    the *same* network, initial positions, alarm and thresholds but a different
    position-noise substream, which is exactly the within-arm variability the
    decomposition treats as negligible. At every step:

        noise  = the largest across-replicate s.d. of mean alarm, over the arms
        signal = |a_bar_full - a_bar_null|, the numerator of Pi

    The horizon is the first step at which ``noise > ratio * signal``: past it,
    re-drawing the noise moves a single arm by more than a tenth of the effect
    the four-way comparison is trying to resolve.

    Returns the horizon (None if the criterion is never met within the run),
    together with the two curves, so the reader can see the margin rather than
    take the cut on trust.
    """
    arm_series: Dict[str, np.ndarray] = {}
    for arm in ARMS:
        arm_config = _arm_config(config, arm)
        traces: List[np.ndarray] = []
        for replicate in range(n_replicates):
            streams = Streams.from_seed(config.seed)
            initial = initialise(arm_config, streams)
            # re-draw ONLY the noise stream: same population, different shocks
            perturbed = replace(
                streams,
                noise=np.random.Generator(
                    np.random.PCG64(np.random.SeedSequence([config.seed, 0xBEEF, replicate]))
                ),
            )
            traces.append(Model(arm_config, perturbed, initial).run().series("mean_alarm"))
        arm_series[arm] = np.array(traces)

    noise = np.max([series.std(axis=0, ddof=1) for series in arm_series.values()], axis=0)
    signal = np.abs(arm_series[FULL].mean(axis=0) - arm_series[NULL].mean(axis=0))
    exceeds = noise > ratio * np.maximum(signal, 1e-12)
    horizon = int(np.flatnonzero(exceeds)[0]) if exceeds.any() else None

    return {
        "horizon": horizon,
        "n_replicates": n_replicates,
        "ratio": ratio,
        "noise": noise,
        "signal": signal,
        "max_noise": float(noise.max()),
        "note": (
            "Pi and the handover time are reportable up to `horizon`; "
            "None means the arms never separated beyond the tolerance."
        ),
    }


def is_subcritical(
    config: RunConfig, seed_fraction: float = 0.05, steps: int = 200, tol: float = 0.01
) -> Dict[str, object]:
    """Is this parameter point below the contagion threshold? (spec §3.3, C3)

    Silences both actors, sets omega = 0, seeds a small fraction at full alarm
    and lets contagion run alone. Below the threshold alarm dies; above it,
    alarm self-sustains no matter what any claims-maker does, and H2 becomes
    true for the wrong reason -- persistence would then reflect supercritical
    contagion rather than othering.

    The threshold depends on mean degree as well as on mu, delta and gamma, so
    it is measured rather than asserted from a closed form.
    """
    from .config import Parameters as _P

    probe = replace(
        config,
        n_steps=steps,
        parameters=replace(config.parameters, omega=0.0),
        actor_d=config.actor_d.silenced(),
        actor_c=config.actor_c.silenced(),
    )
    streams = Streams.from_seed(config.seed)
    initial = initialise(probe, streams)
    model = Model(probe, streams, initial)
    model.alarm[:] = 0.0
    model.alarm[: int(seed_fraction * probe.n_agents)] = 1.0
    resting = float(model.run().series("mean_alarm")[-1])
    return {
        "subcritical": resting < tol,
        "resting_mean_alarm": resting,
        "mu_plus_delta": config.parameters.mu + config.parameters.delta,
    }
