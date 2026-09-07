#!/usr/bin/env python3
"""Slide-ready figures for the moral-panic talk.

Two families, written as separate files so a slide can carry exactly one idea:

  panels/   the twelve panels of the three paper figures (Results/figures/fig1-3),
            cut apart and restyled for projection, each with its finding as a title
  concepts/ nine expository figures for the parts of the argument the panels
            assume: the counterfactual design, the bounded-confidence asymmetry,
            the apportionment, the exposure schedule, and the population itself

Everything in `panels/` is drawn from `Results/data/*.json`, the same aggregates
behind the paper figures, so the numbers on a slide and the numbers in the text
cannot drift apart. Two of the concept figures re-run the model live at N = 300;
they take about a second and are fully seeded.

Usage
-----
    python3 make_presentation_figures.py                  # everything, PDF + PNG
    python3 make_presentation_figures.py --only concepts
    python3 make_presentation_figures.py --mono           # greyscale, for print
    python3 make_presentation_figures.py --out ../Presentation/figures

Colours follow a validated categorical palette (blue / orange / aqua, with grey
reserved for baselines): every pair clears the colour-vision separation floor,
and every series also carries a distinct dash and marker, so the set survives
greyscale printing and a bad projector alike.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

# --------------------------------------------------------------------------- #
# Palette and theme
# --------------------------------------------------------------------------- #

INK = "#1a1a19"        # primary text
SECOND = "#52514e"     # secondary text
MUTED = "#8a8a8a"      # captions, grid ink
REF = "#6b6b68"        # the baseline / null series: grey by role, not by accident
BLUE = "#2a78d6"
ORANGE = "#eb6834"
AQUA = "#1baf7a"
SURFACE = "#ffffff"

SEQ = LinearSegmentedColormap.from_list("seq_blue", [
    "#f4f8fe", "#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b",
])

MONO = False           # set by --mono
TITLES = True          # False for the deck-ready copies under untitled/


def grey(hexcolour: str) -> str:
    """Greyscale stand-in, used when --mono is on."""
    table = {BLUE: "#111111", ORANGE: "#444444", AQUA: "#7a7a7a", REF: "#a5a5a5"}
    return table.get(hexcolour, hexcolour)


def C(hexcolour: str) -> str:
    return grey(hexcolour) if MONO else hexcolour


def apply_theme() -> None:
    matplotlib.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
        "font.family": ["PT Sans", "Helvetica Neue", "Arial", "DejaVu Sans"],
        "font.size": 12,
        "axes.edgecolor": "#c9c9c6", "axes.linewidth": 0.9,
        "axes.grid": True, "grid.color": "#ececea", "grid.linewidth": 0.8,
        "axes.axisbelow": True,
        "xtick.color": SECOND, "ytick.color": SECOND,
        "xtick.labelsize": 11, "ytick.labelsize": 11,
        "text.color": INK, "axes.labelcolor": SECOND, "axes.labelsize": 11.5,
        "legend.fontsize": 10.5,
        "figure.dpi": 110, "savefig.dpi": 300, "savefig.bbox": "tight",
        "pdf.fonttype": 42, "ps.fonttype": 42, "pdf.compression": 6,
    })


# --------------------------------------------------------------------------- #
# Data
# --------------------------------------------------------------------------- #

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"

REQUIRED = ["meta.json", "h1_ignition.json", "h2_handover.json",
            "h2_sobol.json", "h2_c3_audit.json", "h3_defense.json"]


def load_store():
    missing = [n for n in REQUIRED if not (DATA / n).exists()]
    if missing:
        sys.exit(f"Results/data/ is missing {', '.join(missing)}.\n"
                 "Run  cd ../Code && python run_hypotheses.py --seeds 250  first "
                 "(--seeds 20 gives a four-minute pilot).")
    read = lambda name: json.loads((DATA / name).read_text())
    return (read("h1_ignition.json"), read("h2_handover.json"), read("h3_defense.json"),
            read("h2_sobol.json"), read("h2_c3_audit.json"), read("meta.json"))


H1, H2, H3, SOBOL, C3, META = {}, {}, {}, {}, {}, {}
T_OFF = 150


def block(store, name):
    return [v for v in store.values() if v["label"]["block"] == name]


def pick(cells, **conditions):
    hits = [c for c in cells if all(c["label"].get(k) == v for k, v in conditions.items())]
    if len(hits) != 1:
        raise KeyError(f"{len(hits)} cells match {conditions}")
    return hits[0]


def scalar(cell, key):
    values = np.array([s[key] for s in cell["seeds"]], dtype=float)
    return values.mean(), values.std(ddof=1)


def curve(cell, key):
    return np.array(cell["mean_curves"][key], dtype=float)


def sweep(cells, axis, key):
    ordered = sorted(cells, key=lambda c: c["label"][axis])
    stats = [scalar(c, key) for c in ordered]
    return (np.array([c["label"][axis] for c in ordered]),
            np.array([m for m, _ in stats]), np.array([s for _, s in stats]))


# --------------------------------------------------------------------------- #
# Drawing helpers
# --------------------------------------------------------------------------- #

OUT = Path()
FORMATS = ("pdf", "png")
WRITTEN = []


def canvas(width=8.6, height=4.5):
    fig, ax = plt.subplots(figsize=(width, height))
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    return fig, ax


def headline(fig, title, subtitle=None, ax=None, y=0.985):
    """One plain-language claim above the plot, one line of quiet detail below it.

    Anchored to the axes of a real chart, so the gap above the plot does not
    depend on the figure's height; anchored to the figure for the schematics,
    which switch their axes off and place their own content by hand.
    """
    if ax is None and fig.axes and fig.axes[0].axison:
        ax = fig.axes[0]
    if ax is not None:
        if TITLES:
            ax.text(0.0, 1.155 if subtitle else 1.07, title, transform=ax.transAxes,
                    ha="left", va="bottom", fontsize=14.5, fontweight="bold", color=INK)
        if subtitle:
            ax.text(0.0, 1.075 if TITLES else 1.035, subtitle, transform=ax.transAxes,
                    ha="left", va="bottom", fontsize=10.5, color=MUTED)
        return
    if TITLES:
        fig.text(0.0, y, title, ha="left", va="top", fontsize=14.5,
                 fontweight="bold", color=INK)
    if subtitle:
        fig.text(0.0, y - (0.075 if TITLES else 0.0), subtitle, ha="left", va="top",
                 fontsize=10.5, color=MUTED)


def footnote(fig, text, y=-0.055):
    fig.text(0.0, y, text, ha="left", va="top", fontsize=9, color=MUTED)


def save(fig, folder, name):
    target = OUT / folder
    target.mkdir(parents=True, exist_ok=True)
    for extension in FORMATS:
        path = target / f"{name}.{extension}"
        fig.savefig(path, bbox_inches="tight", facecolor=SURFACE)
        WRITTEN.append(path)
    plt.close(fig)


def legend(ax, **kwargs):
    options = dict(frameon=False, fontsize=10.5, labelcolor=SECOND,
                   handlelength=2.6, borderpad=0.2)
    options.update(kwargs)
    return ax.legend(**options)


# --------------------------------------------------------------------------- #
# Shared vocabulary of the result panels
# --------------------------------------------------------------------------- #

X_REACH = "reach   " + r"$\rho_D$" + "   (share of the population per step)"
Y_PANIC = "panic index   " + r"$\Pi$" + "   at $t = 199$"

# repertoire -> colour, dash, marker, label. `random` is grey by role: it is the
# benchmark the other three are read against, and it never amplifies.
REP_STYLE = {
    "random":       (REF,    (0, (1.4, 1.6)),        "^", "`random` — fresh audience each step"),
    "fixed_random": (AQUA,   (0, (4, 1.4, 1, 1.4)),  "D", "`fixed_random` — control"),
    "hub":          (ORANGE, (0, (5, 1.6)),          "s", "`hub` — highest degree"),
    "base":         (BLUE,   "solid",                "o", "`base` — nearest the actor's pole"),
}

TOPO_STYLE = {
    "holme_kim":      (ORANGE, "solid",         "s", "hub-dominated (Holme–Kim)"),
    "watts_strogatz": (BLUE,   (0, (5, 1.6)),   "o", "small world (Watts–Strogatz)"),
    "erdos_renyi":    (AQUA,   (0, (1.4, 1.6)), "^", "unstructured (Erdős–Rényi)"),
}

DEFENSE_STYLE = [
    ("none",          REF,    (0, (1.4, 1.6)),       "undefended baseline"),
    ("broad_shallow", AQUA,   (0, (5, 1.6)),         "broad & shallow"),
    ("narrow_deep",   ORANGE, "solid",               "narrow & deep"),
    ("matched",       BLUE,   (0, (4, 1.4, 1, 1.4)), "matched"),
]
DEFENSE_DETAIL = {"none": "", "broad_shallow": r"  $(\alpha_C,\rho_C)=(0.15,\,0.60)$",
                  "narrow_deep": r"  $(0.90,\,0.10)$", "matched": r"  $(0.70,\,0.25)$"}


def repertoire_cells(repertoire, topology="watts_strogatz"):
    """Block A5 holds `fixed_random`; block A1 holds the other three."""
    source = block(H1, "A5") if repertoire == "fixed_random" else block(H1, "A1")
    return [c for c in source
            if c["label"]["topology"] == topology and c["label"]["repertoire"] == repertoire]


def seed_note():
    return (f"Mean over {len(META['seeds'])} seeds, four runs per seed. Small world, "
            r"$N=1000$, $\langle k\rangle=10$.")


# --------------------------------------------------------------------------- #
# H1 — ignition
# --------------------------------------------------------------------------- #

def panel_h1a():
    fig, ax = canvas()
    ax.plot([0, 1], [0, 1], color=MUTED, lw=1.0, ls=(0, (4, 3)), zorder=1)
    ax.text(0.615, 0.585, r"$\Pi = \rho_D$", fontsize=10.5, color=MUTED)
    for rep, (colour, dash, marker, label) in REP_STYLE.items():
        x, m, s = sweep(repertoire_cells(rep), "rho_d", "panic_index_at")
        ax.plot(x, m, color=C(colour), linestyle=dash, marker=marker, ms=5.6,
                lw=2.0, label=label, zorder=3)
        ax.fill_between(x, m - s, m + s, color=C(colour), alpha=0.13, lw=0, zorder=2)
    ax.annotate("the control tracks `base`: what amplifies is\nthe exposure schedule, not the selection rule",
                xy=(0.52, 0.437), xytext=(0.42, 0.175), fontsize=10, color=INK, ha="left",
                arrowprops=dict(arrowstyle="->", lw=0.9, color=SECOND))
    ax.set_xlim(0, 1.02); ax.set_ylim(0, 0.64)
    ax.set_xlabel(X_REACH); ax.set_ylabel(Y_PANIC)
    legend(ax, loc="upper left", bbox_to_anchor=(0.01, 1.0))
    headline(fig, "Amplification requires a stable audience",
             "Panic index against reach, by targeting repertoire, on the small world")
    footnote(fig, seed_note() + r"  Bands are $\pm 1$ s.d. across seeds.")
    save(fig, "panels", "h1a_reach")


def panel_h1b():
    fig, ax = canvas()
    for topo, (colour, dash, marker, label) in TOPO_STYLE.items():
        cells = [c for c in block(H1, "A1")
                 if c["label"]["topology"] == topo and c["label"]["repertoire"] == "hub"]
        x, m, _ = sweep(cells, "rho_d", "panic_index_at")
        ax.plot(x, m, color=C(colour), linestyle=dash, marker=marker, ms=5.6,
                lw=2.0, label=label, zorder=3)
    x, m, _ = sweep(repertoire_cells("random"), "rho_d", "panic_index_at")
    ax.plot(x, m, color=C(REF), lw=1.2, ls=(0, (1, 2.2)), zorder=2)
    ax.annotate("`random`, for reference:\nno amplification on any topology",
                xy=(0.80, 0.145), xytext=(0.30, 0.030), fontsize=10, color=MUTED,
                arrowprops=dict(arrowstyle="->", lw=0.9, color=MUTED))
    ax.set_xlim(0, 1.02); ax.set_ylim(0, 0.64)
    ax.set_xlabel(X_REACH); ax.set_ylabel(Y_PANIC)
    legend(ax, loc="upper right")
    headline(fig, "Topology moves `hub` and almost nothing else",
             "Panic index for the `hub` repertoire across the three network generators")
    footnote(fig, seed_note())
    save(fig, "panels", "h1b_topology")


def panel_h1c():
    fig, ax = canvas()
    for rep, (colour, dash, marker, label) in REP_STYLE.items():
        x, m, _ = sweep(repertoire_cells(rep), "rho_d", "interaction_at")
        ax.plot(x, m, color=C(colour), linestyle=dash, marker=marker, ms=5.6,
                lw=2.0, label=label, zorder=3)
        peak = int(np.argmax(m))
        if m[peak] > 0.05:
            ax.plot(x[peak], m[peak], marker="o", ms=13, mfc="none",
                    mec=C(colour), mew=1.4, zorder=4)
    ax.axhline(0, color=SECOND, lw=1.0)
    ax.annotate("at $\\rho_D = 1$ exposure is uniform\nacross the population, so no\ndivision is manufactured",
                xy=(1.0, 0.006), xytext=(0.44, 0.105), fontsize=10, color=INK,
                arrowprops=dict(arrowstyle="->", lw=0.9, color=SECOND))
    ax.set_xlim(0, 1.02); ax.set_ylim(-0.02, 0.44)
    ax.set_xlabel(X_REACH)
    ax.set_ylabel("interaction term   at $t = 199$")
    legend(ax, loc="upper right")
    headline(fig, "Manufactured division peaks at intermediate reach",
             "The interaction term: alarm that neither mechanism produces on its own")
    footnote(fig, seed_note())
    save(fig, "panels", "h1c_interaction")


def panel_h1d():
    fig, ax = plt.subplots(figsize=(8.8, 4.9))
    cells = block(H1, "A2")
    alphas = sorted({c["label"]["alpha_d"] for c in cells})
    rhos = sorted({c["label"]["rho_d"] for c in cells})
    grid = np.array([[scalar(pick(cells, alpha_d=a, rho_d=r), "panic_index_at")[0]
                      for r in rhos] for a in alphas])
    mesh = ax.imshow(grid, origin="lower", aspect="auto",
                     cmap="Greys" if MONO else SEQ, vmin=0, vmax=0.45,
                     interpolation="nearest")
    ax.set_xticks(range(len(rhos)), [f"{r:g}" for r in rhos])
    ax.set_yticks(range(len(alphas)), [f"{a:g}" for a in alphas])
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    for i in range(len(alphas)):
        for j in range(len(rhos)):
            ax.text(j, i, f"{grid[i, j]:.2f}", ha="center", va="center", fontsize=9,
                    color="white" if grid[i, j] > 0.26 else INK)
    gate = alphas.index(0.7) - 0.5
    ax.plot([-0.5, len(rhos) - 0.5], [gate, gate], color=C(ORANGE), lw=2.6,
            solid_capstyle="butt", zorder=5)
    ax.set_xlim(-0.5, len(rhos) - 0.5 + 2.4)
    ax.text(len(rhos) - 0.30, gate, r"$\alpha_D(1-\bar b) = \epsilon$", fontsize=10.5,
            va="center", ha="left", color=C(ORANGE), fontweight="bold")
    ax.text(len(rhos) - 0.30, gate + 2.0, "above the gate:\nthe campaign divides",
            fontsize=10, va="center", ha="left", color=INK)
    ax.text(len(rhos) - 0.30, gate - 2.4, "below the gate:\nthe campaign converts",
            fontsize=10, va="center", ha="left", color=INK)
    ax.set_xlabel(X_REACH)
    ax.set_ylabel("depth   " + r"$\alpha_D$")
    bar = fig.colorbar(mesh, ax=ax, fraction=0.042, pad=0.03)
    bar.set_label("panic index  " + r"$\Pi$" + "  at $t = 199$", fontsize=10.5, color=SECOND)
    bar.outline.set_visible(False)
    headline(fig, "Depth is a gate, reach is the dial",
             "Panic index across the full depth $\\times$ reach grid; the rule marks where a "
             "single exposure crosses tolerance")
    footnote(fig, seed_note())
    save(fig, "panels", "h1d_gate")


# --------------------------------------------------------------------------- #
# H2 — handover
# --------------------------------------------------------------------------- #

DECOMPOSITION = [
    ("interaction",    BLUE,   "solid",               "interaction"),
    ("claims_alone",   ORANGE, (0, (5, 1.6)),         "claims-making alone"),
    ("warranted",      REF,    (0, (1.4, 1.6)),       "warranted   " + r"$\bar a^{\mathrm{null}}$"),
    ("othering_alone", AQUA,   (0, (4, 1.4, 1, 1.4)), "othering alone"),
]


def panel_h2a():
    cell = block(H2, "B1")[0]
    fig, ax = canvas()
    t = np.arange(len(curve(cell, "panic_index")))
    for key, colour, dash, label in DECOMPOSITION:
        ax.plot(t, curve(cell, key), color=C(colour), linestyle=dash, lw=2.0, label=label)
    ax.axvline(T_OFF, color=SECOND, lw=1.0, ls=(0, (2, 2)))
    ax.annotate("entrepreneur\nwithdraws", xy=(T_OFF, 0.175), xytext=(T_OFF + 10, 0.172),
                fontsize=10, color=INK, va="top")
    ax.annotate("", xy=(62, 0.244), xytext=(62, 0.041),
                arrowprops=dict(arrowstyle="<->", lw=1.2, color=SECOND))
    ax.text(69, 0.140, r"$\times\,5.94$", fontsize=12, color=INK)
    ax.set_xlim(0, t[-1]); ax.set_ylim(-0.012, 0.32)
    ax.set_xlabel("step   $t$")
    ax.set_ylabel("contribution to mean alarm   " + r"$\bar a$")
    legend(ax, loc="upper right")
    headline(fig, "The interaction dominates the entrepreneur's own signal",
             "The four terms of the decomposition across the entrepreneur's withdrawal")
    footnote(fig, seed_note() + r"  Operating point: `base`, $\alpha_D = 0.7$, $\rho_D = 0.25$, "
             r"$t_{\mathrm{off}} = 150$.")
    save(fig, "panels", "h2a_decomposition")


def panel_h2b():
    cells = block(H2, "B2")
    fig, ax = canvas()
    x, at_m, _ = sweep(cells, "omega", "panic_index_at")
    _, end_m, end_s = sweep(cells, "omega", "panic_index_end")
    ax.fill_between(x, end_m, at_m, color=MUTED, alpha=0.16, lw=0,
                    label="decayed over 250 steps")
    ax.plot(x, at_m, color=C(ORANGE), ls=(0, (5, 1.6)), marker="s", ms=6.0, lw=2.0,
            label=r"at withdrawal,  $\Pi(149)$")
    ax.plot(x, end_m, color=C(BLUE), ls="solid", marker="o", ms=6.0, lw=2.2,
            label=r"250 steps later,  $\Pi(399)$")
    ax.fill_between(x, end_m - end_s, end_m + end_s, color=C(BLUE), alpha=0.13, lw=0)
    ax.axhline(0, color=SECOND, lw=1.0)
    ax.annotate(r"at $\omega = 0$ disproportion" + "\ndecays to exactly zero",
                xy=(0.006, 0.003), xytext=(0.045, 0.140), fontsize=10, color=INK,
                arrowprops=dict(arrowstyle="->", lw=0.9, color=SECOND))
    ax.set_xlim(-0.02, 0.50); ax.set_ylim(-0.02, 0.47)
    ax.set_xlabel("othering weight   " + r"$\omega$")
    ax.set_ylabel("panic index   " + r"$\Pi$")
    legend(ax, loc="upper left")
    headline(fig, "Post-withdrawal persistence is governed by othering",
             "Panic index at withdrawal and 250 steps later, at fixed total alarm intensity")
    footnote(fig, seed_note() + r"  $\mu + \delta$ held at 0.55, so only the mix changes.")
    save(fig, "panels", "h2b_othering")


def panel_h2c():
    fig, ax = plt.subplots(figsize=(8.6, 4.9))
    subcritical = {(p["p_mu"], p["p_delta"], p["p_omega"]): p["subcritical"] for p in C3["points"]}
    points, values, valid = [], [], []
    for cell in block(H2, "B6"):
        key = (cell["label"]["p_mu"], cell["label"]["p_delta"], cell["label"]["p_omega"])
        points.append(key)
        values.append(scalar(cell, "panic_index_end")[0])
        valid.append(bool(subcritical.get(key, True)))
    points, values, valid = np.array(points), np.array(values), np.array(valid)
    x = points[:, 1] + 0.5 * points[:, 2]
    y = (np.sqrt(3) / 2) * points[:, 2]
    ax.plot([0, 1, 0.5, 0], [0, 0, np.sqrt(3) / 2, 0], color="#c9c9c6", lw=1.2, zorder=2)
    dots = ax.scatter(x[valid], y[valid], c=values[valid], cmap="Greys" if MONO else SEQ,
                      s=150, vmin=0, vmax=0.11, edgecolors="#c9c9c6", linewidths=0.6, zorder=3)
    ax.scatter(x[~valid], y[~valid], marker="x", s=70, color=C(ORANGE), linewidths=1.8, zorder=4)
    best = int(np.argmax(np.where(valid, values, -1)))
    ax.plot(x[best], y[best], marker="o", ms=22, mfc="none", mec=C(BLUE), mew=2.0, zorder=5)
    for label, (px, py), (dx, dy) in [
            ("memory\n" + r"$\mu$", (0, 0), (-0.04, -0.10)),
            ("contagion\n" + r"$\delta$", (1, 0), (0.04, -0.10)),
            ("othering\n" + r"$\omega$", (0.5, np.sqrt(3) / 2), (0, 0.20))]:
        ax.annotate(label, xy=(px, py), xytext=(px + dx, py + dy), fontsize=11,
                    color=INK, ha="center", va="center")
    ax.annotate("maximum over the 41\nsub-critical points, at\npure othering",
                xy=(x[best] + 0.03, y[best] - 0.02), xytext=(0.80, 0.66),
                fontsize=10, color=INK, ha="left",
                arrowprops=dict(arrowstyle="->", lw=0.9, color=SECOND))
    ax.text(-0.18, -0.30, "×   discarded: contagion supercritical, so alarm sustains itself "
            "without any campaign", fontsize=9.5, color=C(ORANGE), ha="left")
    ax.set_xlim(-0.22, 1.36); ax.set_ylim(-0.38, 1.14)
    ax.set_aspect("equal"); ax.axis("off")
    bar = fig.colorbar(dots, ax=ax, fraction=0.030, pad=0.02, shrink=0.55, anchor=(0.0, 0.80))
    bar.set_label(r"$\Pi(399)$", fontsize=10.5, color=SECOND)
    bar.outline.set_visible(False)
    headline(fig, "Residual disproportion across the simplex of alarm splits",
             "45 splits of memory, contagion and othering at fixed total intensity $s = 0.60$")
    save(fig, "panels", "h2c_simplex")


def panel_h2d():
    fig, ax = canvas(8.6, 4.4)
    names = SOBOL["input_names"]
    pretty = {"s": "total intensity\n" + r"$s = \mu + \delta + \omega$",
              "u1": "split: memory vs rest\n" + r"$(u_1)$",
              "u2": "split: othering vs contagion\n" + r"$(u_2)$"}
    width, positions = 0.36, np.arange(len(names))
    series = [("residual_ratio", C(BLUE), r"persistence  $\Pi(399)/\Pi(150)$", None),
              ("handover_step", "#ffffff", "handover step", "///")]
    for k, (key, colour, label, hatch) in enumerate(series):
        heights = SOBOL["outputs"][key]["ST"]
        bars = ax.bar(positions + (k - 0.5) * width, heights, width * 0.9, label=label,
                      color=colour, edgecolor=C(BLUE), linewidth=1.2, hatch=hatch, zorder=3)
        for bar_patch, height in zip(bars, heights):
            ax.text(bar_patch.get_x() + bar_patch.get_width() / 2, height + 0.035,
                    f"{height:.2f}", ha="center", fontsize=10, color=INK)
    ax.set_xticks(positions, [pretty[n] for n in names], fontsize=11)
    ax.set_ylim(0, 1.30); ax.grid(axis="x", visible=False)
    ax.set_ylabel("total-order Sobol index   " + r"$S_T$")
    legend(ax, loc="upper left")
    headline(fig, "Persistence is governed by the split, not the total intensity",
             "Share of the variation in each outcome attributable to each reparameterised input")
    footnote(fig, "Saltelli/Jansen estimators, $N = 256$; docked against the Ishigami function "
                  f"to {SOBOL['estimator_check']['max_abs_error']:.4f}.")
    save(fig, "panels", "h2d_sobol")


# --------------------------------------------------------------------------- #
# H3 — defence
# --------------------------------------------------------------------------- #

def defense_traces():
    cells = block(H3, "C1")
    return {name: {k: curve(pick(cells, configuration=name), k)
                   for k in ("panic_index", "mean_position")}
            for name, *_ in DEFENSE_STYLE}


def panel_h3a():
    traces = defense_traces()
    t = np.arange(len(traces["none"]["panic_index"]))
    fig, ax = canvas()
    for name, colour, dash, label in DEFENSE_STYLE:
        ax.plot(t, traces[name]["panic_index"], color=C(colour), linestyle=dash, lw=2.0,
                label=label + DEFENSE_DETAIL[name])
    ax.axvline(T_OFF, color=SECOND, lw=1.0, ls=(0, (2, 2)))
    ax.text(T_OFF + 3, 0.575, "$D$ withdraws,\n$C$ enters", fontsize=10.5,
            color=INK, ha="left", va="top")
    peak = int(np.argmax(traces["narrow_deep"]["panic_index"]))
    ax.plot(peak, traces["narrow_deep"]["panic_index"][peak], marker="o", ms=14,
            mfc="none", mec=C(ORANGE), mew=1.6)
    ax.annotate("61% above the\nundefended baseline", xy=(peak + 3, 0.467),
                xytext=(peak + 26, 0.505), fontsize=10.5, color=INK,
                arrowprops=dict(arrowstyle="->", lw=0.9, color=SECOND))
    ax.set_xlim(132, 285); ax.set_ylim(0, 0.60)
    ax.set_xlabel("step   $t$"); ax.set_ylabel("panic index   " + r"$\Pi$")
    legend(ax, loc="center right", bbox_to_anchor=(1.02, 0.58))
    headline(fig, "Every configuration overshoots before it works",
             "Three counter-entrepreneur configurations against the undefended baseline")
    footnote(fig, seed_note())
    save(fig, "panels", "h3a_overshoot")


def panel_h3b():
    traces = defense_traces()
    t = np.arange(len(traces["none"]["panic_index"]))
    fig, ax = canvas()
    ax.axhspan(0, 0.30, color=MUTED, alpha=0.09, lw=0)
    for name, colour, dash, label in DEFENSE_STYLE[1:]:
        excess = traces[name]["panic_index"] - traces["none"]["panic_index"]
        crossing = int((excess[T_OFF:] > 0).sum())
        ax.plot(t - T_OFF, excess, color=C(colour), linestyle=dash, lw=2.1,
                label=f"{label} — {crossing} steps above")
        ax.plot(crossing, 0.0, marker="|", ms=13, color=C(colour), mew=2.2)
    ax.axhline(0, color=SECOND, lw=1.2)
    ax.text(52, 0.085, "defence above the undefended baseline", fontsize=10.5, color=INK)
    ax.text(52, -0.255, "defence below the undefended baseline", fontsize=10.5, color=INK)
    ax.set_xlim(-2, 110); ax.set_ylim(-0.29, 0.30)
    ax.set_xlabel("steps since $C$ entered")
    ax.set_ylabel(r"$\Pi \; - \; \Pi$(undefended)")
    legend(ax, loc="upper right")
    headline(fig, "Disproportion rises first and falls later, never to zero",
             "Each configuration with the undefended baseline subtracted")
    footnote(fig, seed_note())
    save(fig, "panels", "h3b_excess")


def panel_h3c():
    traces = defense_traces()
    fig, ax = canvas()
    for name, colour, dash, label in DEFENSE_STYLE:
        path_b = traces[name]["mean_position"][T_OFF:]
        path_p = traces[name]["panic_index"][T_OFF:]
        ax.plot(path_b, path_p, color=C(colour), linestyle=dash, lw=2.0, label=label)
        ax.plot(path_b[-1], path_p[-1], marker="o", ms=7, color=C(colour), zorder=4)
    ax.plot(traces["none"]["mean_position"][T_OFF], traces["none"]["panic_index"][T_OFF],
            marker="*", ms=19, color=INK, zorder=5)
    ax.annotate(r"common start at $t_{\mathrm{off}}$", xy=(0.27, 0.294), xytext=(0.02, 0.470),
                fontsize=10.5, color=INK, ha="left",
                arrowprops=dict(arrowstyle="->", lw=0.9, color=SECOND))
    ax.annotate(r"total conversion to $p_C = -1$:" + "\nno disagreement left to fear",
                xy=(-0.98, 0.035), xytext=(-0.72, 0.108), fontsize=10, color=INK, ha="left",
                arrowprops=dict(arrowstyle="->", lw=0.9, color=SECOND))
    ax.axvline(0, color="#d8d8d5", lw=1.0)
    ax.set_xlim(-1.12, 0.62); ax.set_ylim(0, 0.60)
    ax.set_xlabel("mean position   " + r"$\bar b$")
    ax.set_ylabel("panic index   " + r"$\Pi$")
    legend(ax, loc="upper left")
    headline(fig, "Disproportion falls only as the population converts",
             r"Each run as a path across the $(\bar b,\ \Pi)$ plane, from withdrawal to the horizon")
    footnote(fig, seed_note())
    save(fig, "panels", "h3c_conversion")


def panel_h3d():
    cells = block(H3, "C2")
    fig, ax = canvas()
    grid_x = np.linspace(0, 1.05, 20)
    ax.plot(grid_x, 0.18 * grid_x, color=MUTED, lw=1.0, ls=(0, (4, 3)), zorder=1)
    for axis, colour, dash, marker, label in [
            ("rho_c", BLUE, "solid", "o", r"vary reach $\rho_C$   (depth fixed at 0.50)"),
            ("alpha_c", AQUA, (0, (1.4, 1.6)), "^", r"vary depth $\alpha_C$   (reach fixed at 0.50)")]:
        selected = [c for c in cells if c["label"]["axis"] == axis]
        x, m, s = sweep(selected, "value", "panic_index_end")
        ax.errorbar(x, m, yerr=s, color=C(colour), linestyle=dash, marker=marker, ms=6.0,
                    lw=2.0, capsize=3, elinewidth=1.0, label=label, zorder=3)
    ax.annotate(r"$\Pi \approx 0.18\,\rho_C$" + "\nthe residual cost of broadcasting",
                xy=(0.80, 0.148), xytext=(0.06, 0.190), fontsize=10.5, color=INK,
                arrowprops=dict(arrowstyle="->", lw=0.9, color=SECOND))
    ax.set_xlim(0, 1.06); ax.set_ylim(0, 0.215)
    ax.set_xlabel("counter-entrepreneur's   " + r"$\rho_C$   or   $\alpha_C$")
    ax.set_ylabel(r"$\Pi(399)$")
    legend(ax, loc="lower right")
    headline(fig, "The residual floor scales with reach, not with depth",
             "Disproportion at the horizon, moving one of the counter-entrepreneur's levers at a time")
    footnote(fig, seed_note())
    save(fig, "panels", "h3d_floor")


# --------------------------------------------------------------------------- #
# Concept figures — no notation required
# --------------------------------------------------------------------------- #

# Neutral has to stay visible: an agent who has not moved is still a dot on a
# white slide, so the midpoint is a legible grey rather than the surface colour.
DIVERGING = LinearSegmentedColormap.from_list(
    "stance", ["#1c5cab", "#4a90e2", "#a8c8ea", "#cfcfcb", "#f2a883", "#eb6834", "#b8410f"])


def box(ax, x, y, w, h, title, body, *, fill="#f7f7f5", edge="#d8d8d5", lw=1.2,
        title_colour=INK, body_colour=SECOND, title_size=11.5, body_size=10):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.10",
                                facecolor=fill, edgecolor=edge, linewidth=lw, zorder=2))
    ax.text(x + w / 2, y + h - 0.20, title, ha="center", va="top", fontsize=title_size,
            fontweight="bold", color=title_colour, zorder=3)
    ax.text(x + w / 2, y + h - 0.58 - 0.42 * title.count("\n"), body, ha="center", va="top",
            fontsize=body_size, color=body_colour, zorder=3, linespacing=1.35)


def arrow(ax, start, end, colour=SECOND, lw=1.6, style="-|>"):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=14,
                                 color=colour, lw=lw, shrinkA=2, shrinkB=2, zorder=4))


def blank_axes(width, height, xlim, ylim):
    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect("equal" if (xlim[1] - xlim[0]) == (ylim[1] - ylim[0]) else "auto")
    ax.axis("off"); ax.grid(False)
    return fig, ax


def concept_counterfactual():
    """The same population, lived four times: what disproportion is measured against."""
    cell = block(H2, "B1")[0]
    at = T_OFF - 1
    warranted = curve(cell, "warranted")[at]
    claims = curve(cell, "claims_alone")[at]
    othering = curve(cell, "othering_alone")[at]
    interaction = curve(cell, "interaction")[at]

    worlds = [  # (column, row, title, body, mean alarm, fill)
        (0, 1, "Neither   " + r"$\bar a^{\mathrm{null}}$",
         "claims-making off,\nothering off", warranted, "#f7f7f5"),
        (1, 1, "Claims-making only   " + r"$\bar a^{\mathrm{cm}}$",
         "claims-making on,\nothering off", warranted + claims, "#fdf0e9"),
        (0, 0, "Othering only   " + r"$\bar a^{\mathrm{oth}}$",
         "claims-making off,\nothering on", warranted + othering, "#e9f8f2"),
        (1, 0, "Both   " + r"$\bar a$", "the full run",
         warranted + claims + othering + interaction, "#e8f1fc"),
    ]
    fig, ax = blank_axes(8.6, 5.3, (0, 10), (-1.35, 5.6))
    for column, row, title, body, value, fill in worlds:
        x, y = 0.35 + column * 4.4, 0.35 + row * 2.55
        edge = {"#e8f1fc": C(BLUE), "#fdf0e9": C(ORANGE), "#e9f8f2": C(AQUA)}.get(fill, "#d8d8d5")
        box(ax, x, y, 4.0, 2.2, title, body, fill=fill, edge=edge, lw=1.6)
        ax.text(x + 3.80, y + 0.18, f"mean alarm  {value:.3f}", ha="right", va="bottom",
                fontsize=10.5, color=INK, fontweight="bold")
    ax.text(5.0, -0.35, "interaction  =  Both  −  Claims-making only  −  Othering only  +  Neither",
            ha="center", va="top", fontsize=12.5, color=INK, fontweight="bold")
    ax.text(5.0, -0.95, "A single seed fixes the network, the initial positions, the initial alarm "
            "and the thresholds, so the four worlds\nare the same population and no other "
            "difference between them is possible.",
            ha="center", va="top", fontsize=10, color=MUTED, linespacing=1.4)
    headline(fig, "The $2 \\times 2$ counterfactual design",
             "Every setting is executed four times on one seed, switching each source of alarm "
             "off in turn")
    save(fig, "concepts", "c1_four_worlds")


def concept_mechanism():
    """The chain from unequal exposure to alarm, and where the campaign touches it."""
    steps = [
        ("Unequal exposure", "the campaign addresses\nsome agents repeatedly\nand others never"),
        ("Moral division", "the agents it reaches\nmove; the remainder\nstay where they were"),
        ("Loss of persuasion", "neighbours now beyond\neach other's tolerance\nstop influencing"),
        ("Othering", "moral disagreement is\nconverted into\nperceived threat"),
        ("Alarm", "which then spreads\nby contagion between\nneighbours"),
    ]
    width, gap = 4.6, 1.3
    span = len(steps) * width + (len(steps) - 1) * gap
    fig, ax = blank_axes(13.0, 4.0, (-0.4, span + 0.4), (-2.1, 4.6))
    for index, (title, body) in enumerate(steps):
        x = index * (width + gap)
        highlight = index == len(steps) - 1
        box(ax, x, 0.90, width, 2.7, title, body,
            fill="#e8f1fc" if highlight else "#f7f7f5",
            edge=C(BLUE) if highlight else "#d8d8d5", lw=1.6 if highlight else 1.2,
            title_size=12, body_size=10.5)
        if index < len(steps) - 1:
            arrow(ax, (x + width + 0.15, 2.25), (x + width + gap - 0.15, 2.25))
    arrow(ax, (width / 2, 4.15), (width / 2, 3.75), colour=C(ORANGE), lw=2.0)
    ax.text(width / 2, 4.25, "the claims-maker acts on this step alone", ha="center",
            va="bottom", fontsize=11.5, color=C(ORANGE), fontweight="bold")
    ax.add_patch(FancyArrowPatch((span - width / 2, 0.70), (width + gap + width / 2, 0.70),
                                 arrowstyle="-|>", mutation_scale=16,
                                 connectionstyle="arc3,rad=-0.34", color=C(BLUE), lw=1.8, zorder=1))
    ax.text(span / 2, -1.72, "once the division exists, the remaining steps proceed with no "
            "claims-making at all",
            ha="center", va="center", fontsize=12, color=C(BLUE))
    headline(fig, "From unequal exposure to alarm", y=1.04)
    save(fig, "concepts", "c2_mechanism")


def concept_tolerance():
    """The asymmetry the whole model rests on."""
    fig, ax = blank_axes(9.4, 4.4, (-1.25, 1.25), (-1.5, 1.5))
    ax.set_aspect("auto")
    ax.plot([-1.12, 1.12], [0, 0], color="#c9c9c6", lw=1.4, zorder=1)
    for position, label in [(-1, r"$-1$  stigmatised pole"), (0, ""),
                            (1, r"$+1$  dominant claim")]:
        ax.plot([position], [0], marker="|", ms=14, color="#c9c9c6", mew=1.4)
        if label:
            ax.text(position, -0.28, label, ha="center", fontsize=10.5, color=MUTED)
    ax.add_patch(Rectangle((-0.5, -0.14), 1.0, 0.28, facecolor="#e8f1fc",
                           edgecolor=C(BLUE), lw=1.2, zorder=2))
    ax.text(0.0, 0.20, r"tolerance $\epsilon$", ha="center", va="bottom",
            fontsize=11.5, color=C(BLUE))

    ax.plot([0], [0], marker="o", ms=15, color=INK, zorder=5)
    ax.text(0.0, -0.40, "agent $i$", ha="center", fontsize=12, color=INK, fontweight="bold")
    ax.plot([0.32], [0], marker="o", ms=13, color=C(AQUA), zorder=5, mec="white", mew=1.2)
    ax.plot([0.86], [0], marker="o", ms=13, color=C(ORANGE), zorder=5, mec="white", mew=1.2)

    ax.annotate("neighbour within tolerance:\nmoves $i$'s position and alarm",
                xy=(0.32, 0.12), xytext=(0.10, 1.10), fontsize=11.5, color=C(AQUA), ha="center",
                arrowprops=dict(arrowstyle="->", lw=1.4, color=C(AQUA),
                                connectionstyle="arc3,rad=-0.20"))
    ax.annotate("neighbour beyond tolerance:\nmoves $i$'s alarm only",
                xy=(0.88, 0.12), xytext=(0.86, 0.62), fontsize=11.5, color=C(ORANGE), ha="center",
                arrowprops=dict(arrowstyle="->", lw=1.4, color=C(ORANGE)))
    ax.text(0.0, -1.02, "A neighbour beyond tolerance is tuned out of persuasion "
            "but not out of view.",
            ha="center", fontsize=13, color=INK, fontweight="bold")
    ax.text(0.0, -1.34, "It contributes nothing to $i$'s position and the most to $i$'s alarm: "
            "a divided population manufactures its own alarm.",
            ha="center", fontsize=10.5, color=MUTED)
    headline(fig, "The bounded-confidence asymmetry", y=1.04)
    save(fig, "concepts", "c3_tolerance")


def concept_apportionment():
    """Where the manufactured alarm comes from: 14 / 2 / 84."""
    cell = block(H2, "B1")[0]
    at = T_OFF - 1
    parts = [("claims-making alone — the entrepreneur's own signal",
              curve(cell, "claims_alone")[at], C(ORANGE)),
             ("othering alone — disagreement present before the campaign",
              curve(cell, "othering_alone")[at], C(AQUA)),
             ("interaction — campaign-created division, othered by the population",
              curve(cell, "interaction")[at], C(BLUE))]
    total = sum(value for _, value, _ in parts)

    fig, ax = plt.subplots(figsize=(10.6, 4.0))
    ax.set_xlim(0, 1); ax.set_ylim(-1.62, 0.75); ax.axis("off"); ax.grid(False)
    left = 0.0
    for label, value, colour in parts:
        share = value / total
        ax.add_patch(Rectangle((left + 0.003, 0.10), share - 0.006, 0.50, facecolor=colour,
                               edgecolor="white", linewidth=0, zorder=3))
        if share > 0.08:
            ax.text(left + share / 2, 0.35, f"{share * 100:.0f}%", ha="center", va="center",
                    fontsize=19, color="white", fontweight="bold", zorder=4)
        left += share
    # The key sits underneath, one row per slice: leader lines to a 2% sliver collide.
    for row, (label, value, colour) in enumerate(parts):
        share = value / total
        y = -0.24 - row * 0.34
        ax.add_patch(Rectangle((0.0, y - 0.055), 0.022, 0.11, facecolor=colour, lw=0, zorder=3))
        ax.text(0.036, y, f"{share * 100:4.0f}%", ha="left", va="center", fontsize=13,
                color=INK, fontweight="bold")
        ax.text(0.115, y, label, ha="left", va="center", fontsize=11.5, color=SECOND)
    ax.text(0.0, -1.45, "The entrepreneur is necessary, and accounts for a seventh of "
            "the manufactured alarm.", ha="left", va="center", fontsize=13, color=INK,
            fontweight="bold")
    headline(fig, "Apportionment of manufactured alarm",
             r"The three manufactured terms of the decomposition at $t = 149$, "
             "the step before withdrawal", y=1.10)
    save(fig, "concepts", "c4_apportionment")


def concept_reach():
    """Loudness is not the mechanism: the same campaign, told to more and more people."""
    cells = repertoire_cells("base")
    x, m, _ = sweep(cells, "rho_d", "panic_index_at")
    by_reach = {c["label"]["rho_d"]: c for c in cells}
    cut = "0.20_0.20_10"

    fig, ax = canvas(9.2, 4.6)
    ax.plot(x, m, color=C(BLUE), lw=2.6, marker="o", ms=6.5, zorder=3)
    peak = int(np.argmax(m))
    ax.plot(x[peak], m[peak], marker="o", ms=16, mfc="none", mec=C(BLUE), mew=2.0, zorder=4)

    def incidence(reach):
        return by_reach[reach]["incidence"][cut]

    ax.annotate(f"maximum at $\\rho_D = {x[peak]:.2f}$:\npanic incidence "
                f"{incidence(x[peak]):.2f}",
                xy=(x[peak], m[peak] - 0.022), xytext=(0.28, 0.205), fontsize=10.5, color=INK,
                ha="left", arrowprops=dict(arrowstyle="->", lw=1.0, color=SECOND))
    ax.annotate(f"universal reach: $\\Pi$ halves and\npanic incidence is "
                f"{incidence(1.0):.2f}\nunder every cut of the criterion",
                xy=(1.0, 0.186), xytext=(0.62, 0.070), fontsize=10.5, color=C(ORANGE),
                ha="left", arrowprops=dict(arrowstyle="->", lw=1.0, color=C(ORANGE)))
    ax.annotate("negligible reach:\nno episode",
                xy=(0.03, 0.030), xytext=(0.045, 0.330), fontsize=10.5, color=MUTED,
                ha="left", arrowprops=dict(arrowstyle="->", lw=1.0, color=MUTED))
    ax.set_xlim(-0.01, 1.06); ax.set_ylim(0, 0.52)
    ax.set_xlabel(X_REACH)
    ax.set_ylabel("panic index   " + r"$\Pi$" + "   at $t = 199$")
    headline(fig, "Universal reach manufactures no division",
             "The `base` repertoire, identical in every respect except the share of the "
             "population it addresses")
    footnote(fig, seed_note() + r"  Incidence at $\Pi^* = q^* = 0.20$, $W = 10$; the "
             "conclusion holds across the whole grid of cuts.")
    save(fig, "concepts", "c5_reach")


def concept_timeline():
    """The life of one episode, in three acts."""
    cell = block(H2, "B1")[0]
    panic = curve(cell, "panic_index")
    t = np.arange(len(panic))
    fig, ax = canvas(9.6, 4.6)
    ax.axvspan(0, T_OFF, color="#fdf0e9", alpha=0.85, lw=0, zorder=0)
    ax.axvspan(T_OFF, t[-1], color="#f4f8fe", alpha=0.9, lw=0, zorder=0)
    ax.plot(t, panic, color=C(BLUE), lw=2.8, zorder=3)
    ax.axvline(T_OFF, color=SECOND, lw=1.2, ls=(0, (2, 2)), zorder=2)
    ax.plot([T_OFF, t[-1]], [panic[T_OFF], panic[-1]], marker="o", ms=8, ls="none",
            color=C(BLUE), zorder=4)

    retained = panic[-1] / panic[T_OFF - 1]
    ax.text(T_OFF / 2, 0.055, "entrepreneur active", ha="center", fontsize=12,
            color=C(ORANGE), fontweight="bold")
    ax.text((T_OFF + t[-1]) / 2, 0.055, "no claims-making", ha="center",
            fontsize=12, color=C(BLUE), fontweight="bold")
    ax.annotate("claims-making alone falls to\nzero within five steps",
                xy=(T_OFF + 6, panic[T_OFF + 6]), xytext=(T_OFF + 26, 0.365), fontsize=10.5,
                color=INK, arrowprops=dict(arrowstyle="->", lw=1.0, color=SECOND))
    ax.annotate(f"{retained:.0%} of the disproportion\nretained 250 steps later",
                xy=(t[-1] - 2, panic[-1]), xytext=(t[-1] - 150, 0.115), fontsize=11.5,
                color=INK, ha="left", arrowprops=dict(arrowstyle="->", lw=1.0, color=SECOND))
    ax.set_xlim(0, t[-1]); ax.set_ylim(0, 0.40)
    ax.set_xlabel("step   $t$"); ax.set_ylabel("panic index   " + r"$\Pi$")
    headline(fig, "Disproportion across the entrepreneur's withdrawal",
             r"The operating point, followed to the horizon $T = 400$")
    footnote(fig, seed_note())
    save(fig, "concepts", "c6_timeline")


def concept_overshoot():
    """The defence result, reduced to the two curves that carry it."""
    traces = defense_traces()
    t = np.arange(len(traces["none"]["panic_index"]))
    none, deep = traces["none"]["panic_index"], traces["narrow_deep"]["panic_index"]
    above = deep > none
    fig, ax = canvas(9.6, 4.6)
    ax.fill_between(t, none, deep, where=above, color=C(ORANGE), alpha=0.16, lw=0, zorder=1,
                    interpolate=True)
    ax.fill_between(t, none, deep, where=~above, color=C(BLUE), alpha=0.12, lw=0, zorder=1,
                    interpolate=True)
    ax.plot(t, none, color=C(REF), lw=2.2, ls=(0, (4, 2.4)), label="undefended baseline", zorder=3)
    ax.plot(t, deep, color=C(BLUE), lw=2.6,
            label=r"narrow & deep  $(\alpha_C, \rho_C) = (0.90,\, 0.10)$", zorder=3)
    ax.axvline(T_OFF, color=SECOND, lw=1.2, ls=(0, (2, 2)), zorder=2)
    ax.text(T_OFF + 3, 0.575, "$C$ enters", fontsize=10.5, color=INK, va="top")
    crossing = T_OFF + int((deep[T_OFF:] > none[T_OFF:]).sum())
    ax.annotate("24 steps above the\nundefended baseline", xy=(T_OFF + 12, 0.42),
                xytext=(T_OFF + 34, 0.500), fontsize=11, color=C(ORANGE),
                arrowprops=dict(arrowstyle="->", lw=1.0, color=C(ORANGE)))
    ax.annotate("lower thereafter, and only\nthrough total conversion",
                xy=(crossing + 55, 0.075), xytext=(crossing + 12, 0.215), fontsize=11,
                color=C(BLUE), arrowprops=dict(arrowstyle="->", lw=1.0, color=C(BLUE)))
    ax.set_xlim(132, 300); ax.set_ylim(0, 0.60)
    ax.set_xlabel("step   $t$"); ax.set_ylabel("panic index   " + r"$\Pi$")
    legend(ax, loc="center right", bbox_to_anchor=(1.01, 0.62))
    headline(fig, "Counter-claims-making raises disproportion before lowering it",
             "The lowest-reach configuration produces the largest overshoot")
    footnote(fig, seed_note())
    save(fig, "concepts", "c7_defence_overshoot")


# --------------------------------------------------------------------------- #
# Concept figures that re-run the model
# --------------------------------------------------------------------------- #

def demo_run(n_agents=300, n_steps=200, seed=11):
    """One live trajectory at the operating point, small enough to draw."""
    sys.path.insert(0, str(HERE.parent / "Code"))
    from moralpanic.config import (NetworkSpec, Parameters, RunConfig, Repertoire,
                                   Topology, entrepreneur)
    from moralpanic.model import Model, initialise
    from moralpanic.rng import Streams

    config = RunConfig(
        seed=seed, n_steps=n_steps,
        network=NetworkSpec(topology=Topology.SMALL_WORLD, n_agents=n_agents, mean_degree=10.0),
        parameters=Parameters(epsilon=META["epsilon"], mu=META["mu"],
                              delta=META["delta"], omega=META["omega"]),
        actor_d=entrepreneur(alpha=META["alpha_d"], rho=META["rho_d"],
                             repertoire=Repertoire.BASE),
        record_states=True)
    streams = Streams.from_seed(seed)
    initial = initialise(config, streams)
    return initial.graph, Model(config, streams, initial).run()


def concept_network():
    """What the population looks like before and after the campaign."""
    import networkx as nx

    graph, result = demo_run()
    layout = nx.spring_layout(graph, seed=4, iterations=90)
    coords = np.array([layout[node] for node in graph.nodes()])
    before, after = result.position_states[0], result.position_states[T_OFF]

    fig = plt.figure(figsize=(11.6, 5.9))
    grid = fig.add_gridspec(2, 2, height_ratios=[3.1, 1.0], hspace=0.30, wspace=0.08)
    cmap = "Greys" if MONO else DIVERGING
    tallest = max(np.histogram(p, bins=np.linspace(-1, 1, 33))[0].max()
                  for p in (before, after))

    for column, (positions, caption) in enumerate(
            [(before, "$t = 0$, before the campaign"), (after, "$t = 150$, at withdrawal")]):
        ax = fig.add_subplot(grid[0, column])
        ax.axis("off"); ax.grid(False)
        segments = np.array([[coords[u], coords[v]] for u, v in graph.edges()])
        from matplotlib.collections import LineCollection
        ax.add_collection(LineCollection(segments, colors="#dcdcd9", linewidths=0.35, zorder=1))
        ax.scatter(coords[:, 0], coords[:, 1], c=(positions + 1) / 2, cmap=cmap,
                   vmin=0, vmax=1, s=46, edgecolors="white", linewidths=0.6, zorder=3)
        ax.set_title(caption, fontsize=13, color=INK, fontweight="bold", pad=6)
        ax.autoscale_view()
        ax.set_aspect("equal")

        hist = fig.add_subplot(grid[1, column])
        counts, edges = np.histogram(positions, bins=np.linspace(-1, 1, 33))
        centres = (edges[:-1] + edges[1:]) / 2
        colours = plt.get_cmap(cmap)((centres + 1) / 2)
        hist.bar(centres, counts, width=(edges[1] - edges[0]) * 0.9, color=colours, zorder=3)
        hist.set_ylim(0, tallest * 1.12)
        hist.set_xlim(-1.05, 1.05)
        hist.set_xticks([-1, 0, 1], [r"$-1$", "$0$", r"$+1$"], fontsize=10)
        hist.set_yticks([])
        for side in ("top", "right", "left"):
            hist.spines[side].set_visible(False)
        hist.grid(False)
        hist.set_xlabel("moral position   " + r"$b_i$", fontsize=10.5)

    moved = float((after > 0.9).mean())
    footnote(fig, f"{moved:.0%} of the population has been carried to the entrepreneur's pole "
             "and the remainder have not moved.\nThe resulting gap is twice the tolerance "
             r"$\epsilon = 0.5$, so the two groups no longer influence each other's positions "
             "and each contributes to the other's alarm.")
    headline(fig, "The population before and after the campaign",
             f"One run at the operating point, $N = {len(graph)}$, laid out by the network; "
             r"colour is the moral position $b_i$", y=1.02)
    save(fig, "concepts", "c8_network")


def concept_exposure():
    """The same number of messages, distributed two ways."""
    rng = np.random.default_rng(3)
    side, reached_per_step, steps = 10, 25, 20
    n = side * side
    fresh = np.zeros(n, dtype=int)
    for _ in range(steps):
        fresh[rng.choice(n, size=reached_per_step, replace=False)] += 1
    audience = rng.choice(n, size=reached_per_step, replace=False)
    fixed = np.zeros(n, dtype=int)
    fixed[audience] = steps

    concentration = {}
    for repertoire in ("random", "fixed_random"):
        cells = repertoire_cells(repertoire)
        match = [c for c in cells if c["label"]["rho_d"] == 0.25]
        if match:
            concentration[repertoire] = float(np.mean(
                [s["exposure_concentration"] for s in match[0]["seeds"]]))

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 5.0))
    cmap = plt.get_cmap("Greys" if MONO else SEQ)
    panels = [(fresh, "`random`: a fresh audience each step",
               "every agent is reached about five times;\nexposure is close to uniform"),
              (fixed, "`fixed_random`: one audience throughout",
               "a quarter are reached at every step;\nthree quarters are never reached")]
    for ax, (counts, title, caption) in zip(axes, panels):
        ax.axis("off"); ax.grid(False)
        ax.set_xlim(-0.5, side - 0.5); ax.set_ylim(-0.5, side + 1.2)
        ax.set_aspect("equal")
        for index, value in enumerate(counts):
            row, column = divmod(index, side)
            shade = cmap(0.08 + 0.85 * value / steps)
            ax.add_patch(Rectangle((column - 0.42, side - 1 - row - 0.42), 0.84, 0.84,
                                   facecolor=shade, edgecolor="#e4e4e1", linewidth=0.8))
        ax.set_title(title, fontsize=13, color=INK, fontweight="bold", pad=10)
        ax.text((side - 1) / 2, -2.15, caption, ha="center", va="top", fontsize=11,
                color=SECOND, linespacing=1.4)

    # The shading scale, drawn in the left panel's own coordinates: an inset axes
    # would sit outside the tight bounding box and collide with the footnote.
    scale = axes[0]
    for step in range(9):
        scale.add_patch(Rectangle((1.30 + step * 0.62, -1.42), 0.58, 0.42, clip_on=False,
                                  facecolor=cmap(0.08 + 0.85 * step / 8),
                                  edgecolor="#e4e4e1", linewidth=0.7, zorder=5))
    scale.text(1.20, -1.21, "reached 0 times", ha="right", va="center", fontsize=9.5, color=MUTED)
    scale.text(6.98, -1.21, f"reached {steps} times", ha="left", va="center",
               fontsize=9.5, color=MUTED)
    if len(concentration) == 2:
        ratio = concentration["fixed_random"] / concentration["random"]
        footnote(fig, r"In the model at $\rho_D = 0.25$ the exposure concentration "
                 r"$\mathrm{Var}_i(\sum_t g^D_i)$ is "
                 f"{concentration['random']:.0f} under `random` and "
                 f"{concentration['fixed_random']:.0f} under `fixed_random`:\nthe same number "
                 f"of exposures, distributed {ratio:.0f} times more unequally. Only the second "
                 "amplifies.", y=-0.135)
    headline(fig, "Two exposure schedules of identical size",
             r"$N = 100$, $\rho = 0.25$, 20 steps; each square is one agent, shaded by the "
             "number of times it was reached", y=1.06)
    save(fig, "concepts", "c9_exposure")


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #

PANELS = [panel_h1a, panel_h1b, panel_h1c, panel_h1d,
          panel_h2a, panel_h2b, panel_h2c, panel_h2d,
          panel_h3a, panel_h3b, panel_h3c, panel_h3d]

CONCEPTS = [concept_counterfactual, concept_mechanism, concept_tolerance,
            concept_apportionment, concept_reach, concept_timeline,
            concept_overshoot, concept_network, concept_exposure]


def main(argv=None):
    global H1, H2, H3, SOBOL, C3, META, T_OFF, OUT, FORMATS, MONO, TITLES

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", default=str(HERE.parent / "Presentation" / "figures"),
                        help="output directory (default: Presentation/figures)")
    parser.add_argument("--only", choices=("panels", "concepts", "all"), default="all")
    parser.add_argument("--formats", nargs="+", default=["pdf", "png"],
                        choices=["pdf", "png", "svg"])
    parser.add_argument("--mono", action="store_true",
                        help="greyscale, matching the figures in the paper")
    parser.add_argument("--no-untitled", action="store_true",
                        help="skip the headline-free copies the slide deck uses")
    args = parser.parse_args(argv)

    MONO = args.mono
    OUT = Path(args.out).expanduser().resolve()
    FORMATS = tuple(args.formats)
    apply_theme()

    H1, H2, H3, SOBOL, C3, META = load_store()
    T_OFF = META["t_off"]

    jobs = {"panels": PANELS, "concepts": CONCEPTS,
            "all": PANELS + CONCEPTS}[args.only]

    # Two copies of each figure. The titled one stands on its own, wherever it is
    # dropped; the untitled one goes on a slide whose heading already carries the
    # claim, where repeating it would be the standard slide-deck mistake.
    for job in jobs:
        job()
    titled = len(WRITTEN)
    print(f"{titled} files written under {OUT}")
    for path in WRITTEN:
        if path.suffix == ".pdf":
            print(f"  {path.relative_to(OUT)}")

    if not args.no_untitled:
        TITLES = False
        OUT = OUT / "untitled"
        for job in jobs:
            job()
        print(f"{len(WRITTEN) - titled} deck-ready copies (no headline) under {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
