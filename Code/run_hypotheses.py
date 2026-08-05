#!/usr/bin/env python3
"""Run the three experiments of spec §12.1 and dump per-hypothesis results as JSON.

    python run_hypotheses.py [--quick] [--out DIR] [--seeds N]

Experiment A (H1, ignition), B (H2, handover) and C (H3, defense) are each run
over a list of seeds; every seed costs the four runs of the 2x2 counterfactual
set (spec §10.1), so nothing here is ever a single trajectory.

Output is one JSON file per hypothesis plus a `meta.json`, written to
`../Results/data/` by default. The notebook `../Results/hypothesis_figures.ipynb`
reads those files; nothing in the figures is computed twice.

The Sobol design, the estimators and their Ishigami validation live in
`moralpanic.sensitivity`; the appendix checks of spec §12.3 live in
`moralpanic.appendix` and are run by `run_appendix.py`.
"""

from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import sys
import time
from dataclasses import replace
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import numpy as np

from moralpanic import (
    Constants,
    ExposureMode,
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
    run_counterfactual_set,
)
from moralpanic.counterfactual import _first_sustained, is_subcritical
from moralpanic.sensitivity import (
    alarm_parameters,
    simplex_grid,
    sobol_design,
    sobol_indices,
    validate_sobol_estimator,
)

# --------------------------------------------------------------------------- #
# The operating point (README pilot, lifted to N = 1000)
# --------------------------------------------------------------------------- #

N_AGENTS = 1000
MEAN_DEGREE = 10.0
EPSILON = 0.5
MU, DELTA, OMEGA = 0.30, 0.25, 0.35
ALPHA_D = 0.7
RHO_D = 0.25
T_OFF = 150
T_LONG = 400
T_SHORT = 200

# the panic criterion is a convention, so results are reported over a grid of it
PI_STARS = (0.10, 0.20, 0.30, 0.40, 0.50)
Q_STARS = (0.10, 0.20, 0.30, 0.40, 0.50)
WINDOWS = (5, 10, 20)


# --------------------------------------------------------------------------- #
# Config construction and summarisation (top level, so workers can pickle them)
# --------------------------------------------------------------------------- #


def build_config(spec: Dict) -> RunConfig:
    """Build a RunConfig from a plain dict, so cells travel through a Pool."""
    t_off = spec.get("t_off")
    rho_c = spec.get("rho_c", 0.0)
    actor_c = (
        counter_entrepreneur(
            alpha=spec.get("alpha_c", 0.0),
            rho=rho_c,
            repertoire=Repertoire(spec.get("repertoire_c", "random")),
            active_from=spec.get("c_from", 0),
        )
        if rho_c > 0.0
        else SILENT_C
    )
    return RunConfig(
        seed=spec["seed"],
        n_steps=spec["n_steps"],
        network=NetworkSpec(
            topology=Topology(spec.get("topology", "watts_strogatz")),
            n_agents=spec.get("n_agents", N_AGENTS),
            mean_degree=spec.get("mean_degree", MEAN_DEGREE),
        ),
        parameters=Parameters(
            epsilon=spec.get("epsilon", EPSILON),
            mu=spec.get("mu", MU),
            delta=spec.get("delta", DELTA),
            omega=spec.get("omega", OMEGA),
        ),
        actor_d=entrepreneur(
            alpha=spec.get("alpha_d", ALPHA_D),
            rho=spec.get("rho_d", RHO_D),
            repertoire=Repertoire(spec.get("repertoire_d", "base")),
            active_until=t_off,
        ),
        actor_c=actor_c,
        constants=Constants(
            sigma=spec.get("sigma", 0.0),
            gamma=spec.get("gamma", 3.0),
            zeta=spec.get("zeta", 0.01),
        ),
        exposure_mode=ExposureMode(spec.get("exposure", "reinforcing")),
        position_regime=PositionRegime(spec.get("positions", "consensual")),
        threshold_regime=ThresholdRegime(spec.get("thresholds", "dispersed")),
    )


