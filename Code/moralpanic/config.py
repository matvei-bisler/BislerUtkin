"""Configuration objects for the moral panic model.

Every field maps onto a named quantity in the specification (`model_simplified.md`);
section references in docstrings point there.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Optional

import numpy as np

# --------------------------------------------------------------------------- #
# Parameters and constants (spec §3)
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Parameters:
    """The four global parameters (spec §3.1).

    epsilon : moral tolerance, in [0, 2]
    mu      : alarm memory, in [0, 1)
    delta   : alarm contagion, in [0, 1]
    omega   : othering, in [0, 1]
    """

    epsilon: float
    mu: float
    delta: float
    omega: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.epsilon <= 2.0:
            raise ValueError("epsilon must lie in [0, 2]")
        for name in ("mu", "delta", "omega"):
            value = getattr(self, name)
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must lie in [0, 1]")
        if self.mu >= 1.0:
            raise ValueError("mu must be strictly below 1")

    # -- stability conditions (spec §3.3) ---------------------------------- #

    @property
    def alarm_intensity(self) -> float:
        """Total alarm intensity mu + delta + omega, the quantity C1 bounds."""
        return self.mu + self.delta + self.omega

    def satisfies_c1(self, tol: float = 1e-12) -> bool:
        """C1: mu + delta + omega <= 1 keeps alarm in range without clipping."""
        return self.alarm_intensity <= 1.0 + tol

    def satisfies_c2(self) -> bool:
        """C2: mu + delta < 1 keeps contagion sub-critical."""
        return self.mu + self.delta < 1.0

    def require_stable(self) -> None:
        if not self.satisfies_c1():
            raise ValueError(
                f"C1 violated: mu+delta+omega = {self.alarm_intensity:.4f} > 1 (spec §3.3)"
            )
        if not self.satisfies_c2():
            raise ValueError(
                f"C2 violated: mu+delta = {self.mu + self.delta:.4f} >= 1 (spec §3.3)"
            )

    def without_othering(self) -> "Parameters":
        """The omega=0 arm of the 2x2 counterfactual design (spec §10.1)."""
        return replace(self, omega=0.0)


@dataclass(frozen=True)
class Constants:
    """The three fixed constants (spec §3.2).

    sigma defaults to ZERO. The anchor sigma*b_i(0) is a restoring force toward
    each agent's pre-campaign position; under the consensual regime those all
    sit near zero, so a positive sigma returns the population to consensus once
    the entrepreneur withdraws and dissolves the division the campaign created.
    Post-withdrawal persistence then tracks -1/ln(1-sigma) rather than omega,
    which is the reverse of H2. Bounded confidence already prevents the trivial
    DeGroot consensus that spec §11 credits to the anchor, so sigma = 0 costs
    nothing the model needs. If sigma is set positive it must enter the
    sensitivity analysis of spec §12.2, because it competes with omega directly.
    """

    sigma: float = 0.0
    gamma: float = 3.0
    zeta: float = 0.01

    def __post_init__(self) -> None:
        if not 0.0 <= self.sigma <= 1.0:
            raise ValueError("sigma must lie in [0, 1]")
        if self.gamma < 1.0:
            raise ValueError("gamma must be at least 1")
        if self.zeta < 0.0:
            raise ValueError("zeta must be non-negative")


# --------------------------------------------------------------------------- #
# Claims-makers (spec §5, §7.1)
# --------------------------------------------------------------------------- #


class Repertoire(str, Enum):
    """The claims-making repertoires (spec §7.1).

    FIXED_RANDOM is the control the other three need. `hub` and `base` differ
    from `random` in two ways at once -- whom they select, and that they select
    the *same* people every step -- so an effect attributed to degree targeting
    may be an effect of a fixed audience. FIXED_RANDOM holds the schedule fixed
    while removing the selection rule: a uniformly random subset, drawn once and
    addressed every step. It shares `random`'s selection logic and `hub`'s
    exposure schedule, which is what makes the two explanations separable.
    """

    RANDOM = "random"  # null benchmark; at rho=1 this is mass broadcast
    HUB = "hub"  # the n highest-degree nodes
    BASE = "base"  # the n agents closest to the actor's own pole
    FIXED_RANDOM = "fixed_random"  # one random subset, addressed every step


@dataclass(frozen=True)
class ActorSpec:
    """One external claims-maker (spec §5).

    pole          : +1 for the entrepreneur D, -1 for the counter-entrepreneur C
    alpha         : depth, how hard it pushes each agent it reaches
    rho           : reach, the share of the population it reaches per step
    repertoire    : whom it targets
    active_from   : first step at which it acts (inclusive)
    active_until  : first step at which it no longer acts (exclusive); None = never stops

    An actor is SILENT when rho == 0 or when the step falls outside its window.
    Setting alpha = 0 is NOT equivalent: alpha scales only the position channel,
    while a targeted agent still counts the actor as a maximally alarmed contact
    in the alarm exposure E_i (spec §3.1, §7.4).
    """

    pole: float
    alpha: float
    rho: float
    repertoire: Repertoire = Repertoire.RANDOM
    active_from: int = 0
    active_until: Optional[int] = None
    name: str = "D"

    def __post_init__(self) -> None:
        if self.pole not in (-1.0, 1.0):
            raise ValueError("pole must be +1 (entrepreneur) or -1 (counter-entrepreneur)")
        if not 0.0 <= self.alpha <= 1.0:
            raise ValueError("alpha must lie in [0, 1]")
        if not 0.0 <= self.rho <= 1.0:
            raise ValueError("rho must lie in [0, 1]")

    def is_active(self, t: int) -> bool:
        if self.rho <= 0.0:
            return False
        if t < self.active_from:
            return False
        if self.active_until is not None and t >= self.active_until:
            return False
        return True

    def silenced(self) -> "ActorSpec":
        """The rho=0 arm of the 2x2 counterfactual design (spec §10.1)."""
        return replace(self, rho=0.0)

    def n_targets(self, n_agents: int) -> int:
        return int(min(n_agents, np.ceil(self.rho * n_agents)))


def entrepreneur(
    alpha: float,
    rho: float,
    repertoire: Repertoire = Repertoire.RANDOM,
    active_until: Optional[int] = None,
) -> ActorSpec:
    """The moral entrepreneur D, pushing toward p_D = +1 (spec §5)."""
    return ActorSpec(
        pole=+1.0,
        alpha=alpha,
        rho=rho,
        repertoire=repertoire,
        active_until=active_until,
        name="D",
    )


def counter_entrepreneur(
    alpha: float,
    rho: float,
    repertoire: Repertoire = Repertoire.RANDOM,
    active_from: int = 0,
) -> ActorSpec:
    """The counter-entrepreneur C, pushing toward p_C = -1 (spec §5)."""
    return ActorSpec(
        pole=-1.0,
        alpha=alpha,
        rho=rho,
        repertoire=repertoire,
        active_from=active_from,
        name="C",
    )


SILENT_C = counter_entrepreneur(alpha=0.0, rho=0.0)
"""A permanently silent counter-entrepreneur, used in Experiments A and B."""


# --------------------------------------------------------------------------- #
# Network and initialization (spec §4, §8)
# --------------------------------------------------------------------------- #


class Topology(str, Enum):
    """The three generators (spec §4), compared at matched mean degree."""

    SMALL_WORLD = "watts_strogatz"
    HUB_DOMINATED = "holme_kim"
    RANDOM_GRAPH = "erdos_renyi"
    EMPIRICAL = "empirical"  # an edge list read from disk; appendix only (spec §12.3)
    EMPTY = "empty"  # no edges; a degenerate case used by verification limit 5


class BoundMode(str, Enum):
    """How the position update is kept inside [-1, 1] (spec §7.3, §14.2).

    CLIP -- the specification's own rule. Noise, and claims-making acting with a
        strong peer pull, can drive a position past a pole, and clipping then
        accumulates mass as two point atoms at +/-1. That mass inflates any
        moment-based polarization statistic, which is artifact 1 of spec §14.2.

    TANH -- the soft replacement that artifact check asks for: the identity on
        [-c, c] and a tanh knee beyond it, so positions approach the poles
        without ever reaching them, no atom forms, and `boundary_fraction` is
        identically zero.

        The knee, rather than a plain b = tanh(raw), is load-bearing. tanh(x) < x
        for every x > 0, so plain tanh is not only a bound but a contraction
        toward the origin: with no forcing at all it would drive every position
        geometrically to zero. That is a restoring force toward the pre-campaign
        consensus, which is exactly the mechanism spec §3.2 refuses to leave
        outside the analysis in the case of sigma, and it would dissolve
        manufactured division for reasons having nothing to do with the boundary.
        Keeping the map the identity on the interior confines the change to where
        the artifact actually lives.
    """

    CLIP = "clip"
    TANH = "tanh"


SOFT_CORE = 0.9
"""Where the soft bound's knee begins (spec §14.2).

