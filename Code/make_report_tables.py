#!/usr/bin/env python3
"""Emit the tables of the three hypothesis reports, in Markdown, from the JSON.

    python make_report_tables.py [h1|h2|h3|appendix|all]

The reports in `../Results/` quote a lot of numbers. Typing them by hand is how a
report drifts from the data it claims to describe, so every table there is
produced here and pasted, and re-running this after a re-run is the check that
nothing has drifted. Reads `../Results/data/`; writes nothing.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np

DATA = Path(__file__).resolve().parents[1] / "Results" / "data"

TOPOLOGIES = ("watts_strogatz", "holme_kim", "erdos_renyi")
TOPOLOGY_NAMES = {
    "watts_strogatz": "Watts–Strogatz",
    "holme_kim": "Holme–Kim",
    "erdos_renyi": "Erdős–Rényi",
}
REPERTOIRES = ("random", "fixed_random", "hub", "base")


def load(name: str) -> Dict:
    return json.loads((DATA / name).read_text())


def block(store: Dict, name: str) -> List[Dict]:
    return [v for v in store.values() if v["label"]["block"] == name]


def pick(cells: List[Dict], **conditions) -> Dict:
    hits = [c for c in cells if all(c["label"].get(k) == v for k, v in conditions.items())]
    if len(hits) != 1:
        raise KeyError(f"{len(hits)} cells match {conditions}")
    return hits[0]


def stat(cell: Dict, key: str):
    values = np.array([s[key] for s in cell["seeds"]], dtype=float)
    return values.mean(), values.std(ddof=1)


def handover_label(hits: List, cell: Dict) -> str:
    """`median (n/total)`, or `never` when the criterion is not met in any seed."""
    if not hits:
        return "never"
    return f"{np.median(hits):.0f} ({len(hits)}/{len(cell['seeds'])})"


def curve(cell: Dict, key: str) -> np.ndarray:
    return np.array(cell["mean_curves"][key], dtype=float)


def repertoire_cells(h1: Dict, repertoire: str, topology: str) -> List[Dict]:
    source = block(h1, "A5") if repertoire == "fixed_random" else block(h1, "A1")
    return [
        c for c in source
        if c["label"]["topology"] == topology and c["label"]["repertoire"] == repertoire
    ]


def sweep(cells: List[Dict], axis: str, key: str):
    ordered = sorted(cells, key=lambda c: c["label"][axis])
    stats = [stat(c, key) for c in ordered]
    return ([c["label"][axis] for c in ordered],
            [m for m, _ in stats], [s for _, s in stats])


# --------------------------------------------------------------------------- #


def h1_tables() -> None:
    h1 = load("h1_ignition.json")
    meta = load("meta.json")
    n_seeds = len(meta["seeds"])
    print(f"\n## H1 tables ({n_seeds} seeds)\n")

    print("### Disproportion against reach, by repertoire (Watts–Strogatz)\n")
    reaches = sorted({c["label"]["rho_d"] for c in block(h1, "A1")})
    print("| $\\rho_D$ | " + " | ".join(f"`{r}`" for r in REPERTOIRES) + " |")
    print("|---" * (len(REPERTOIRES) + 1) + "|")
    for rho in reaches:
        row = [f"| {rho:.2f} "]
        for rep in REPERTOIRES:
            cell = pick(repertoire_cells(h1, rep, "watts_strogatz"), rho_d=rho)
            m, sd = stat(cell, "panic_index_at")
            row.append(f"| {m:.3f} ± {sd:.3f} ({m / rho:.2f}) ")
        print("".join(row) + "|")

    print("\n### Peak disproportion and low-reach amplification, by repertoire × topology\n")
    print("| Topology | degree s.d. | " + " | ".join(
        f"`{r}` peak $\\Pi$" for r in REPERTOIRES) + " |")
    print("|---" * (len(REPERTOIRES) + 2) + "|")
    degree_sd = {"watts_strogatz": "1.00", "holme_kim": "12.81", "erdos_renyi": "3.22"}
    for topology in TOPOLOGIES:
        row = [f"| {TOPOLOGY_NAMES[topology]} | {degree_sd[topology]} "]
        for rep in REPERTOIRES:
            _, means, _ = sweep(repertoire_cells(h1, rep, topology), "rho_d", "panic_index_at")
            xs, _, _ = sweep(repertoire_cells(h1, rep, topology), "rho_d", "panic_index_at")
            peak = int(np.argmax(means))
            row.append(f"| {means[peak]:.3f} at $\\rho={xs[peak]:.2f}$ ")
        print("".join(row) + "|")

    print("\n### The fixed-audience control (Watts–Strogatz, degree s.d. 1.00)\n")
    print("| $\\rho_D$ | `random` | `fixed_random` | `hub` | ratio fixed/random | ratio hub/fixed |")
    print("|---|---|---|---|---|---|")
    for rho in reaches:
        values = {
            rep: stat(pick(repertoire_cells(h1, rep, "watts_strogatz"), rho_d=rho),
                      "panic_index_at")[0]
            for rep in ("random", "fixed_random", "hub")
        }
        print(f"| {rho:.2f} | {values['random']:.3f} | {values['fixed_random']:.3f} | "
              f"{values['hub']:.3f} | {values['fixed_random'] / values['random']:.1f}× | "
              f"{values['hub'] / values['fixed_random']:.2f}× |")

    print("\n### Exposure concentration at $\\rho=0.10$\n")
    print("| Topology | " + " | ".join(f"`{r}`" for r in REPERTOIRES) + " |")
    print("|---" * (len(REPERTOIRES) + 1) + "|")
    for topology in TOPOLOGIES:
        row = [f"| {TOPOLOGY_NAMES[topology]} "]
        for rep in REPERTOIRES:
            cell = pick(repertoire_cells(h1, rep, topology), rho_d=0.10)
            row.append(f"| {stat(cell, 'exposure_concentration')[0]:,.0f} ")
        print("".join(row) + "|")

    print("\n### Depth against reach (`base`, Watts–Strogatz): $\\Pi$ / $\\bar b$\n")
    a2 = block(h1, "A2")
    alphas = sorted({c["label"]["alpha_d"] for c in a2})
    rhos = sorted({c["label"]["rho_d"] for c in a2})
    print("| $\\alpha_D$ \\\\ $\\rho_D$ | " + " | ".join(f"{r:g}" for r in rhos) + " |")
    print("|---" * (len(rhos) + 1) + "|")
    for alpha in alphas:
        row = [f"| {alpha:.1f} "]
        for rho in rhos:
            cell = pick(a2, alpha_d=alpha, rho_d=rho)
            row.append(f"| {stat(cell, 'panic_index_at')[0]:.3f} / "
                       f"{stat(cell, 'mean_position_at')[0]:+.2f} ")
        print("".join(row) + "|")

    print("\n### Interaction term against reach (Watts–Strogatz)\n")
    print("| repertoire | " + " | ".join(f"{r:g}" for r in reaches) + " |")
    print("|---" * (len(reaches) + 1) + "|")
    for rep in REPERTOIRES:
        _, means, _ = sweep(repertoire_cells(h1, rep, "watts_strogatz"), "rho_d",
                            "interaction_at")
        print(f"| `{rep}` | " + " | ".join(f"{m:.3f}" for m in means) + " |")

    print("\n### Threshold dispersion and initial position regime\n")
    a3, a4 = block(h1, "A3"), block(h1, "A4")
    print("| $\\rho_D$ | dispersed $\\theta$ | uniform $\\theta=0.5$ | consensual | polarized |")
    print("|---|---|---|---|---|")
    for rho in reaches:
        cells = [pick(a3, thresholds="dispersed", rho_d=rho),
                 pick(a3, thresholds="uniform", rho_d=rho),
                 pick(a4, positions="consensual", rho_d=rho),
                 pick(a4, positions="polarized", rho_d=rho)]
        print(f"| {rho:.2f} | " + " | ".join(
            f"{stat(c, 'panic_index_at')[0]:.3f} ± {stat(c, 'panic_index_at')[1]:.3f}"
            for c in cells) + " |")

    print("\n### Panic incidence over the criterion grid "
          f"(`base`, Watts–Strogatz, $W=10$; s.e. ≤ {0.5 / np.sqrt(n_seeds):.3f})\n")
    cuts = [(0.2, 0.2), (0.2, 0.3), (0.3, 0.2), (0.3, 0.3), (0.4, 0.3)]
    print("| $\\rho_D$ | " + " | ".join(
        f"$\\Pi^*={p}$, $q^*={q}$" for p, q in cuts) + " |")
    print("|---" * (len(cuts) + 1) + "|")
    for rho in reaches:
        cell = pick(repertoire_cells(h1, "base", "watts_strogatz"), rho_d=rho)
        print(f"| {rho:.2f} | " + " | ".join(
            f"{cell['incidence'][f'{p:.2f}_{q:.2f}_10']:.2f}" for p, q in cuts) + " |")


def h2_tables() -> None:
    h2 = load("h2_handover.json")
    sobol = load("h2_sobol.json")
    audit = load("h2_c3_audit.json")
    meta = load("meta.json")
    t_off = meta["t_off"]
    print(f"\n## H2 tables ({len(meta['seeds'])} seeds)\n")

    b1 = block(h2, "B1")[0]
    print("### The decomposition across withdrawal\n")
    print("| $t$ | warranted | claims-alone | othering-alone | interaction | $\\Pi$ | $q$ |")
    print("|---|---|---|---|---|---|---|")
    series = {k: curve(b1, k) for k in
              ("warranted", "claims_alone", "othering_alone", "interaction",
               "panic_index", "amplifying")}
    for t in (0, 1, 2, 5, 10, 20, t_off - 1, t_off + 5, 200, 300, len(series["panic_index"]) - 1):
        print(f"| {t} | " + " | ".join(
            f"{series[k][t]:.4f}" for k in
            ("warranted", "claims_alone", "othering_alone", "interaction", "panic_index",
             "amplifying")) + " |")
    ratio = series["interaction"][20] / series["claims_alone"][20]
    handovers = {s["handover_step"] for s in b1["seeds"]}
    censored = sum(s["persistence_censored"] for s in b1["seeds"])
    print(f"\ninteraction/claims at t=20: {ratio:.2f}x; handover steps observed: "
          f"{sorted(str(h) for h in handovers)}; persistence censored in "
          f"{censored}/{len(b1['seeds'])} seeds")
    print(f"Phi full vs othering-only at t={t_off-1}: "
          f"{curve(b1, 'mean_othering')[t_off-1]:.4f} vs "
          f"{curve(b1, 'mean_othering_only')[t_off-1]:.4f}")
    retained = series["panic_index"][-1] / series["panic_index"][t_off - 1]
    print(f"Pi retained at the end: {100*retained:.0f}% of its value at withdrawal")

    for name, axis, label in (("B2", "omega", "$\\omega$"), ("B3", "epsilon", "$\\epsilon$"),
                              ("B7", "alpha_d", "$\\alpha_D$")):
        cells = block(h2, name)
        if not cells:
            continue
        print(f"\n### Sweep in {label}\n")
        print(f"| {label} | $\\Pi(t_{{off}}-1)$ | $\\Pi(T-1)$ | interaction | "
              "handover (median, n) | persistence (median, censored) |")
        print("|---|---|---|---|---|---|")
        for cell in sorted(cells, key=lambda c: c["label"][axis]):
            hits = [s["handover_step"] for s in cell["seeds"] if s["handover_step"] is not None]
            durations = [s["persistence"] for s in cell["seeds"]]
            cens = sum(s["persistence_censored"] for s in cell["seeds"])
            print(f"| {cell['label'][axis]:.2f} "
                  f"| {stat(cell, 'panic_index_at')[0]:.3f} ± {stat(cell, 'panic_index_at')[1]:.3f} "
                  f"| {stat(cell, 'panic_index_end')[0]:.3f} ± {stat(cell, 'panic_index_end')[1]:.3f} "
                  f"| {stat(cell, 'interaction_at')[0]:.3f} "
                  f"| {handover_label(hits, cell)} "
                  f"| {np.median(durations):.0f} ({cens}/{len(cell['seeds'])}) |")

    print("\n### Initial position regime, and the anchor\n")
    print("| Cell | $\\Pi$ at withdrawal | interaction | othering-alone | handover | $\\bar\\Phi(0)$ |")
    print("|---|---|---|---|---|---|")
    for cell in block(h2, "B4"):
        hits = [s["handover_step"] for s in cell["seeds"] if s["handover_step"] is not None]
        print(f"| {cell['label']['positions']} "
              f"| {stat(cell, 'panic_index_at')[0]:.3f} "
              f"| {stat(cell, 'interaction_at')[0]:.3f} "
              f"| {stat(cell, 'othering_alone_at')[0]:.3f} "
              f"| {handover_label(hits, cell)} "
              f"| {stat(cell, 'mean_othering_0')[0]:.3f} |")
    print("\n| $\\sigma$ | predicted $-1/\\ln(1-\\sigma)$ | measured persistence | censored |")
    print("|---|---|---|---|")
    for cell in sorted(block(h2, "B5"), key=lambda c: c["label"]["sigma"]):
        sigma = cell["label"]["sigma"]
        predicted = "∞" if sigma == 0 else f"{-1 / np.log(1 - sigma):.1f}"
        durations = [s["persistence"] for s in cell["seeds"]]
        cens = sum(s["persistence_censored"] for s in cell["seeds"])
        print(f"| {sigma:.2f} | {predicted} | {np.median(durations):.0f} "
              f"| {cens}/{len(cell['seeds'])} |")

    print("\n### The simplex, with the C3 audit applied\n")
    sub = {(p["p_mu"], p["p_delta"], p["p_omega"]): p["subcritical"] for p in audit["points"]}
    rows = []
    for cell in block(h2, "B6"):
        key = (cell["label"]["p_mu"], cell["label"]["p_delta"], cell["label"]["p_omega"])
        rows.append((key, sub.get(key, True), stat(cell, "panic_index_end")[0],
                     stat(cell, "residual_ratio")[0]))
    supercritical = [r for r in rows if not r[1]]
    ok = sorted([r for r in rows if r[1]], key=lambda r: -r[2])
    print(f"{len(supercritical)} of {len(rows)} lattice points fail the measured C3 probe:")
    for key, _, pi, _ in supercritical:
        print(f"  - $(p_\\mu,p_\\delta,p_\\omega)$ = ({key[0]:.2f}, {key[1]:.2f}, {key[2]:.2f}), "
              f"$\\Pi(T-1)$ = {pi:.4f}")
    print("\n| $p_\\mu$ | $p_\\delta$ | $p_\\omega$ | $\\Pi(T-1)$ | residual ratio |")
    print("|---|---|---|---|---|")
    for key, _, pi, rr in ok[:5]:
        print(f"| {key[0]:.2f} | {key[1]:.2f} | **{key[2]:.2f}** | **{pi:.4f}** | {rr:.3f} |")
    print(f"\nargmax over sub-critical points: p_omega = {ok[0][0][2]:.2f}; "
          f"mean p_omega of the top five = {np.mean([r[0][2] for r in ok[:5]]):.3f}")

    print("\n### Variance-based sensitivity\n")
    print("| Output | reliable | " + " | ".join(
        f"$S_1({n})$ | $S_T({n})$" for n in sobol["input_names"]) + " |")
    print("|---" * (2 + 2 * len(sobol["input_names"])) + "|")
    for output, result in sobol["outputs"].items():
        cells = " | ".join(f"{result['S1'][i]:.3f} | {result['ST'][i]:.3f}"
                           for i in range(len(sobol["input_names"])))
        print(f"| {output} | {result.get('reliable')} | {cells} |")
    check = sobol["estimator_check"]
    print(f"\nIshigami check: max abs error {check['max_abs_error']:.4f}, "
          f"passed = {check.get('passed')}")


def h3_tables() -> None:
    h3 = load("h3_defense.json")
    meta = load("meta.json")
    t_off = meta["t_off"]
    order = ["none", "broad_shallow", "narrow_deep", "matched"]
    c1 = block(h3, "C1")
    print(f"\n## H3 tables ({len(meta['seeds'])} seeds)\n")

    traces = {name: {k: curve(pick(c1, configuration=name), k)
                     for k in ("panic_index", "mean_position", "mean_othering", "amplifying")}
              for name in order}

    print("### The panic index around $C$'s entry\n")
    print("| $t$ | " + " | ".join(order) + " |")
    print("|---" * (len(order) + 1) + "|")
    for t in (t_off - 1, t_off + 2, t_off + 5, t_off + 10, t_off + 15, t_off + 25, t_off + 50,
              200, len(traces["none"]["panic_index"]) - 1):
        print(f"| {t} | " + " | ".join(
            f"{traces[n]['panic_index'][t]:.3f}" for n in order) + " |")

    print("\n| Configuration | peak $\\Pi$ | max excess | steps above baseline | "
          "$\\Delta\\Pi$ at $T$ | $\\bar b$ at $T$ | $\\bar\\Phi$ at $T$ |")
    print("|---|---|---|---|---|---|---|")
    for name in order[1:]:
        pi = traces[name]["panic_index"][t_off:]
        excess = (traces[name]["panic_index"] - traces["none"]["panic_index"])[t_off:]
        peak = int(np.argmax(pi))
        worst = int(np.argmax(excess))
        print(f"| {name} | {pi[peak]:.3f} at $t={t_off + peak}$ | "
              f"**+{excess[worst]:.3f}** at $t={t_off + worst}$ | {int((excess > 0).sum())} | "
              f"{excess[-1]:+.3f} | {traces[name]['mean_position'][-1]:+.3f} | "
              f"{traces[name]['mean_othering'][-1]:.3f} |")

    print("\n### The two channels, isolated\n")
    c2 = block(h3, "C2")
    for axis, held in (("rho_c", "$\\alpha_C=0.50$"), ("alpha_c", "$\\rho_C=0.50$")):
        cells = sorted([c for c in c2 if c["label"]["axis"] == axis],
                       key=lambda c: c["label"]["value"])
        if not cells:
            continue
        print(f"\n| {axis} (at {held}) | " + " | ".join(
            f"{c['label']['value']:.2f}" for c in cells) + " |")
        print("|---" * (len(cells) + 1) + "|")
        print("| $\\Pi(T-1)$ | " + " | ".join(
            f"{stat(c, 'panic_index_end')[0]:.3f}" for c in cells) + " |")


def appendix_tables() -> None:
    payload = load("appendix.json")
    print("\n## Appendix tables\n")
    for name, rows in payload.items():
        if not isinstance(rows, list):
            continue
        print(f"\n### {name}\n")
        keys = [k for k in ("n_agents", "topology", "source", "constant", "value",
                            "bound_mode", "update_order", "cell", "alpha_d")
                if k in rows[0]]
        print("| " + " | ".join(keys) + " | $\\Pi$ at withdrawal | $\\Pi$ at $T$ | BC | "
              "BC interior | boundary | handover |")
        print("|---" * (len(keys) + 6) + "|")
        for row in rows:
            label = " | ".join(str(row[k]) for k in keys)
            b = row["boundary"]
            print(f"| {label} | {row['panic_index_at']['mean']:.3f} ± "
                  f"{row['panic_index_at']['sd']:.3f} | "
                  f"{row['panic_index_end']['mean']:.3f} ± {row['panic_index_end']['sd']:.3f} | "
                  f"{b['bimodality']:.3f} | {b['bimodality_interior']:.3f} | "
                  f"{b['boundary_fraction']:.3f} | {row['handover']['median']} "
                  f"({row['handover']['reached']}) |")


def main() -> int:
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("h1", "all"):
        h1_tables()
    if which in ("h2", "all"):
        h2_tables()
    if which in ("h3", "all"):
        h3_tables()
    if which in ("appendix", "all"):
        appendix_tables()
    return 0


if __name__ == "__main__":
    sys.exit(main())
