"""Per-step measurements taken from a single trajectory (spec §10.3).

Quantities that need more than one run of the 2x2 design -- the decomposition,
the panic index, handover time, persistence -- live in `counterfactual.py`.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


BOUNDARY_TOL = 1e-9
"""How close to +/-1 a position must be to count as a boundary atom (spec §14.2)."""


@dataclass(frozen=True)
class StepRecord:
    """Measurements at one step (spec §10.3).

    mean_position   : b-bar(t)
    mean_alarm      : a-bar(t)
    amplifying      : q(t), the share past threshold
    mean_othering   : Phi-bar(t)
    bimodality      : Sarle's coefficient on positions; > 5/9 flags bimodality
    bimodality_interior : the same, excluding agents pinned at +/-1 (spec §14.2)
    boundary_fraction   : share of agents sitting exactly on a pole
    alarm_assortativity : Newman's scalar assortativity r_a of alarm over edges
    reached_d       : how many agents the entrepreneur reached this step
    """

    step: int
    mean_position: float
    mean_alarm: float
    amplifying: float
    mean_othering: float
    bimodality: float
    bimodality_interior: float
    boundary_fraction: float
    alarm_assortativity: float
    reached_d: int


def bimodality_coefficient(values: np.ndarray) -> float:
    """Sarle's bimodality coefficient (spec §10.3).

        BC = (g1^2 + 1) / (g2 + 3(n-1)^2 / ((n-2)(n-3)))

    with g1 the sample skewness and g2 the sample excess kurtosis in their
    bias-corrected (SAS/Excel) form, which is what Sarle's formula assumes.
    The uniform-distribution value 5/9 is the conventional flag. Returns NaN
    for n < 4 or for a degenerate (zero-variance) sample.
    """
    n = values.size
    if n < 4:
        return float("nan")
    sd = values.std(ddof=1)
    if not np.isfinite(sd) or sd <= 0.0:
        return float("nan")

    z = (values - values.mean()) / sd
    g1 = n / ((n - 1) * (n - 2)) * np.sum(z**3)
    g2 = (
        n * (n + 1) / ((n - 1) * (n - 2) * (n - 3)) * np.sum(z**4)
        - 3.0 * (n - 1) ** 2 / ((n - 2) * (n - 3))
    )
    denominator = g2 + 3.0 * (n - 1) ** 2 / ((n - 2) * (n - 3))
    if denominator == 0.0:
        return float("nan")
    return float((g1**2 + 1.0) / denominator)


def boundary_fraction(positions: np.ndarray, tol: float = BOUNDARY_TOL) -> float:
    """Share of agents sitting on a pole, where the clip in spec §7.3 has bound.

    Clipping accumulates mass as two point atoms at +/-1. That mass is
    indistinguishable from genuine polarization to any moment-based statistic,
    which is the artifact spec §14.2 (1) exists to detect.
    """
    if positions.size == 0:
        return float("nan")
    return float((np.abs(positions) >= 1.0 - tol).mean())


def interior_bimodality_coefficient(
    positions: np.ndarray, tol: float = BOUNDARY_TOL
) -> float:
    """Sarle's coefficient over the interior only (spec §14.2, artifact check 1).

    Agents pinned at +/-1 by the clip are dropped before the moments are taken,
    so what remains is bimodality of the freely-moving population. Read together
    with `boundary_fraction`: a high raw coefficient and a low interior one means
    the polarization is boundary pile-up, not emergent structure.

    Returns NaN when fewer than four agents survive the exclusion, which is
    itself informative -- it means essentially everyone is at a pole.
    """
    interior = positions[np.abs(positions) < 1.0 - tol]
    return bimodality_coefficient(interior)


def scalar_assortativity(values: np.ndarray, source: np.ndarray, target: np.ndarray) -> float:
    """Newman's scalar assortativity of `values` across edges (spec §10.3).

    Computed as the Pearson correlation over the 2|E| directed edge endpoints,
    which is Newman's definition. Returns NaN when there are no edges or the
    endpoint values are constant.
    """
    if source.size == 0:
        return float("nan")
    x = values[source]
    y = values[target]
    if x.std() == 0.0 or y.std() == 0.0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def measure_step(
    step: int,
    positions: np.ndarray,
    alarm: np.ndarray,
    thresholds: np.ndarray,
    othering: np.ndarray,
    neighbourhood,
    reached_d: np.ndarray,
) -> StepRecord:
    """Assemble one StepRecord from the time-t state."""
    return StepRecord(
        step=step,
        mean_position=float(positions.mean()),
        mean_alarm=float(alarm.mean()),
        amplifying=float((alarm > thresholds).mean()),
        mean_othering=float(othering.mean()),
        bimodality=bimodality_coefficient(positions),
        bimodality_interior=interior_bimodality_coefficient(positions),
        boundary_fraction=boundary_fraction(positions),
        alarm_assortativity=scalar_assortativity(
            alarm, neighbourhood.source, neighbourhood.target
        ),
        reached_d=int(reached_d.sum()),
    )


def exposure_concentration(reached_counts: np.ndarray) -> float:
    """Var_i( sum_t g^D_i(t) ), the variance of cumulative exposure (spec §10.3).

    Separates repertoires that address the same people repeatedly (`hub`, high
    variance) from those that spread exposure thinly (`random`, low variance)
    at equal reach. Moral distance arises from *differences* in exposure, so
    this is the quantity that discriminates where the interaction term is
    non-monotone in reach.
    """
    return float(np.var(reached_counts))