The map is the identity on [-SOFT_CORE, SOFT_CORE] and bends only beyond it, so
it alters the dynamics only in the region where the hard clip would have been
accumulating its atoms.
"""


class UpdateOrder(str, Enum):
    """Synchronous or random-order sequential updating (spec §6, §12.3).

    SYNCHRONOUS -- the specification's scheme: everything dated t+1 is computed
        from quantities dated t.

    ASYNCHRONOUS -- agents are visited in a fresh random order each step and each
        writes its new position and alarm immediately, so later agents in the
        sweep read some already-updated neighbours. Included as the appendix
        check on the update scheme (spec §12.3). Targeting is still decided once
        per step from the step-start state, so the actors are not given a
        within-step information advantage.
    """

    SYNCHRONOUS = "synchronous"
    ASYNCHRONOUS = "asynchronous"


class ExposureMode(str, Enum):
    """How amplifying neighbours enter alarm exposure E_i (spec §7.4).

    PROPORTIONAL -- E_i is a kappa-weighted MEAN of neighbour alarm. Because a
        mean can never exceed its largest input, E_i <= max_j a_j, so under C2
        the population peak contracts geometrically and endogenous cascades are
        impossible at any gamma. Amplification only re-weights who counts.

    REINFORCING -- the same numerator divided by the neighbour COUNT, then
        clipped to [0, 1]. Amplifying neighbours now ADD rather than re-weight,
        so an agent with many alarmed contacts can end up more alarmed than any
        of them. This is the complex contagion of Granovetter (1978) and Centola
        & Macy (2007): reinforcement from multiple alarmed contacts. The two
        modes coincide exactly at gamma = 1 and diverge as gamma grows.
    """

    PROPORTIONAL = "proportional"
    REINFORCING = "reinforcing"


class PositionRegime(str, Enum):
    """Initial position regimes (spec §8)."""

    CONSENSUAL = "consensual"  # Uniform[-0.2, 0.2]; the default
    POLARIZED = "polarized"  # equal mixture of Normal(+/-0.7, 0.15), truncated


class ThresholdRegime(str, Enum):
    """Initial threshold regimes (spec §8)."""

    DISPERSED = "dispersed"  # Uniform[0, 1]; the default
    UNIFORM = "uniform"  # constant 0.5, removing heterogeneity


@dataclass(frozen=True)
class NetworkSpec:
    """Network generation (spec §4). Generators are matched on mean degree.

    `edge_list` is required by, and only used by, `Topology.EMPIRICAL`: the path
    to a whitespace-separated edge list. The file fixes the population, so
    `n_agents` and `mean_degree` are ignored for that topology and the realised
    values are recorded per run instead (spec §4, §12.3).
    """

    topology: Topology = Topology.SMALL_WORLD
    n_agents: int = 1000
    mean_degree: float = 10.0
    rewiring_p: float = 0.1  # Watts-Strogatz only
    triad_p: float = 0.5  # Holme-Kim only
    edge_list: Optional[str] = None  # Topology.EMPIRICAL only

    def __post_init__(self) -> None:
        if self.n_agents < 2:
            raise ValueError("n_agents must be at least 2")
        if self.mean_degree <= 0:
            raise ValueError("mean_degree must be positive")
        if self.topology is Topology.EMPIRICAL and not self.edge_list:
            raise ValueError("Topology.EMPIRICAL requires an edge_list path (spec §12.3)")


@dataclass(frozen=True)
class RunConfig:
    """Everything needed to reproduce one trajectory (spec §8).

    Given `seed`, `network`, `parameters`, `constants` and the actor specs, a run
    is exactly reproducible. The four runs of a 2x2 counterfactual set share the
    seed and therefore the network, initial positions, initial alarm and
    thresholds (spec §15).
    """

    seed: int
    n_steps: int
    network: NetworkSpec
    parameters: Parameters
    actor_d: ActorSpec
    actor_c: ActorSpec = SILENT_C
    constants: Constants = Constants()
    exposure_mode: ExposureMode = ExposureMode.REINFORCING
    position_regime: PositionRegime = PositionRegime.CONSENSUAL
    threshold_regime: ThresholdRegime = ThresholdRegime.DISPERSED
    bound_mode: BoundMode = BoundMode.CLIP
    update_order: UpdateOrder = UpdateOrder.SYNCHRONOUS
    initial_alarm_max: float = 0.1
    record_states: bool = False

    def __post_init__(self) -> None:
        if self.n_steps < 1:
            raise ValueError("n_steps must be at least 1")
        if self.initial_alarm_max <= 0.0:
            # Spec §8: a zero baseline makes the null run identically zero and
            # collapses the panic index to plain mean alarm.
            raise ValueError(
                "initial_alarm_max must be strictly positive (spec §8): a zero "
                "baseline destroys the counterfactual the panic index rests on"
            )
        if self.initial_alarm_max > 1.0:
            raise ValueError("initial_alarm_max must not exceed 1")

    @property
    def n_agents(self) -> int:
        return self.network.n_agents
