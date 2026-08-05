#!/usr/bin/env python3
"""The appendix table of spec §12.3, plus the artifact checks of §14.2.

    python run_appendix.py [--seeds N] [--out DIR] [--only ...]

Six exercises on the headline settings, reported as one table rather than in the
main text:

  1. population size          N in {500, 1000, 2000}                    (§12.3)
  2. empirical network        one public graph, generators matched to it (§12.3)
  3. fixed constants          two alternative values of sigma, gamma, zeta (§3.2)
  4. update scheme            synchronous vs random-order asynchronous   (§12.3)
  5. boundary pile-up         hard clip vs soft tanh; interior bimodality (§14.2)
  6. counterfactual validity  the step past which Pi is not reportable   (§14.2)

Every cell is a distribution over seeds, and each seed costs the four runs of the
2x2 (spec §10.1). Writes `Results/data/appendix.json` and prints the table.

The empirical check is skipped with a message when no edge list is present; run
`python fetch_empirical_network.py --list` to see the options.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

from moralpanic import (
    Constants,
    NetworkSpec,
    Parameters,
    Repertoire,
    RunConfig,
    Topology,
    entrepreneur,
)
from moralpanic.appendix import (
    check_boundary_artifact,
    check_constants,
    check_counterfactual_validity,
    check_empirical_network,
    check_population_size,
    check_update_scheme,
)

# the headline setting, identical to run_hypotheses.py
T_OFF, T_LONG = 150, 400
HEADLINE = RunConfig(
    seed=11,
    n_steps=T_LONG,
    network=NetworkSpec(topology=Topology.SMALL_WORLD, n_agents=1000, mean_degree=10.0),
    parameters=Parameters(epsilon=0.5, mu=0.30, delta=0.25, omega=0.35),
    actor_d=entrepreneur(alpha=0.7, rho=0.25, repertoire=Repertoire.BASE, active_until=T_OFF),
    constants=Constants(sigma=0.0, gamma=3.0, zeta=0.01),
)

NETWORK_DIR = Path(__file__).resolve().parent / "networks"


def find_edge_lists() -> List[Path]:
    """Every edge list retrieved by `fetch_empirical_network.py`, if any."""
    if not NETWORK_DIR.exists():
        return []
    return sorted(p for p in NETWORK_DIR.iterdir() if p.suffix in (".txt", ".gz"))


def show(rows: List[Dict[str, object]], title: str, key: str) -> None:
    """Print one block of the appendix table."""
    print(f"\n{title}")
    print(f"  {'cell':<28} {'N':>5} {'<k>':>6} {'Pi(149)':>16} {'Pi(399)':>16} "
          f"{'BC':>6} {'BC int':>7} {'bdry':>6} {'handover':>9}")
    for row in rows:
        label = str(row.get(key, ""))
        boundary = row["boundary"]
        handover = row["handover"]
        print(f"  {label:<28} {row['n_agents']:>5} "
              f"{row['structure']['mean_degree']:>6.2f} "
              f"{row['panic_index_at']['mean']:>7.3f} ± {row['panic_index_at']['sd']:<6.3f} "
              f"{row['panic_index_end']['mean']:>7.3f} ± {row['panic_index_end']['sd']:<6.3f} "
              f"{boundary['bimodality']:>6.3f} {boundary['bimodality_interior']:>7.3f} "
              f"{boundary['boundary_fraction']:>6.3f} "
              f"{str(handover['median']):>4} {handover['reached']:>5}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--seeds", type=int, default=10)
    parser.add_argument("--async-seeds", type=int, default=3,
                        help="the asynchronous sweep is a Python loop and much slower")
    parser.add_argument("--out", default=str(Path(__file__).resolve().parents[1]
                                             / "Results" / "data"))
    parser.add_argument("--only", default="", help="size,empirical,constants,update,boundary,validity")
    args = parser.parse_args()

    seeds = list(range(11, 11 + args.seeds))
    wanted = {w.strip() for w in args.only.split(",") if w.strip()} or {
        "size", "empirical", "constants", "update", "boundary", "validity"
    }
    started = time.time()
    payload: Dict[str, object] = {
        "seeds": seeds,
        "headline": {
            "n_agents": HEADLINE.network.n_agents,
            "mean_degree": HEADLINE.network.mean_degree,
            "epsilon": HEADLINE.parameters.epsilon,
            "mu": HEADLINE.parameters.mu,
            "delta": HEADLINE.parameters.delta,
            "omega": HEADLINE.parameters.omega,
            "alpha_d": HEADLINE.actor_d.alpha,
            "rho_d": HEADLINE.actor_d.rho,
            "t_off": T_OFF,
            "n_steps": T_LONG,
        },
    }

    print(f"Appendix checks over {len(seeds)} seeds; four runs per seed (spec §10.1).\n")

    if "size" in wanted:
        rows = check_population_size(HEADLINE, seeds, t_off=T_OFF)
        payload["population_size"] = rows
        show(rows, "1. Population size (spec §12.3)", "n_agents")

    if "empirical" in wanted:
        edge_lists = find_edge_lists()
        if not edge_lists:
            print("\n2. Empirical network (spec §12.3): SKIPPED — no edge list present.")
            print("   python fetch_empirical_network.py --list      # see the options")
            print("   python fetch_empirical_network.py ego-facebook")
            payload["empirical_network"] = {"skipped": "no edge list in Code/networks/"}
        else:
            rows: List[Dict[str, object]] = []
            for path in edge_lists:
                rows += check_empirical_network(HEADLINE, seeds, str(path), t_off=T_OFF)
            payload["empirical_network"] = rows
            show(rows, "2. Empirical network, generators matched to it (spec §12.3)", "topology")
            for row in rows:
                print(f"     {row['source']:<26} {row['topology']:<15} "
                      f"C = {row['structure']['clustering']:.3f}, "
                      f"components = {int(row['structure']['n_components']):>4}, "
                      f"C3 subcritical = {row['c3']['subcritical']} "
                      f"(resting {row['c3']['resting_mean_alarm']:.4f})")

    if "constants" in wanted:
        rows = check_constants(HEADLINE, seeds, t_off=T_OFF)
        for row in rows:
            row["cell"] = f"{row['constant']}={row['value']}" if row["value"] is not None else "default"
        payload["constants"] = rows
        show(rows, "3. The fixed constants (spec §3.2, §12.3)", "cell")
        print("   sigma is the one that is not neutral: persistence should track "
              "-1/ln(1-sigma), not omega.")
        for row in rows:
            if row["constant"] == "sigma" and row["value"]:
                print(f"     sigma={row['value']:.2f}: predicted relaxation "
                      f"{row['predicted_relaxation']:.1f} steps, measured persistence "
                      f"{row['persistence']['median']:.0f} "
                      f"({row['persistence']['censored']} censored)")

    if "update" in wanted:
        async_seeds = seeds[: max(1, args.async_seeds)]
        print(f"\n   (asynchronous sweep over {len(async_seeds)} seeds; it is a Python loop)")
        rows = check_update_scheme(HEADLINE, async_seeds, t_off=T_OFF)
        payload["update_scheme"] = rows
        show(rows, "4. Update scheme (spec §12.3)", "update_order")

    if "boundary" in wanted:
        rows = check_boundary_artifact(HEADLINE, seeds, t_off=T_OFF)
        payload["boundary_artifact"] = rows
        show(rows, "5. Boundary pile-up (spec §14.2, artifact 1)", "cell")
        for row in rows:
            print(f"     {row['cell']:>18}: displacement at b=0 is "
                  f"{row['realised_displacement']:.3f} vs epsilon="
                  f"{HEADLINE.parameters.epsilon}; the clip bound on "
                  f"{100 * row['boundary']['clip_rate']:.2f}% of agent-steps")

    if "validity" in wanted:
        rows = check_counterfactual_validity(HEADLINE, seeds[:5])
        payload["counterfactual_validity"] = rows
        print("\n6. Counterfactual validity (spec §14.2, artifact 2)")
        print("   the step past which Pi and the handover time stop being reportable")
        for row in rows:
            horizon = row["horizon"]
            print(f"     seed {row['seed']}: horizon "
                  f"{horizon if horizon is not None else 'not reached in the run'}"
                  f"; largest within-arm noise s.d. {row['max_noise']:.2e} against a "
                  f"full-vs-null gap of {row['signal_at_end']:.4f}")

    # merge rather than overwrite, so `--only <block>` refreshes one block and
    # leaves the rest of the table standing
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    target = out / "appendix.json"
    if target.exists():
        existing = json.loads(target.read_text())
        existing.update(payload)
        payload = existing
    target.write_text(json.dumps(payload, indent=2, default=str))
    print(f"\nWrote {target} in {time.time() - started:.1f}s "
          f"(blocks present: {', '.join(k for k in payload if k not in ('seeds', 'headline'))})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
