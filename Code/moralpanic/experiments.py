"""The three experiments (spec §12.1).

An actor is activated or silenced by its reach rho_X, never by its depth alpha_X.

    A -- Ignition (H1): D's repertoire x topology x initial regime, then a fine
         sweep in rho_D to locate any abrupt transition, and an alpha x rho grid.
    B -- Handover (H2): the settings that ignite, re-run with rho_D -> 0 at
         t_off and C still silent, tracking the decomposition across withdrawal.
    C -- Counter-claims-making (H3): D fixed and withdrawing at t_off; C entering
         at t_off at three configurations that span the dilemma, not a grid.

Each cell is a set of seeds, and each seed costs the four runs of the 2x2.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Dict, Iterable, List, Optional, Sequence

import numpy as np

from .config import (
    NetworkSpec,
    Parameters,
    PositionRegime,
    Repertoire,
    RunConfig,
    SILENT_C,
    ThresholdRegime,
    Topology,
    counter_entrepreneur,
    entrepreneur,
)
from .counterfactual import CounterfactualResult, run_counterfactual_set


# --------------------------------------------------------------------------- #
# Cells
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Cell:
    """One design cell: a configuration template plus a label."""

    label: Dict[str, object]
    config: RunConfig

    def with_seed(self, seed: int) -> RunConfig:
        return replace(self.config, seed=seed)


@dataclass
class CellOutcome:
    """Seed-level results for one cell, summarised as distributions."""

    label: Dict[str, object]
    results: List[CounterfactualResult]

    def panic_incidence(
        self, pi_star: float = 0.5, q_star: float = 0.5, window: int = 10
    ) -> float:
        """Frequency of panic episodes over seeds (spec §10.3). Never single runs."""
        flags = [
            r.panic_episode(pi_star, q_star, window) is not None for r in self.results
        ]
        return float(np.mean(flags))

    def monte_carlo_se(self, incidence: Optional[float] = None) -> float:
        """Standard error of the reported incidence, which sets the seed count."""
        p = self.panic_incidence() if incidence is None else incidence
        return float(np.sqrt(max(p * (1.0 - p), 0.0) / max(len(self.results), 1)))

    def onset_times(self, **kwargs) -> np.ndarray:
        times = [r.panic_episode(**kwargs) for r in self.results]
        return np.array([t for t in times if t is not None], dtype=float)

    def handover_times(self, hold: int = 10) -> np.ndarray:
        times = [r.handover_step(hold) for r in self.results]
        return np.array([t for t in times if t is not None], dtype=float)

    def mean_curve(self, name: str) -> np.ndarray:
        """Seed-averaged curve of one decomposition component or panic index."""
        stack = np.array([getattr(r.decomposition, name) for r in self.results])
        return stack.mean(axis=0)

    def persistence(self, t_off: int) -> Dict[str, np.ndarray]:
        """Durations and censoring flags after withdrawal (spec §10.3)."""
        entries = [r.persistence(t_off) for r in self.results]
        return {
            "duration": np.array([e["duration"] for e in entries], dtype=float),
            "censored": np.array([e["censored"] for e in entries], dtype=bool),
        }

    def exposure_concentration(self) -> np.ndarray:
        return np.array([r.exposure_concentration() for r in self.results], dtype=float)


def run_cell(cell: Cell, seeds: Sequence[int]) -> CellOutcome:
    """Run one cell over a list of seeds; four simulations per seed."""
    return CellOutcome(
        label=cell.label,
        results=[run_counterfactual_set(cell.with_seed(seed)) for seed in seeds],
    )


# --------------------------------------------------------------------------- #
# Experiment A -- Ignition (H1)
# --------------------------------------------------------------------------- #


def experiment_a_cells(
    parameters: Parameters,
    n_agents: int = 1000,
    mean_degree: float = 10.0,
    n_steps: int = 200,
    alpha: float = 0.6,
    reaches: Iterable[float] = tuple(np.round(np.linspace(0.02, 0.5, 12), 4)),
    repertoires: Iterable[Repertoire] = tuple(Repertoire),
    topologies: Iterable[Topology] = (
        Topology.SMALL_WORLD,
        Topology.HUB_DOMINATED,
        Topology.RANDOM_GRAPH,
    ),
    position_regimes: Iterable[PositionRegime] = tuple(PositionRegime),
    threshold_regimes: Iterable[ThresholdRegime] = (ThresholdRegime.DISPERSED,),
) -> List[Cell]:
    """Repertoire x topology x initial regime x reach, with C silent (spec §12.1).

    The uniform-threshold regime is included by passing both threshold regimes;
    it isolates the role of threshold dispersion in producing the discontinuity.
    """
    cells: List[Cell] = []
    for topology in topologies:
        for position_regime in position_regimes:
            for threshold_regime in threshold_regimes:
                for repertoire in repertoires:
                    for rho in reaches:
                        cells.append(
                            Cell(
                                label={
                                    "experiment": "A",
                                    "topology": topology.value,
                                    "positions": position_regime.value,
                                    "thresholds": threshold_regime.value,
                                    "repertoire": repertoire.value,
                                    "alpha": alpha,
                                    "rho": float(rho),
                                },
                                config=RunConfig(
                                    seed=0,
                                    n_steps=n_steps,
                                    network=NetworkSpec(
                                        topology=topology,
                                        n_agents=n_agents,
                                        mean_degree=mean_degree,
                                    ),
                                    parameters=parameters,
                                    actor_d=entrepreneur(alpha, float(rho), repertoire),
                                    actor_c=SILENT_C,
                                    position_regime=position_regime,
                                    threshold_regime=threshold_regime,
                                ),
                            )
                        )
    return cells


def experiment_a_depth_reach_cells(
    parameters: Parameters,
    repertoire: Repertoire = Repertoire.BASE,
    topology: Topology = Topology.SMALL_WORLD,
    n_agents: int = 1000,
    mean_degree: float = 10.0,
    n_steps: int = 200,
    alphas: Iterable[float] = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9),
    reaches: Iterable[float] = (0.05, 0.10, 0.20, 0.30, 0.50, 0.70, 1.00),
    position_regime: PositionRegime = PositionRegime.CONSENSUAL,
) -> List[Cell]:
    """Depth against reach on a grid (spec §12.1, the second half of Experiment A).

    H1 claims reach dominates depth above a threshold. Testing that needs both
    axes at once, because the threshold is in the *other* one: a reached agent
    moves by alpha*(1 - b_i), and only when that exceeds the tolerance epsilon do
    its bounded-confidence ties break and division get manufactured at all. Below
    that, the entrepreneur converts the population and no reach ignites.
    """
    return [
        Cell(
            label={
                "experiment": "A",
                "block": "depth_reach",
                "topology": topology.value,
                "repertoire": repertoire.value,
                "alpha": float(alpha),
                "rho": float(rho),
                "epsilon": parameters.epsilon,
            },
            config=RunConfig(
                seed=0,
                n_steps=n_steps,
                network=NetworkSpec(
                    topology=topology, n_agents=n_agents, mean_degree=mean_degree
                ),
                parameters=parameters,
                actor_d=entrepreneur(float(alpha), float(rho), repertoire),
                actor_c=SILENT_C,
                position_regime=position_regime,
            ),
        )
        for alpha in alphas
        for rho in reaches
    ]


# --------------------------------------------------------------------------- #
# Experiment B -- Handover (H2)
# --------------------------------------------------------------------------- #


def experiment_b_cell(
    parameters: Parameters,
    repertoire: Repertoire,
    topology: Topology,
    rho: float,
    alpha: float = 0.6,
    n_agents: int = 1000,
    mean_degree: float = 10.0,
    n_steps: int = 400,
    t_off: int = 150,
    position_regime: PositionRegime = PositionRegime.CONSENSUAL,
) -> Cell:
    """One igniting setting, re-run with D withdrawing at t_off and C silent."""
    return Cell(
        label={
            "experiment": "B",
            "topology": topology.value,
            "repertoire": repertoire.value,
            "positions": position_regime.value,
            "alpha": alpha,
            "rho": rho,
            "t_off": t_off,
            **{"mu": parameters.mu, "delta": parameters.delta, "omega": parameters.omega},
        },
        config=RunConfig(
            seed=0,
            n_steps=n_steps,
            network=NetworkSpec(
                topology=topology, n_agents=n_agents, mean_degree=mean_degree
            ),
            parameters=parameters,
            actor_d=entrepreneur(alpha, rho, repertoire, active_until=t_off),
            actor_c=SILENT_C,
            position_regime=position_regime,
        ),
    )


# --------------------------------------------------------------------------- #
# Experiment C -- Counter-claims-making (H3)
# --------------------------------------------------------------------------- #

COUNTER_CONFIGURATIONS: Dict[str, Dict[str, float]] = {
    "broad_shallow": {"alpha": 0.15, "rho": 0.60},
    "narrow_deep": {"alpha": 0.90, "rho": 0.10},
    "matched": {},  # filled from D's values at withdrawal
}
"""The three points that span H3's dilemma (spec §12.1). Not a grid."""