def panic_onset_grid(result) -> Dict[str, Optional[int]]:
    """Onset step under every (Pi*, q*, W) in the grid (spec §10.2).

    The criterion is a convention, not a finding, so the whole grid is reported
    and the reader can see how much the calm/panic boundary depends on the cut.
    """
    pi = result.decomposition.panic_index
    q = result.full.series("amplifying")
    out: Dict[str, Optional[int]] = {}
    for pi_star in PI_STARS:
        for q_star in Q_STARS:
            meets = (pi >= pi_star) & (q >= q_star)
            for window in WINDOWS:
                key = f"{pi_star:.2f}_{q_star:.2f}_{window}"
                onset = _first_sustained(meets, window)
                out[key] = None if onset is None else int(onset)
    return out


def summarise(result, spec: Dict, keep_curves: bool = False) -> Dict:
    """Reduce one 2x2 set to the scalars and (optionally) curves the figures need."""
    d = result.decomposition
    full = result.full
    n_steps = spec["n_steps"]
    t_off = spec.get("t_off")
    at = (t_off - 1) if t_off else (n_steps - 1)  # last step with D still active

    out: Dict = {
        "seed": spec["seed"],
        "at": at,
        "panic_index_at": float(d.panic_index[at]),
        "panic_index_end": float(d.panic_index[-1]),
        "warranted_at": float(d.warranted[at]),
        "claims_alone_at": float(d.claims_alone[at]),
        "othering_alone_at": float(d.othering_alone[at]),
        "interaction_at": float(d.interaction[at]),
        "interaction_end": float(d.interaction[-1]),
        "amplifying_at": float(full.series("amplifying")[at]),
        "amplifying_end": float(full.series("amplifying")[-1]),
        "mean_position_at": float(full.series("mean_position")[at]),
        "mean_position_end": float(full.series("mean_position")[-1]),
        "mean_othering_at": float(full.series("mean_othering")[at]),
        "mean_othering_0": float(full.series("mean_othering")[0]),
        "bimodality_at": float(full.series("bimodality")[at]),
        "bimodality_interior_at": float(full.series("bimodality_interior")[at]),
        "boundary_fraction_at": float(full.series("boundary_fraction")[at]),
        "alarm_assortativity_at": float(full.series("alarm_assortativity")[at]),
        "exposure_concentration": float(result.exposure_concentration()),
        "null_peak": float(result.null_peak()),
        "handover_step": result.handover_step(),
        "clip_events": float(full.structure.get("clip_events", 0.0)),
        "mean_degree": float(full.structure["mean_degree"]),
        "clustering": float(full.structure["clustering"]),
        "isolate_fraction": float(full.structure["isolate_fraction"]),
        "n_components": int(full.structure["n_components"]),
        "onsets": panic_onset_grid(result),
    }
    if t_off is not None:
        persistence = result.persistence(t_off)
        out["persistence"] = int(persistence["duration"])
        out["persistence_censored"] = bool(persistence["censored"])
        out["panic_index_t_off"] = float(d.panic_index[t_off])
        # a continuous surrogate for persistence, needed by the Sobol analysis
        out["residual_ratio"] = float(
            d.panic_index[-1] / d.panic_index[t_off] if d.panic_index[t_off] > 0 else 0.0
        )
    if keep_curves:
        out["curves"] = {
            "warranted": d.warranted.tolist(),
            "claims_alone": d.claims_alone.tolist(),
            "othering_alone": d.othering_alone.tolist(),
            "interaction": d.interaction.tolist(),
            "panic_index": d.panic_index.tolist(),
            "amplifying": full.series("amplifying").tolist(),
            "mean_position": full.series("mean_position").tolist(),
            "mean_othering": full.series("mean_othering").tolist(),
            "mean_othering_only": result.runs["othering"].series("mean_othering").tolist(),
            "bimodality": full.series("bimodality").tolist(),
        }
    return out


def _worker(job: Dict) -> Dict:
    """One 2x2 set. `job` carries the cell label and the config spec."""
    spec = job["spec"]
    result = run_counterfactual_set(build_config(spec))
    summary = summarise(result, spec, keep_curves=job.get("keep_curves", False))
    return {"cell": job["cell"], "summary": summary}


