"""The appendix robustness checks of spec §12.3.

Four exercises, run on the headline settings only and reported as a single
table, not in the main text:

    1. population size   -- N in {500, 1000, 2000}
    2. empirical network -- one public friendship or ego-network, structure only
    3. fixed constants   -- two alternative values of each of sigma, gamma, zeta
    4. update scheme     -- random-order asynchronous updating

Plus the two artifact checks of spec §14.2, which belong with them because they
are checks on the instrument rather than results:

    5. boundary pile-up  -- interior bimodality, and a soft-tanh replication
    6. counterfactual validity -- the step past which the arms stop being
       comparable, beyond which Pi and the handover time are not reportable

Each returns a list of plain dicts, one per cell, so a caller can tabulate or
serialise them without knowing anything about the model.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence

import numpy as np

from .config import (
    BoundMode,
    Constants,
    NetworkSpec,
    RunConfig,
    Topology,
    UpdateOrder,
)
from .counterfactual import counterfactual_validity, is_subcritical, run_counterfactual_set
from .network import build_graph, structural_summary
from .rng import Streams


# --------------------------------------------------------------------------- #
# Shared summary
# --------------------------------------------------------------------------- #


def summarise_cell(
    config: RunConfig, seeds: Sequence[int], t_off: Optional[int] = None
) -> Dict[str, object]:
    """Run one setting over seeds and reduce it to the headline quantities.

    Everything is a distribution over seeds and never a single run (spec §10.3).
    """
    results = [run_counterfactual_set(replace(config, seed=seed)) for seed in seeds]
    at = (t_off - 1) if t_off else (config.n_steps - 1)

    def over_seeds(extract) -> Dict[str, float]:
        values = np.array([extract(r) for r in results], dtype=float)
        return {"mean": float(values.mean()), "sd": float(values.std(ddof=1)) if values.size > 1 else 0.0}

    summary: Dict[str, object] = {
        "n_seeds": len(seeds),
        "n_agents": int(results[0].full.positions_final.size),
        "structure": {
            key: float(results[0].structure[key])
            for key in ("mean_degree", "clustering", "isolate_fraction", "n_components")
        },
        "panic_index_at": over_seeds(lambda r: r.decomposition.panic_index[at]),
        "interaction_at": over_seeds(lambda r: r.decomposition.interaction[at]),
        "claims_alone_at": over_seeds(lambda r: r.decomposition.claims_alone[at]),
        "othering_alone_at": over_seeds(lambda r: r.decomposition.othering_alone[at]),
        "panic_index_end": over_seeds(lambda r: r.decomposition.panic_index[-1]),
        "amplifying_at": over_seeds(lambda r: r.full.series("amplifying")[at]),
        "mean_position_at": over_seeds(lambda r: r.full.series("mean_position")[at]),
        "null_peak": float(max(r.null_peak() for r in results)),
        "boundary": {
            key: float(np.mean([r.boundary_diagnostics()[key] for r in results]))
            for key in ("bimodality", "bimodality_interior", "boundary_fraction", "clip_rate")
        },
    }
    handovers = [r.handover_step() for r in results]
    reached = [h for h in handovers if h is not None]
    summary["handover"] = {
        "median": float(np.median(reached)) if reached else None,
        "reached": f"{len(reached)}/{len(results)}",
    }
    if t_off is not None:
        entries = [r.persistence(t_off) for r in results]
        summary["persistence"] = {
            "median": float(np.median([e["duration"] for e in entries])),
            "censored": f"{sum(e['censored'] for e in entries)}/{len(entries)}",
        }
    return summary


# --------------------------------------------------------------------------- #
# 1. Population size (spec §12.3)
# --------------------------------------------------------------------------- #


def check_population_size(
    config: RunConfig, seeds: Sequence[int], sizes: Iterable[int] = (500, 1000, 2000),
    t_off: Optional[int] = None,
) -> List[Dict[str, object]]:
    """Replicate the headline setting at three population sizes.

    N is a modelling choice rather than an empirical target (spec §2.4), so what
    matters is that the headline conclusions do not turn on it. Mean degree is
    held fixed, so the three differ in size and not in density.
    """
    rows = []
    for n_agents in sizes:
        variant = replace(config, network=replace(config.network, n_agents=int(n_agents)))
        rows.append({"check": "population_size", "n_agents": int(n_agents),
                     **summarise_cell(variant, seeds, t_off)})
    return rows


# --------------------------------------------------------------------------- #
# 2. Empirical network (spec §12.3)
# --------------------------------------------------------------------------- #


def check_empirical_network(
    config: RunConfig,
    seeds: Sequence[int],
    edge_list: str,
    t_off: Optional[int] = None,
    match_generators: bool = True,
) -> List[Dict[str, object]]:
    """Replicate on one empirical network, with the generators matched to it.

    The graph enters as fixed structure only; node attributes are discarded and
    agent state is initialized exactly as in spec §8. The three synthetic
    generators are re-run at the empirical network's *realised* size and mean
    degree, because comparing them at their own defaults would confound a
    structure effect with a density effect (spec §4).

    The C3 sub-criticality probe is re-run on every row, because mean degree
    moves the reinforcement boundary: a parameter point that is sub-critical at
    the operating point's mean degree of 10 need not be at 43.7. Reading an
    empirical row without that check would risk reporting alarm that no longer
    depends on the forcing (spec §3.3).
    """
    empirical = replace(
        config,
        network=NetworkSpec(topology=Topology.EMPIRICAL, edge_list=str(edge_list)),
    )
    graph = build_graph(empirical.network, Streams.from_seed(seeds[0]))
    structure = structural_summary(graph)
    probe = is_subcritical(empirical)
    rows = [{
        "check": "empirical_network",
        "topology": "empirical",
        "source": str(Path(edge_list).name),
        "c3": {"subcritical": bool(probe["subcritical"]),
               "resting_mean_alarm": float(probe["resting_mean_alarm"])},
        **summarise_cell(empirical, seeds, t_off),
    }]

    if match_generators:
        for topology in (Topology.SMALL_WORLD, Topology.HUB_DOMINATED, Topology.RANDOM_GRAPH):
            matched = replace(
                config,
                network=NetworkSpec(
                    topology=topology,
                    n_agents=int(structure["n_agents"]),
                    mean_degree=float(structure["mean_degree"]),
                ),
            )
            matched_probe = is_subcritical(matched)
            rows.append({
                "check": "empirical_network",
                "topology": topology.value,
                "source": "matched generator",
                "c3": {"subcritical": bool(matched_probe["subcritical"]),
                       "resting_mean_alarm": float(matched_probe["resting_mean_alarm"])},
                **summarise_cell(matched, seeds, t_off),
            })
    return rows


# --------------------------------------------------------------------------- #
# 3. The fixed constants (spec §3.2, §12.3)
# --------------------------------------------------------------------------- #

CONSTANT_ALTERNATIVES: Dict[str, Sequence[float]] = {
    "sigma": (0.05, 0.10),
    "gamma": (2.0, 5.0),
    "zeta": (0.0, 0.05),
}
"""Two alternative values of each constant, as spec §3.2 requires.