def experiment_c_cells(
    parameters: Parameters,
    repertoire: Repertoire,
    topology: Topology,
    rho_d: float,
    alpha_d: float = 0.6,
    n_agents: int = 1000,
    mean_degree: float = 10.0,
    n_steps: int = 400,
    t_off: int = 150,
    counter_repertoire: Repertoire = Repertoire.RANDOM,
    position_regime: PositionRegime = PositionRegime.CONSENSUAL,
) -> List[Cell]:
    """D withdraws at t_off; C enters at t_off at three configurations.

    In this experiment the "claims-making on" runs of the 2x2 include C's entry,
    so the panic index measures excess over a world with no organized
    claims-making of either kind (spec §12.1).
    """
    cells: List[Cell] = []
    for name, override in COUNTER_CONFIGURATIONS.items():
        alpha_c = override.get("alpha", alpha_d)
        rho_c = override.get("rho", rho_d)
        cells.append(
            Cell(
                label={
                    "experiment": "C",
                    "counter_configuration": name,
                    "topology": topology.value,
                    "repertoire": repertoire.value,
                    "alpha_c": alpha_c,
                    "rho_c": rho_c,
                    "t_off": t_off,
                },
                config=RunConfig(
                    seed=0,
                    n_steps=n_steps,
                    network=NetworkSpec(
                        topology=topology, n_agents=n_agents, mean_degree=mean_degree
                    ),
                    parameters=parameters,
                    actor_d=entrepreneur(alpha_d, rho_d, repertoire, active_until=t_off),
                    actor_c=counter_entrepreneur(
                        alpha_c, rho_c, counter_repertoire, active_from=t_off
                    ),
                    position_regime=position_regime,
                ),
            )
        )
    return cells


def counter_effect(withdrawal_only: CellOutcome, with_counter: CellOutcome) -> Dict[str, float]:
    """H3's directional read: does defense lower the panic index or raise it?

    The diagnostic is the pair (mean position, panic index): a response that
    moves positions toward its own pole while the index rises has won the
    argument and lost the panic (spec §10.3, §13).
    """
    base_pi = withdrawal_only.mean_curve("panic_index")[-1]
    counter_pi = with_counter.mean_curve("panic_index")[-1]
    base_b = np.mean([r.full.series("mean_position")[-1] for r in withdrawal_only.results])
    counter_b = np.mean([r.full.series("mean_position")[-1] for r in with_counter.results])
    return {
        "delta_panic_index": float(counter_pi - base_pi),
        "delta_mean_position": float(counter_b - base_b),
        "lowers_panic": bool(counter_pi < base_pi),
    }