def run_jobs(jobs: List[Dict], processes: Optional[int] = None) -> List[Dict]:
    """Execute jobs over a process pool, reporting progress on one line."""
    if not jobs:
        return []
    processes = processes or max(1, (mp.cpu_count() or 2) - 1)
    started = time.time()
    done: List[Dict] = []
    with mp.Pool(processes) as pool:
        for index, item in enumerate(pool.imap_unordered(_worker, jobs, chunksize=4), 1):
            done.append(item)
            if index % 25 == 0 or index == len(jobs):
                elapsed = time.time() - started
                sys.stderr.write(
                    f"\r    {index}/{len(jobs)} sets, {elapsed:5.1f}s "
                    f"({elapsed / index:.2f}s each)   "
                )
                sys.stderr.flush()
    sys.stderr.write("\n")
    return done


def group(results: List[Dict]) -> Dict[str, Dict]:
    """Collect worker output into {cell_key: {label, seeds, incidence, mean_curves}}.

    Two things are reduced here rather than stored per seed, because at the seed
    counts spec §12.1 asks for the per-seed copies dominate the file and nothing
    reads them:

      * the onset grid becomes `incidence`, a frequency per (Pi*, q*, W) -- which
        is what §10.3 says to report anyway, panic being a rate and never a
        single run;
      * retained curves become `mean_curves`, the seed-mean of each series, which
        is the only form the figures use.
    """
    grouped: Dict[str, Dict] = {}
    for item in results:
        key = json.dumps(item["cell"], sort_keys=True)
        entry = grouped.setdefault(key, {"label": item["cell"], "seeds": []})
        entry["seeds"].append(item["summary"])

    for entry in grouped.values():
        entry["seeds"].sort(key=lambda s: s["seed"])
        seeds = entry["seeds"]
        entry["n_seeds"] = len(seeds)

        if seeds[0].get("onsets"):
            keys = seeds[0]["onsets"].keys()
            entry["incidence"] = {
                k: float(np.mean([s["onsets"][k] is not None for s in seeds])) for k in keys
            }
            entry["onset_median"] = {
                k: (float(np.median(hits)) if (hits := [s["onsets"][k] for s in seeds
                                                        if s["onsets"][k] is not None]) else None)
                for k in keys
            }
            for s in seeds:
                s.pop("onsets", None)

        if seeds[0].get("curves"):
            names = seeds[0]["curves"].keys()
            entry["mean_curves"] = {
                name: np.mean([s["curves"][name] for s in seeds], axis=0).tolist()
                for name in names
            }
            for s in seeds:
                s.pop("curves", None)
    return grouped


# --------------------------------------------------------------------------- #
# Experiment A -- Ignition (H1)
# --------------------------------------------------------------------------- #

REACHES = (0.02, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.70, 0.85, 1.00)
ALPHAS = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
GRID_REACHES = (0.05, 0.10, 0.20, 0.30, 0.50, 0.70, 1.00)


