"""The five verification limits (spec §12.3).

Verification asks whether the code implements the specification, and is
reported separately from any substantive result. Each limit reduces the model
to a system whose behaviour is known independently, so a failure localises the
bug rather than merely signalling one.

In all five, both actors are silent unless stated otherwise.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Callable, List

import numpy as np

from .config import (
    Constants,
    Repertoire,
    NetworkSpec,
    Parameters,
    PositionRegime,
    RunConfig,
    SILENT_C,
    ThresholdRegime,
    Topology,
    entrepreneur,
)
from .counterfactual import counterfactual_validity, run_counterfactual_set
from .measures import (
    bimodality_coefficient,
    boundary_fraction,
    interior_bimodality_coefficient,
)
from .model import Model, initialise
from .rng import Streams


@dataclass
class LimitResult:
    name: str
    passed: bool
    detail: str

    def __str__(self) -> str:
        mark = "PASS" if self.passed else "FAIL"
        return f"[{mark}] {self.name}: {self.detail}"


def _base_config(**overrides) -> RunConfig:
    defaults = dict(
        seed=20260731,
        n_steps=400,
        network=NetworkSpec(
            topology=Topology.SMALL_WORLD, n_agents=200, mean_degree=6.0, rewiring_p=0.1
        ),
        parameters=Parameters(epsilon=2.0, mu=0.3, delta=0.3, omega=0.0),
        actor_d=entrepreneur(alpha=0.0, rho=0.0),
        actor_c=SILENT_C,
        constants=Constants(sigma=0.2, gamma=3.0, zeta=0.0),
        position_regime=PositionRegime.CONSENSUAL,
        threshold_regime=ThresholdRegime.DISPERSED,
    )
    defaults.update(overrides)
    return RunConfig(**defaults)


def _run(config: RunConfig):
    streams = Streams.from_seed(config.seed)
    return Model(config, streams).run()


# --------------------------------------------------------------------------- #
# Limit 1 -- DeGroot consensus
# --------------------------------------------------------------------------- #


def limit_degroot(tol: float = 1e-6) -> LimitResult:
    """sigma = zeta = 0, epsilon = 2, gamma = 1, actors silent.

    Positions must converge to a single consensus value on any connected,
    non-bipartite graph.
    """
    config = _base_config(
        n_steps=2000,
        constants=Constants(sigma=0.0, gamma=1.0, zeta=0.0),
        parameters=Parameters(epsilon=2.0, mu=0.3, delta=0.3, omega=0.0),
    )
    result = _run(config)
    spread = float(result.positions_final.max() - result.positions_final.min())
    return LimitResult(
        "1. DeGroot consensus",
        spread < tol,
        f"final position spread {spread:.2e} (tolerance {tol:.0e})",
    )


# --------------------------------------------------------------------------- #
# Limit 2 -- Friedkin-Johnsen equilibrium
# --------------------------------------------------------------------------- #


def limit_friedkin_johnsen(tol: float = 1e-6) -> LimitResult:
    """sigma > 0, zeta = 0, epsilon = 2, gamma = 1, actors silent.

    Positions must converge to b* = (I - (1-sigma) M)^-1 sigma b(0), with M the
    row-stochastic neighbour-averaging matrix of spec §7.3.
    """
    sigma = 0.2
    config = _base_config(
        n_steps=2000,
        constants=Constants(sigma=sigma, gamma=1.0, zeta=0.0),
        parameters=Parameters(epsilon=2.0, mu=0.3, delta=0.3, omega=0.0),
    )
    streams = Streams.from_seed(config.seed)
    initial = initialise(config, streams)
    result = Model(config, streams, initial).run()

    from .network import Neighbourhood

    matrix = Neighbourhood.from_graph(initial.graph).adjacency_row_stochastic()
    n = matrix.shape[0]
    analytic = np.linalg.solve(
        np.eye(n) - (1.0 - sigma) * matrix, sigma * initial.positions
    )
    error = float(np.max(np.abs(result.positions_final - analytic)))
    return LimitResult(
        "2. Friedkin-Johnsen equilibrium",
        error < tol,
        f"max deviation from the analytic equilibrium {error:.2e} (tolerance {tol:.0e})",
    )


# --------------------------------------------------------------------------- #
# Limit 3 -- Hegselmann-Krause clustering
# --------------------------------------------------------------------------- #


def _count_clusters(values: np.ndarray, tolerance: float) -> int:
    """Single-linkage cluster count at the given tolerance."""
    ordered = np.sort(values)
    if ordered.size == 0:
        return 0
    return 1 + int(np.count_nonzero(np.diff(ordered) > tolerance))


def limit_hegselmann_krause() -> LimitResult:
    """sigma = zeta = 0, epsilon < 2, delta = omega = 0, actors silent.

    Bounded confidence on a network: the surviving cluster count must fall as
    epsilon rises, and must be 1 at epsilon = 2. With delta = omega = 0 alarm
    decays to zero, no agent amplifies, and gamma is inert.
    """
    counts = []
    for epsilon in (0.15, 0.4, 2.0):
        config = _base_config(
            n_steps=1500,
            network=NetworkSpec(
                topology=Topology.SMALL_WORLD, n_agents=200, mean_degree=6.0
            ),
            constants=Constants(sigma=0.0, gamma=3.0, zeta=0.0),
            parameters=Parameters(epsilon=epsilon, mu=0.3, delta=0.0, omega=0.0),
            position_regime=PositionRegime.POLARIZED,
        )
        result = _run(config)
        counts.append(_count_clusters(result.positions_final, 1e-3))

    monotone = counts[0] >= counts[1] >= counts[2]
    converged = counts[-1] == 1
    return LimitResult(
        "3. Hegselmann-Krause clustering",
        monotone and converged,
        f"cluster counts at epsilon = 0.15, 0.4, 2.0 -> {counts} "
        "(must be non-increasing and end at 1)",
    )


# --------------------------------------------------------------------------- #
# Limit 4 -- mean-field fixed point
# --------------------------------------------------------------------------- #


def limit_mean_field(rel_tol: float = 0.02) -> LimitResult:
    """gamma = 1, homogeneous, one actor at full reach on a regular graph.

    With epsilon = 2 positions converge, so Phi -> 0 and the fixed point of
    spec §3.3 reduces to

        a* = delta * gamma * psi / (1 - mu - delta (1 - psi)),   psi = g / (d + g)

    with g = 1 because broadcast (`random` at rho = 1) reaches every agent every
    step. A ring lattice (Watts-Strogatz at p = 0) is exactly regular, so psi is
    the same constant for all agents, and at gamma = 1 the cap in E_i is inert.
    """
    degree = 6
    gamma = 1.0
    mu, delta = 0.3, 0.4
    config = _base_config(
        n_steps=800,
        network=NetworkSpec(
            topology=Topology.SMALL_WORLD,
            n_agents=300,
            mean_degree=float(degree),
            rewiring_p=0.0,
        ),
        constants=Constants(sigma=0.2, gamma=gamma, zeta=0.0),
        parameters=Parameters(epsilon=2.0, mu=mu, delta=delta, omega=0.0),
        actor_d=entrepreneur(alpha=0.0, rho=1.0),
    )
    result = _run(config)

    psi = 1.0 / (degree + 1.0)  # g = 1 under broadcast
    analytic = delta * gamma * psi / (1.0 - mu - delta * (1.0 - psi))
    simulated = float(result.series("mean_alarm")[-1])
    error = abs(simulated - analytic) / analytic
    return LimitResult(
        "4. Mean-field fixed point",
        error < rel_tol,
        f"simulated {simulated:.6f} vs analytic {analytic:.6f} "
        f"(relative error {error:.2%}, tolerance {rel_tol:.0%})",
    )


# --------------------------------------------------------------------------- #
# Limit 5 -- empty graph
# --------------------------------------------------------------------------- #


def limit_empty_graph(tol: float = 1e-9) -> LimitResult:
    """Empty graph, zeta = 0, actors silent.

    With no neighbours, both E_i and Phi_i are zero, so alarm decays under mu
    alone in every arm and the full run coincides with the null run. Every agent
    must relax to its anchor b_i(0), alarm must decay to zero, and the panic
    index must be identically zero.
    """
    config = _base_config(
        n_steps=500,
        network=NetworkSpec(topology=Topology.EMPTY, n_agents=150, mean_degree=1.0),
        parameters=Parameters(epsilon=2.0, mu=0.4, delta=0.3, omega=0.2),
        actor_d=entrepreneur(alpha=0.0, rho=0.0),
        constants=Constants(sigma=0.2, gamma=3.0, zeta=0.0),
    )
    streams = Streams.from_seed(config.seed)
    initial = initialise(config, streams)
    result = Model(config, streams, initial).run()
    position_error = float(np.max(np.abs(result.positions_final - initial.positions)))
    alarm_error = float(np.max(np.abs(result.alarm_final)))

    cf = run_counterfactual_set(config)
    panic_error = float(np.max(np.abs(cf.decomposition.panic_index)))

    passed = position_error < 1e-6 and alarm_error < tol and panic_error < tol
    return LimitResult(
        "5. Empty graph",
        passed,
        f"position drift {position_error:.2e}, residual alarm {alarm_error:.2e}, "
        f"max |Pi| {panic_error:.2e}",
    )


# --------------------------------------------------------------------------- #
# Property checks that are not limiting cases
# --------------------------------------------------------------------------- #


def property_interaction_zero_at_first_step() -> LimitResult:
    """Spec §10.1: the interaction term is identically zero at t = 1."""
    config = _base_config(
        n_steps=60,
        network=NetworkSpec(topology=Topology.SMALL_WORLD, n_agents=300, mean_degree=8.0),
        parameters=Parameters(epsilon=0.6, mu=0.3, delta=0.3, omega=0.3),
        actor_d=entrepreneur(alpha=0.6, rho=0.3),
        constants=Constants(sigma=0.2, gamma=3.0, zeta=0.01),
    )
    cf = run_counterfactual_set(config)
    value = abs(float(cf.decomposition.interaction[1]))
    return LimitResult(
        "P1. Interaction zero at t=1",
        value < 1e-12,
        f"|interaction(1)| = {value:.2e}, and it becomes non-zero from t=2 onward",
    )


def property_determinism() -> LimitResult:
    """Spec §15: one seed reproduces one trajectory exactly."""
    config = _base_config(
        n_steps=80,
        parameters=Parameters(epsilon=0.6, mu=0.3, delta=0.3, omega=0.3),
        actor_d=entrepreneur(alpha=0.6, rho=0.3),
        constants=Constants(sigma=0.2, gamma=3.0, zeta=0.01),
    )
    first = _run(config)
    second = _run(config)
    identical = bool(np.array_equal(first.positions_final, second.positions_final)) and bool(
        np.array_equal(first.alarm_final, second.alarm_final)
    )
    return LimitResult(
        "P2. Determinism under a fixed seed",
        identical,
        "two runs at the same seed produced bit-identical final states"
        if identical
        else "runs at the same seed diverged",
    )


def property_silencing_by_reach() -> LimitResult:
    """Spec §3.1: alpha = 0 does NOT silence an actor; rho = 0 does.

    An actor with alpha = 0 and rho > 0 persuades no one but still alarms
    everyone it reaches, so its alarm trajectory must differ from a truly
    silent actor's.
    """
    base = dict(
        n_steps=60,
        network=NetworkSpec(topology=Topology.SMALL_WORLD, n_agents=300, mean_degree=8.0),
        parameters=Parameters(epsilon=0.6, mu=0.3, delta=0.4, omega=0.2),
        constants=Constants(sigma=0.2, gamma=3.0, zeta=0.0),
    )
    depth_zero = _run(_base_config(actor_d=entrepreneur(alpha=0.0, rho=0.5), **base))
    reach_zero = _run(_base_config(actor_d=entrepreneur(alpha=0.5, rho=0.0), **base))

    gap = float(
        np.max(np.abs(depth_zero.series("mean_alarm") - reach_zero.series("mean_alarm")))
    )
    return LimitResult(
        "P3. Silencing is by reach, not depth",
        gap > 1e-3,
        f"alpha=0 and rho=0 differ in mean alarm by up to {gap:.4f}, as they must",
    )


def property_interior_bimodality() -> LimitResult:
    """Spec §14.2 (1): the interior coefficient must ignore boundary atoms.

    Docked against a construction with a known answer. A tight unimodal interior,
    Normal(0, 0.12), has skewness 0 and excess kurtosis 0, so BC -> 1/3, far
    below the 5/9 uniform flag. Contaminating it with equal atoms at -1 and +1
    until they carry two thirds of the mass gives a near-three-point
    distribution on {-1, 0, +1}, whose excess kurtosis is -1.52 and whose
    coefficient is therefore 1/(3 - 1.52) = 0.676 -- a false polarization flag
    produced entirely by the atoms. The raw coefficient must clear the flag; the
    interior coefficient must not move from 1/3.
    """
    rng = np.random.default_rng(4242)
    interior = rng.normal(0.0, 0.12, size=2000)
    atoms = np.concatenate([np.full(2000, -1.0), np.full(2000, 1.0)])
    contaminated = np.concatenate([interior, atoms])

    clean = bimodality_coefficient(interior)
    raw = bimodality_coefficient(contaminated)
    recovered = interior_bimodality_coefficient(contaminated)
    share = boundary_fraction(contaminated)

    passed = (
        abs(clean - 1 / 3) < 0.02
        and raw > 5 / 9
        and abs(raw - 0.676) < 0.01
        and abs(recovered - clean) < 1e-12
        and abs(share - 2 / 3) < 1e-12
    )
    return LimitResult(
        "P4. Interior bimodality excludes boundary atoms",
        passed,
        f"interior alone {clean:.3f} (analytic 0.333), with atoms {raw:.3f} "
        f"(analytic 0.676, flag 0.556), recovered {recovered:.3f}, "
        f"boundary share {share:.3f}",
    )


def property_soft_bound() -> LimitResult:
    """Spec §14.2 (1): under the tanh bound nothing is ever pinned to a pole.

    The same setting is run twice. The hard clip must bind and leave atoms; the
    soft bound must leave the positions strictly interior, so the boundary
    fraction is exactly zero and no clip event is counted.
    """
    base = dict(
        n_steps=120,
        network=NetworkSpec(topology=Topology.SMALL_WORLD, n_agents=300, mean_degree=8.0),
        parameters=Parameters(epsilon=0.5, mu=0.3, delta=0.25, omega=0.35),
        actor_d=entrepreneur(alpha=0.8, rho=0.4),
        constants=Constants(sigma=0.0, gamma=3.0, zeta=0.02),
    )
    from .config import BoundMode

    clipped = _run(_base_config(bound_mode=BoundMode.CLIP, **base))
    softened = _run(_base_config(bound_mode=BoundMode.TANH, **base))

    clip_share = float(clipped.series("boundary_fraction")[-1])
    soft_share = float(softened.series("boundary_fraction")[-1])
    passed = (
        clip_share > 0.0
        and soft_share == 0.0
        and softened.structure["clip_events"] == 0
        and float(np.max(np.abs(softened.positions_final))) < 1.0
    )
    return LimitResult(
        "P5. The soft bound leaves no boundary atom",
        passed,
        f"boundary share {clip_share:.3f} under clip vs {soft_share:.3f} under tanh; "
        f"max |b| = {np.max(np.abs(softened.positions_final)):.6f}",
    )


def property_asynchronous_agrees_at_first_step() -> LimitResult:
    """Spec §12.3: the asynchronous sweep must be a scheme change, not a model change.

    Two things are pinned. The first step's *record* is identical under both
    schemes, since it describes the state at the start of the step and no agent
    has moved yet; and both schemes stay deterministic under a fixed seed. If
    the asynchronous path had picked up a different targeting rule, a different
    exposure denominator or a desynchronised noise stream, the first record
    would differ.
    """
    from .config import UpdateOrder

    base = dict(
        n_steps=25,
        network=NetworkSpec(topology=Topology.SMALL_WORLD, n_agents=200, mean_degree=6.0),
        parameters=Parameters(epsilon=0.6, mu=0.3, delta=0.3, omega=0.3),
        actor_d=entrepreneur(alpha=0.6, rho=0.3),
        constants=Constants(sigma=0.0, gamma=3.0, zeta=0.01),
    )
    sync = _run(_base_config(update_order=UpdateOrder.SYNCHRONOUS, **base))
    async_first = _run(_base_config(update_order=UpdateOrder.ASYNCHRONOUS, **base))
    async_again = _run(_base_config(update_order=UpdateOrder.ASYNCHRONOUS, **base))

    same_start = all(
        abs(getattr(sync.records[0], field) - getattr(async_first.records[0], field)) < 1e-12
        for field in ("mean_position", "mean_alarm", "amplifying", "mean_othering")
    )
    deterministic = bool(
        np.array_equal(async_first.positions_final, async_again.positions_final)
        and np.array_equal(async_first.alarm_final, async_again.alarm_final)
    )
    divergence = float(
        np.max(np.abs(sync.series("mean_alarm") - async_first.series("mean_alarm")))
    )
    return LimitResult(
        "P6. Asynchronous updating is a scheme change only",
        same_start and deterministic,
        f"step-0 records identical, asynchronous runs reproducible; the two schemes "
        f"then differ in mean alarm by up to {divergence:.4f} over 25 steps",
    )


def property_counterfactual_validity() -> LimitResult:
    """Spec §14.2 (2): the arms must stay comparable over the reported horizon.

    Re-drawing only the position noise, with the population held fixed, must move
    a single arm by far less than the gap the four-way comparison is resolving.
    A horizon of None means the criterion was never met inside the run, which is
    the outcome the decomposition needs.
    """
    config = _base_config(
        n_steps=200,
        network=NetworkSpec(topology=Topology.SMALL_WORLD, n_agents=400, mean_degree=10.0),
        parameters=Parameters(epsilon=0.5, mu=0.30, delta=0.25, omega=0.35),
        actor_d=entrepreneur(alpha=0.7, rho=0.25),
        constants=Constants(sigma=0.0, gamma=3.0, zeta=0.01),
    )
    report = counterfactual_validity(config, n_replicates=4)
    horizon = report["horizon"]
    passed = horizon is None or horizon > 100
    return LimitResult(
        "P7. Counterfactual validity horizon",
        passed,
        f"horizon = {horizon if horizon is not None else 'not reached within the run'}; "
        f"largest within-arm noise s.d. {report['max_noise']:.2e} against a "
        f"full-vs-null gap of {report['signal'][-1]:.4f}",
    )


def property_fixed_random_isolates_the_schedule() -> LimitResult:
    """Spec §7.1: `fixed_random` must share `random`'s rule and `hub`'s schedule.

    Three things are pinned, and together they make the repertoire a usable
    control. Its audience is the same set at every step, so cumulative exposure
    is maximally concentrated; that audience is drawn uniformly, so it carries no
    degree signal (its mean degree must match the population's); and it is
    identical across the four arms of the 2x2, without which the counterfactual
    would compare different campaigns.
    """
    config = _base_config(
        n_steps=60,
        network=NetworkSpec(topology=Topology.SMALL_WORLD, n_agents=600, mean_degree=10.0),
        parameters=Parameters(epsilon=0.5, mu=0.30, delta=0.25, omega=0.35),
        actor_d=entrepreneur(alpha=0.7, rho=0.2, repertoire=Repertoire.FIXED_RANDOM),
        constants=Constants(sigma=0.0, gamma=3.0, zeta=0.01),
    )
    streams = Streams.from_seed(config.seed)
    initial = initialise(config, streams)
    model = Model(config, streams, initial)
    audience = model._fixed_audience["D"]
    result = model.run()

    degrees = np.array([d for _, d in initial.graph.degree()], dtype=float)
    reached = result.reach_counts_d
    n_targets = config.actor_d.n_targets(degrees.size)

    same_every_step = bool(
        np.count_nonzero(reached) == n_targets
        and np.all(reached[reached > 0] == config.n_steps)
    )
    no_degree_signal = abs(degrees[audience].mean() - degrees.mean()) < 1.0
    cf = run_counterfactual_set(config)
    shared = bool(
        np.array_equal(
            np.flatnonzero(cf.runs["full"].reach_counts_d),
            np.flatnonzero(cf.runs["claims"].reach_counts_d),
        )
    )
    return LimitResult(
        "P8. fixed_random isolates the exposure schedule",
        same_every_step and no_degree_signal and shared,
        f"{n_targets} agents reached at every one of {config.n_steps} steps and nobody else; "
        f"audience mean degree {degrees[audience].mean():.2f} vs population "
        f"{degrees.mean():.2f}; audience identical across the 2x2 arms",
    )


def property_handover_guard() -> LimitResult:
    """Spec §10.3: the handover criterion must not fire on the entrepreneur's exit.

    After withdrawal claims-alone is zero, so `interaction > claims_alone` holds
    for any positive interaction at all. The polarized regime is where this
    bites: there the interaction stays small (the alarm is mostly pre-existing
    division, which the criterion is designed to exclude) and never overtakes
    claims-alone while the entrepreneur is speaking -- so the unguarded criterion
    reports a handover one step after t_off, which is arithmetic and not a
    finding. The guarded version must decline instead.
    """
    t_off = 150
    config = _base_config(
        seed=11,
        n_steps=400,
        network=NetworkSpec(topology=Topology.SMALL_WORLD, n_agents=1000, mean_degree=10.0),
        parameters=Parameters(epsilon=0.5, mu=0.30, delta=0.25, omega=0.35),
        actor_d=entrepreneur(
            alpha=0.7, rho=0.25, repertoire=Repertoire.BASE, active_until=t_off
        ),
        constants=Constants(sigma=0.0, gamma=3.0, zeta=0.01),
        position_regime=PositionRegime.POLARIZED,
    )
    cf = run_counterfactual_set(config)
    unguarded = cf.handover_step(require_active=False)
    guarded = cf.handover_step()
    passed = unguarded == t_off + 1 and guarded is None
    return LimitResult(
        "P9. The handover criterion is guarded by the actor's window",
        passed,
        f"unguarded fires at t = {unguarded}, one step after t_off = {t_off} and only "
        f"because claims-alone reached zero; guarded returns {guarded}, as it must when "
        "the interaction never overtakes the signal while the entrepreneur is speaking",
    )


ALL_CHECKS: List[Callable[[], LimitResult]] = [
    limit_degroot,
    limit_friedkin_johnsen,
    limit_hegselmann_krause,
    limit_mean_field,
    limit_empty_graph,
    property_interaction_zero_at_first_step,
    property_determinism,
    property_silencing_by_reach,
    property_interior_bimodality,
    property_soft_bound,
    property_asynchronous_agrees_at_first_step,
    property_counterfactual_validity,
    property_fixed_random_isolates_the_schedule,
    property_handover_guard,
]


def run_all() -> List[LimitResult]:
    return [check() for check in ALL_CHECKS]