sigma is the one that is *not* neutral: it is a restoring force toward each
agent's pre-campaign position, so a positive value dissolves the manufactured
division and post-withdrawal persistence tracks -1/ln(1-sigma) rather than
omega. The check exists to show that, not to hide it.
"""


def check_constants(
    config: RunConfig, seeds: Sequence[int], t_off: Optional[int] = None
) -> List[Dict[str, object]]:
    """Replicate at two alternative values of each fixed constant."""
    rows = [{"check": "constants", "constant": "default", "value": None,
             **summarise_cell(config, seeds, t_off)}]
    for name, values in CONSTANT_ALTERNATIVES.items():
        for value in values:
            variant = replace(
                config, constants=replace(config.constants, **{name: float(value)})
            )
            rows.append({
                "check": "constants", "constant": name, "value": float(value),
                "predicted_relaxation": (
                    float(-1.0 / np.log(1.0 - value)) if name == "sigma" and value > 0 else None
                ),
                **summarise_cell(variant, seeds, t_off),
            })
    return rows


# --------------------------------------------------------------------------- #
# 4. Update scheme (spec §12.3)
# --------------------------------------------------------------------------- #


def check_update_scheme(
    config: RunConfig, seeds: Sequence[int], t_off: Optional[int] = None
) -> List[Dict[str, object]]:
    """Synchronous against random-order asynchronous updating.

    Excluding repulsion from spec §7.2 means the period-2 oscillations that
    afflict synchronously updated repulsive models cannot arise here, so this is
    a check that the scheme is not doing hidden work rather than a repair.
    Asynchronous updating is a Python sweep and is perhaps 50x slower than the
    vectorised synchronous path, which is why it is an appendix check.
    """
    rows = []
    for order in (UpdateOrder.SYNCHRONOUS, UpdateOrder.ASYNCHRONOUS):
        variant = replace(config, update_order=order)
        rows.append({"check": "update_scheme", "update_order": order.value,
                     **summarise_cell(variant, seeds, t_off)})
    return rows


# --------------------------------------------------------------------------- #
# 5. Boundary pile-up (spec §14.2, artifact 1)
# --------------------------------------------------------------------------- #


def check_boundary_artifact(
    config: RunConfig,
    seeds: Sequence[int],
    t_off: Optional[int] = None,
    depths: Iterable[float] = (0.7, 0.9),
) -> List[Dict[str, object]]:
    """Hard clip against a soft tanh bound, with interior bimodality reported.

    Clipping accumulates mass at +/-1, which is indistinguishable from genuine
    polarization to a moment-based statistic. The check reports how often the
    clip binds, the bimodality coefficient with and without the boundary atoms,
    and the same quantities under a bound that never pins anyone.

    Crossed with depth, and that crossing is the point. tanh does not only remove
    the atoms; it contracts the interior, so a reached agent's realised
    displacement is tanh(b + alpha(1-b)) - b rather than alpha(1-b). Where the
    campaign's depth sits close to the tolerance boundary that contraction can
    push it back across, converting the population instead of dividing it -- so
    the check has to be run both near the gate and clear of it, or a shifted
    gate is indistinguishable from a broken mechanism.
    """
    rows = []
    for alpha in depths:
        for mode in (BoundMode.CLIP, BoundMode.TANH):
            variant = replace(
                config,
                bound_mode=mode,
                actor_d=replace(config.actor_d, alpha=float(alpha)),
            )
            rows.append({
                "check": "boundary_artifact",
                "bound_mode": mode.value,
                "alpha_d": float(alpha),
                "cell": f"{mode.value}, alpha={alpha:g}",
                "realised_displacement": float(np.tanh(alpha) if mode is BoundMode.TANH else alpha),
                **summarise_cell(variant, seeds, t_off),
            })
    return rows


# --------------------------------------------------------------------------- #
# 6. Counterfactual validity (spec §14.2, artifact 2)
# --------------------------------------------------------------------------- #


def check_counterfactual_validity(
    config: RunConfig, seeds: Sequence[int], n_replicates: int = 5
) -> List[Dict[str, object]]:
    """The step past which Pi and the handover time stop being reportable."""
    rows = []
    for seed in seeds:
        report = counterfactual_validity(replace(config, seed=seed), n_replicates)
        rows.append({
            "check": "counterfactual_validity",
            "seed": int(seed),
            "horizon": report["horizon"],
            "n_replicates": report["n_replicates"],
            "ratio": report["ratio"],
            "max_noise": report["max_noise"],
            "signal_at_end": float(report["signal"][-1]),
        })
    return rows