def experiment_a(seeds: Sequence[int], quick: bool) -> Dict:
    reaches = REACHES[::2] if quick else REACHES
    topologies = ("watts_strogatz", "holme_kim", "erdos_renyi")
    repertoires = ("random", "hub", "base")

    jobs: List[Dict] = []

    # A1: repertoire x topology x reach, consensual, dispersed thresholds
    for topology in topologies:
        for repertoire in repertoires:
            for rho in reaches:
                for seed in seeds:
                    cell = {
                        "block": "A1",
                        "topology": topology,
                        "repertoire": repertoire,
                        "rho_d": rho,
                    }
                    jobs.append(
                        {
                            "cell": cell,
                            "spec": {
                                "seed": seed,
                                "n_steps": T_SHORT,
                                "topology": topology,
                                "repertoire_d": repertoire,
                                "rho_d": rho,
                                "alpha_d": ALPHA_D,
                            },
                        }
                    )

    # A2: depth against reach (spec §12.1: does reach dominate depth?)
    grid_seeds = seeds[: max(1, len(seeds) // 2)]
    for alpha in (ALPHAS[::2] if quick else ALPHAS):
        for rho in GRID_REACHES:
            for seed in grid_seeds:
                cell = {"block": "A2", "alpha_d": alpha, "rho_d": rho}
                jobs.append(
                    {
                        "cell": cell,
                        "spec": {
                            "seed": seed,
                            "n_steps": T_SHORT,
                            "alpha_d": alpha,
                            "rho_d": rho,
                            "repertoire_d": "base",
                        },
                    }
                )

    # A5: the fixed-audience control (spec §7.1). `hub` differs from `random`
    # in two ways at once -- whom it selects, and that it selects the same people
    # every step. `fixed_random` holds the schedule fixed while removing the
    # selection rule, which is the only way to tell the two explanations apart.
    for topology in topologies:
        for rho in reaches:
            for seed in seeds:
                jobs.append(
                    {
                        "cell": {
                            "block": "A5",
                            "topology": topology,
                            "repertoire": "fixed_random",
                            "rho_d": rho,
                        },
                        "spec": {
                            "seed": seed,
                            "n_steps": T_SHORT,
                            "topology": topology,
                            "repertoire_d": "fixed_random",
                            "rho_d": rho,
                            "alpha_d": ALPHA_D,
                        },
                    }
                )

    # A3: threshold dispersion, and A4: initial position regime
    for rho in reaches:
        for seed in seeds:
            for thresholds in ("dispersed", "uniform"):
                jobs.append(
                    {
                        "cell": {"block": "A3", "thresholds": thresholds, "rho_d": rho},
                        "spec": {
                            "seed": seed,
                            "n_steps": T_SHORT,
                            "rho_d": rho,
                            "repertoire_d": "base",
                            "thresholds": thresholds,
                        },
                    }
                )
            for positions in ("consensual", "polarized"):
                jobs.append(
                    {
                        "cell": {"block": "A4", "positions": positions, "rho_d": rho},
                        "spec": {
                            "seed": seed,
                            "n_steps": T_SHORT,
                            "rho_d": rho,
                            "repertoire_d": "base",
                            "positions": positions,
                        },
                    }
                )

    print(f"  Experiment A: {len(jobs)} counterfactual sets")
    return group(run_jobs(jobs))


# --------------------------------------------------------------------------- #
# Experiment B -- Handover (H2)
# --------------------------------------------------------------------------- #

OMEGAS = (0.00, 0.10, 0.20, 0.30, 0.35, 0.45)
EPSILONS = (0.20, 0.30, 0.40, 0.50, 0.70, 1.00, 1.50, 2.00)
SIGMAS = (0.00, 0.05, 0.10, 0.20)


def experiment_b(seeds: Sequence[int], quick: bool) -> Dict:
    jobs: List[Dict] = []

    # B1: the headline decomposition across withdrawal, curves retained
    for seed in seeds:
        jobs.append(
            {
                "cell": {"block": "B1"},
                "keep_curves": True,
                "spec": {"seed": seed, "n_steps": T_LONG, "t_off": T_OFF},
            }
        )

    # B2: omega at fixed mu + delta
    for omega in OMEGAS:
        for seed in seeds:
            jobs.append(
                {
                    "cell": {"block": "B2", "omega": omega},
                    "spec": {
                        "seed": seed,
                        "n_steps": T_LONG,
                        "t_off": T_OFF,
                        "omega": omega,
                    },
                }
            )

    # B3: tolerance
    for epsilon in EPSILONS:
        for seed in seeds:
            jobs.append(
                {
                    "cell": {"block": "B3", "epsilon": epsilon},
                    "spec": {
                        "seed": seed,
                        "n_steps": T_LONG,
                        "t_off": T_OFF,
                        "epsilon": epsilon,
                    },
                }
            )

    # B4: initial position regime (H2's contrast)
    for positions in ("consensual", "polarized"):
        for seed in seeds:
            jobs.append(
                {
                    "cell": {"block": "B4", "positions": positions},
                    "keep_curves": True,
                    "spec": {
                        "seed": seed,
                        "n_steps": T_LONG,
                        "t_off": T_OFF,
                        "positions": positions,
                    },
                }
            )

    # B5: the anchor caution of spec §3.2 -- persistence must not track sigma
    for sigma in SIGMAS:
        for seed in seeds[: max(1, len(seeds) // 2)]:
            jobs.append(
                {
                    "cell": {"block": "B5", "sigma": sigma},
                    "spec": {
                        "seed": seed,
                        "n_steps": T_LONG,
                        "t_off": T_OFF,
                        "sigma": sigma,
                    },
                }
            )

    # B6: the simplex scan -- where on (p_mu, p_delta, p_omega) persistence peaks
    resolution = 6 if quick else 8
    total_intensity = 0.60  # keeps mu + delta below the measured C3 boundary (~0.7)
    simplex_seeds = seeds[: max(1, len(seeds) // 4)]
    for point in simplex_grid(resolution):
        p_mu, p_delta, p_omega = (float(v) for v in point)
        for seed in simplex_seeds:
            jobs.append(
                {
                    "cell": {
                        "block": "B6",
                        "p_mu": round(p_mu, 4),
                        "p_delta": round(p_delta, 4),
                        "p_omega": round(p_omega, 4),
                        "s": total_intensity,
                    },
                    "spec": {
                        "seed": seed,
                        "n_steps": T_LONG,
                        "t_off": T_OFF,
                        "mu": total_intensity * p_mu,
                        "delta": total_intensity * p_delta,
                        "omega": total_intensity * p_omega,
                    },
                }
            )

    # B7: does a GRADED handover exist anywhere? The handover is instantaneous
    # at alpha well above the tolerance gate and never happens below it, so if
    # H2's phase language survives anywhere it is in the narrow band between.
    for alpha in (0.55, 0.60, 0.62, 0.64, 0.66, 0.68, 0.70, 0.75):
        for seed in seeds:
            jobs.append(
                {
                    "cell": {"block": "B7", "alpha_d": alpha},
                    "spec": {
                        "seed": seed,
                        "n_steps": T_LONG,
                        "t_off": T_OFF,
                        "alpha_d": alpha,
                    },
                }
            )

    print(f"  Experiment B: {len(jobs)} counterfactual sets")
    return group(run_jobs(jobs))


# --------------------------------------------------------------------------- #
# Sobol analysis (spec §12.2), written out rather than imported from SALib
# --------------------------------------------------------------------------- #

S_MAX = 0.60
"""Upper bound on total alarm intensity in the Sobol box.

C1 (mu+delta+omega <= 1) holds identically under the reparameterisation, but C3
does not: at s near 1 and a small omega share, mu+delta approaches the measured
reinforcement boundary (~0.7 at mean degree 10, gamma 3) where alarm
self-sustains and H2 would be true for the wrong reason. The box is therefore
capped where every corner is still sub-critical, and the cap is reported.
"""


ZETA_MAX = 0.05
"""Upper bound on the noise input of the four-input design (spec §3.2).

Five times the default. Positions live in [-1, 1], so a per-step s.d. of 0.05
accumulates a random walk spanning the whole range inside one run -- large enough
that bounded confidence stops being absorbing and clusters re-merge. The box is
therefore generous to zeta by construction: it gives the constant every chance to
out-explain the split, which is the point of running it at all.
"""


def _sobol_worker(job: Dict) -> Dict:
    point = job["point"]
    s, u1, u2 = point[0], point[1], point[2]
    zeta = float(point[3]) if len(point) > 3 else 0.01
    parameters = alarm_parameters(s, u1, u2, EPSILON)
    spec = {
        "seed": job["seed"],
        "n_steps": T_LONG,
        "t_off": T_OFF,
        "mu": parameters.mu,
        "delta": parameters.delta,
        "omega": parameters.omega,
        "zeta": zeta,
    }
    result = run_counterfactual_set(build_config(spec))
    d = result.decomposition
    handover = result.handover_step()
    return {
        "index": job["index"],
        "matrix": job["matrix"],
        "residual_ratio": float(
            d.panic_index[-1] / d.panic_index[T_OFF] if d.panic_index[T_OFF] > 0 else 0.0
        ),
        "panic_index_end": float(d.panic_index[-1]),
        "handover_step": float(handover if handover is not None else T_LONG),
        "mu": parameters.mu,
        "delta": parameters.delta,
        "omega": parameters.omega,
    }


def experiment_sobol(
    n_base: int, seed: int = 11, include_zeta: bool = False, zeta_max: float = ZETA_MAX
) -> Dict:
    """Variance-based sensitivity on the (s, u1, u2) reparameterisation (spec §12.2).

    The model is deterministic given a seed, so one fixed seed is used across
    the design and the indices describe the parameter map rather than the noise.
    """
    bounds = (S_MAX, 1.0, 1.0, zeta_max) if include_zeta else (S_MAX, 1.0, 1.0)
    k = len(bounds)
    matrix_a, matrix_b, matrix_ab = sobol_design(n_base, bounds=bounds)

    jobs: List[Dict] = []
    for i in range(n_base):
        jobs.append({"index": i, "matrix": "A", "point": matrix_a[i], "seed": seed})
        jobs.append({"index": i, "matrix": "B", "point": matrix_b[i], "seed": seed})
        for column in range(k):
            jobs.append(
                {"index": i, "matrix": f"AB{column}", "point": matrix_ab[column][i],
                 "seed": seed}
            )

    print(f"  Sobol: {len(jobs)} counterfactual sets (N = {n_base}, k = {k})")
    processes = max(1, (mp.cpu_count() or 2) - 1)
    started = time.time()
    raw: List[Dict] = []
    with mp.Pool(processes) as pool:
        for count, item in enumerate(pool.imap_unordered(_sobol_worker, jobs, chunksize=4), 1):
            raw.append(item)
            if count % 25 == 0 or count == len(jobs):
                sys.stderr.write(f"\r    {count}/{len(jobs)} sets, {time.time()-started:5.1f}s   ")
                sys.stderr.flush()
    sys.stderr.write("\n")

    outputs = {}
    for name in ("residual_ratio", "panic_index_end", "handover_step"):
        table = {m: np.zeros(n_base) for m in ["A", "B"] + [f"AB{c}" for c in range(k)]}
        for item in raw:
            table[item["matrix"]][item["index"]] = item[name]
        f_ab = np.array([table[f"AB{c}"] for c in range(k)])
        outputs[name] = sobol_indices(table["A"], table["B"], f_ab)

    subcritical = sum(1 for item in raw if item["mu"] + item["delta"] < 0.7)
    return {
        "n_base": n_base,
        "s_max": S_MAX,
        "zeta_max": zeta_max if include_zeta else None,
        "input_names": ["s", "u1", "u2"] + (["zeta"] if include_zeta else []),
        "note": (
            "u1 and u2 are the two uniforms generating the split "
            "(p_mu, p_delta, p_omega); s is the total alarm intensity. "
            "Indices of u1 and u2 together are the split's share."
        ),
        "subcritical_fraction": subcritical / len(raw),
        "outputs": outputs,
    }


def _c3_worker(job: Dict) -> Dict:
    """The measured C3 probe (spec §3.3) at one point of the alarm simplex."""
    spec = job["spec"]
    probe = is_subcritical(build_config(spec))
    return {
        **job["cell"],
        "mu": spec["mu"],
        "delta": spec["delta"],
        "omega": spec["omega"],
        "subcritical": bool(probe["subcritical"]),
        "resting_mean_alarm": float(probe["resting_mean_alarm"]),
        "mu_plus_delta": float(probe["mu_plus_delta"]),
    }


def experiment_c3_audit(seed: int, quick: bool) -> Dict:
    """Which points of the simplex scan are C3-subcritical? (spec §3.3)

    mu + delta is only a proxy for the reinforcement boundary: the gain also
    depends on how the mass is split, because an amplifying neighbour enters
    with weight gamma. At the delta vertex, delta*gamma alone exceeds one, so a
    point with a perfectly respectable mu + delta can still self-sustain. The
    boundary therefore has to be measured at every point that gets reported.
    """
    jobs: List[Dict] = []
    resolution = 6 if quick else 8
    for total_intensity in (0.60,):
        for point in simplex_grid(resolution):
            p_mu, p_delta, p_omega = (float(v) for v in point)
            jobs.append(
                {
                    "cell": {
                        "p_mu": round(p_mu, 4),
                        "p_delta": round(p_delta, 4),
                        "p_omega": round(p_omega, 4),
                        "s": total_intensity,
                    },
                    "spec": {
                        "seed": seed,
                        "n_steps": T_LONG,
                        "mu": total_intensity * p_mu,
                        "delta": total_intensity * p_delta,
                        "omega": total_intensity * p_omega,
                    },
                }
            )
    print(f"  C3 audit: {len(jobs)} probes")
    with mp.Pool(max(1, (mp.cpu_count() or 2) - 1)) as pool:
        rows = pool.map(_c3_worker, jobs)
    return {"points": rows}


def validate_sobol_estimator(n_base: int = 4096) -> Dict:
    """Dock the hand-written estimator against Ishigami, whose indices are known.

    Analytic values at a = 7, b = 0.1: S1 = (0.3139, 0.4424, 0), ST = (0.5576,
    0.4424, 0.2437). This is verification of the estimator, not of the model,
    and is reported as such.
    """
    from scipy.stats import qmc

    def ishigami(x: np.ndarray) -> np.ndarray:
        a, b = 7.0, 0.1
        return (
            np.sin(x[:, 0]) + a * np.sin(x[:, 1]) ** 2 + b * x[:, 2] ** 4 * np.sin(x[:, 0])
        )

    k = 3
    sample = qmc.Sobol(d=2 * k, scramble=True, seed=7).random(n_base)
    matrix_a = sample[:, :k] * 2 * np.pi - np.pi
    matrix_b = sample[:, k:] * 2 * np.pi - np.pi
    f_a, f_b = ishigami(matrix_a), ishigami(matrix_b)
    f_ab = []
    for column in range(k):
        point = matrix_a.copy()
        point[:, column] = matrix_b[:, column]
        f_ab.append(ishigami(point))
    estimated = sobol_indices(f_a, f_b, np.array(f_ab))
    return {
        "n_base": n_base,
        "estimated": {"S1": estimated["S1"], "ST": estimated["ST"]},
        "analytic": {
            "S1": [0.3139, 0.4424, 0.0],
            "ST": [0.5576, 0.4424, 0.2437],
        },
        "max_abs_error": float(
            max(
                max(abs(e - a) for e, a in zip(estimated["S1"], [0.3139, 0.4424, 0.0])),
                max(abs(e - a) for e, a in zip(estimated["ST"], [0.5576, 0.4424, 0.2437])),
            )
        ),
    }


# --------------------------------------------------------------------------- #
# Experiment C -- Counter-claims-making (H3)
# --------------------------------------------------------------------------- #

COUNTER_CONFIGS = {
    "none": {"alpha_c": 0.0, "rho_c": 0.0},
    "broad_shallow": {"alpha_c": 0.15, "rho_c": 0.60},
    "narrow_deep": {"alpha_c": 0.90, "rho_c": 0.10},
    "matched": {"alpha_c": ALPHA_D, "rho_c": RHO_D},
}


def experiment_c(seeds: Sequence[int], quick: bool) -> Dict:
    jobs: List[Dict] = []
    for name, override in COUNTER_CONFIGS.items():
        for seed in seeds:
            spec = {
                "seed": seed,
                "n_steps": T_LONG,
                "t_off": T_OFF,
                "c_from": T_OFF,
                "repertoire_c": "random",
                **override,
            }
            jobs.append(
                {
                    "cell": {"block": "C1", "configuration": name, **override},
                    "keep_curves": True,
                    "spec": spec,
                }
            )

    # C2: a supplementary one-at-a-time probe, to read the sign of each channel
    # separately (spec §13: immediate cost scales with rho_C, delayed benefit
    # with alpha_C). Three points answer H3; this only says which channel moved.
    probe_seeds = seeds[: max(1, len(seeds) // 2)]
    if not quick:
        for rho_c in (0.10, 0.25, 0.50, 0.75, 1.00):
            for seed in probe_seeds:
                jobs.append(
                    {
                        "cell": {"block": "C2", "axis": "rho_c", "value": rho_c},
                        "spec": {
                            "seed": seed,
                            "n_steps": T_LONG,
                            "t_off": T_OFF,
                            "c_from": T_OFF,
                            "alpha_c": 0.50,
                            "rho_c": rho_c,
                        },
                    }
                )
        for alpha_c in (0.10, 0.30, 0.50, 0.70, 0.90):
            for seed in probe_seeds:
                jobs.append(
                    {
                        "cell": {"block": "C2", "axis": "alpha_c", "value": alpha_c},
                        "spec": {
                            "seed": seed,
                            "n_steps": T_LONG,
                            "t_off": T_OFF,
                            "c_from": T_OFF,
                            "alpha_c": alpha_c,
                            "rho_c": 0.50,
                        },
                    }
                )

    print(f"  Experiment C: {len(jobs)} counterfactual sets")
    return group(run_jobs(jobs))


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(Path(__file__).resolve().parents[1] / "Results" / "data"))
    parser.add_argument("--seeds", type=int, default=250)
    parser.add_argument("--sobol-n", type=int, default=256)
    parser.add_argument("--zeta-max-narrow", type=float, default=0.02,
                        help="second, narrower box for the four-input design (spec §3.2)")
    parser.add_argument("--quick", action="store_true", help="coarser grids, for a smoke test")
    parser.add_argument("--only", default="", help="comma-separated: a,b,c,sobol,c3")
    args = parser.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    seeds = list(range(11, 11 + args.seeds))
    wanted = {w.strip() for w in args.only.split(",") if w.strip()} or {
        "a", "b", "c", "sobol", "sobolz", "c3",
    }

    started = time.time()
    print(f"Running over {len(seeds)} seeds; four runs per seed (spec §10.1).")
    print(f"Operating point: N={N_AGENTS}, <k>={MEAN_DEGREE}, epsilon={EPSILON}, "
          f"mu={MU}, delta={DELTA}, omega={OMEGA}, alpha_D={ALPHA_D}, t_off={T_OFF}.\n")

    # the C3 sub-criticality probe at the operating point (spec §3.3)
    probe = is_subcritical(build_config({"seed": seeds[0], "n_steps": T_LONG}))
    meta = {
        "seeds": seeds,
        "n_agents": N_AGENTS,
        "mean_degree": MEAN_DEGREE,
        "epsilon": EPSILON,
        "mu": MU,
        "delta": DELTA,
        "omega": OMEGA,
        "alpha_d": ALPHA_D,
        "rho_d": RHO_D,
        "t_off": T_OFF,
        "n_steps_long": T_LONG,
        "n_steps_short": T_SHORT,
        "pi_stars": list(PI_STARS),
        "q_stars": list(Q_STARS),
        "windows": list(WINDOWS),
        "c3_probe": {k: (float(v) if isinstance(v, (int, float)) else v) for k, v in probe.items()},
        "quick": args.quick,
    }
    (out / "meta.json").write_text(json.dumps(meta, indent=2))
    print(f"  C3 probe at the operating point: subcritical={probe['subcritical']}, "
          f"resting mean alarm {probe['resting_mean_alarm']:.4f}\n")

    if "a" in wanted:
        (out / "h1_ignition.json").write_text(json.dumps(experiment_a(seeds, args.quick)))
    if "b" in wanted:
        (out / "h2_handover.json").write_text(json.dumps(experiment_b(seeds, args.quick)))
    if "sobol" in wanted:
        n_base = 32 if args.quick else args.sobol_n
        payload = experiment_sobol(n_base)
        payload["estimator_check"] = validate_sobol_estimator()  # Ishigami, spec §12.2
        (out / "h2_sobol.json").write_text(json.dumps(payload, indent=2))
    if "sobolz" in wanted:
        # the four-input design of spec §3.2: does the noise constant compete
        # with the alarm split to explain persistence?
        n_base = 32 if args.quick else args.sobol_n
        for zeta_max in (ZETA_MAX, args.zeta_max_narrow):
            payload = experiment_sobol(n_base, include_zeta=True, zeta_max=zeta_max)
            payload["estimator_check"] = validate_sobol_estimator()
            tag = "" if zeta_max == ZETA_MAX else f"_{zeta_max:g}".replace(".", "p")
            (out / f"h2_sobol_zeta{tag}.json").write_text(json.dumps(payload, indent=2))
    if "c3" in wanted:
        (out / "h2_c3_audit.json").write_text(
            json.dumps(experiment_c3_audit(seeds[0], args.quick), indent=2)
        )
    if "c" in wanted:
        (out / "h3_defense.json").write_text(json.dumps(experiment_c(seeds, args.quick)))

    print(f"\nWrote {out} in {time.time() - started:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
