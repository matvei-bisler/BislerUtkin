"""Sensitivity of persistence to the alarm parameters (spec §12.2).

Sampling mu, delta, omega independently on the unit cube is wrong here. C1
requires mu + delta + omega <= 1, a simplex of volume 1/6 inside the cube;
sampling the cube and rejecting violations makes the surviving inputs mutually
dependent, and the standard Sobol estimators no longer decompose the variance
correctly.

The design therefore reparameterises rather than rejects:

    mu = s * p_mu,   delta = s * p_delta,   omega = s * p_omega

with total intensity s ~ Uniform[0, 1] and the split (p_mu, p_delta, p_omega)
uniform on the 2-simplex, drawn from two independent uniforms by the standard
barycentric map. The Sobol inputs are (s, u1, u2): three quantities,
independent by construction, with C1 satisfied identically because the three
parameters sum to s.

The reparameterisation also matches the question. The dispute H2 joins is not
whether alarm is intense but what holds it up at a given intensity.
"""

from __future__ import annotations

from typing import Dict, Optional, Sequence, Tuple

import numpy as np

from .config import Parameters

SOBOL_INPUT_NAMES = ("s", "u1", "u2")

SOBOL_INPUT_NAMES_WITH_ZETA = ("s", "u1", "u2", "zeta")
"""The four-input design of spec §3.2.

zeta is the s.d. of idiosyncratic position noise. It is a fixed constant of §3.2
rather than a parameter, but at sigma = 0 the permanence of manufactured division
IS the structurally frozen state zeta exists to prevent, so zeta competes with
omega to explain persistence in exactly the way sigma does. The spec's own
standard is that such a constant must either be justified explicitly or enter
this analysis; this design is how it enters. It is independent of (s, u1, u2), so
it needs no reparameterisation -- it is simply a fourth column.
"""


def split_from_uniforms(u1: float, u2: float) -> Tuple[float, float, float]:
    """Map two independent uniforms onto the 2-simplex (spec §12.2).

        p_mu    = 1 - sqrt(u1)
        p_delta = sqrt(u1) * (1 - u2)
        p_omega = sqrt(u1) * u2

    This is the standard uniform sampler for a triangle in barycentric
    coordinates, so the split is uniform on the simplex.
    """
    root = np.sqrt(u1)
    return (1.0 - root, root * (1.0 - u2), root * u2)


def alarm_parameters(
    s: float, u1: float, u2: float, epsilon: float
) -> Parameters:
    """Build a Parameters object from the Sobol inputs (spec §12.2).

    C1 holds identically because mu + delta + omega = s <= 1. C2 (mu + delta < 1)
    is implied for s < 1 and is checked by `Parameters.require_stable`.
    """
    p_mu, p_delta, p_omega = split_from_uniforms(u1, u2)
    return Parameters(epsilon=epsilon, mu=s * p_mu, delta=s * p_delta, omega=s * p_omega)


def salib_problem() -> Dict[str, object]:
    """Problem definition for SALib's Saltelli sampler and Sobol analyser.

    Three inputs, all Uniform[0, 1] and mutually independent, which is exactly
    what the standard estimators assume. Provided for interoperability; the
    estimators below make SALib optional rather than required.
    """
    return {
        "num_vars": 3,
        "names": list(SOBOL_INPUT_NAMES),
        "bounds": [[0.0, 1.0]] * 3,
    }


# --------------------------------------------------------------------------- #
# Variance-based sensitivity, written out rather than imported (spec §12.2)
# --------------------------------------------------------------------------- #


def sobol_design(
    n_base: int, bounds: Optional[Sequence[float]] = None, seed: int = 20260804
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Saltelli's A / B / AB_i design over the three inputs (spec §12.2).

    `bounds` scales each input from the unit interval; the default is the unit
    cube. Capping the first input (total intensity s) is how the design is kept
    inside the C3 sub-critical region, and the cap must then be reported.

    Returns (A, B, AB) with A and B of shape (n_base, 3) and AB of shape
    (3, n_base, 3), where AB[i] is A with column i taken from B. Evaluating the
    model on all of them costs n_base * (k + 2) runs.

    A scrambled Sobol' sequence is used for the base sample, which converges
    faster than plain Monte Carlo; `n_base` should be a power of two for the
    sequence's balance properties to hold.
    """
    from scipy.stats import qmc

    scale = (
        np.ones(len(SOBOL_INPUT_NAMES))
        if bounds is None
        else np.asarray(bounds, dtype=float)
    )
    if scale.ndim != 1 or scale.size < 2:
        raise ValueError("bounds must be a one-dimensional sequence, one entry per input")
    k = scale.size

    sample = qmc.Sobol(d=2 * k, scramble=True, seed=seed).random(n_base)
    matrix_a, matrix_b = sample[:, :k] * scale, sample[:, k:] * scale
    matrix_ab = np.empty((k, n_base, k))
    for column in range(k):
        matrix_ab[column] = matrix_a.copy()
        matrix_ab[column][:, column] = matrix_b[:, column]
    return matrix_a, matrix_b, matrix_ab


def sobol_indices(
    f_a: np.ndarray, f_b: np.ndarray, f_ab: np.ndarray
) -> Dict[str, object]:
    """First-order (Saltelli 2010) and total-order (Jansen 1999) Sobol indices.

        S_i  = mean( f_B * (f_ABi - f_A) ) / Var(f)
        S_Ti = mean( (f_A - f_ABi)^2 ) / (2 Var(f))

    `f_ab` has shape (k, N): row i is the model evaluated on A with column i
    replaced by B's. Both estimators are the standard ones; they are written out
    here only so that the analysis of spec §12.2 has no optional dependency.

    `reliable` is False when any total index leaves [0, 1.05]. S_T is bounded
    above by 1 in expectation, so a violation means the estimator is straining --
    typically near-zero output variance, or an output with a large atom at a
    single value -- and the indices should not be reported as findings.
    """
    variance = float(np.var(np.concatenate([f_a, f_b]), ddof=1))
    k = f_ab.shape[0]
    if variance <= 0.0:
        return {"S1": [0.0] * k, "ST": [0.0] * k, "variance": 0.0, "reliable": False}

    first = [float(np.mean(f_b * (f_ab[i] - f_a)) / variance) for i in range(k)]
    total = [float(np.mean((f_a - f_ab[i]) ** 2) / (2.0 * variance)) for i in range(k)]
    return {
        "S1": first,
        "ST": total,
        "variance": variance,
        "reliable": bool(all(-0.05 <= value <= 1.05 for value in total)),
    }


def validate_sobol_estimator(n_base: int = 4096) -> Dict[str, object]:
    """Dock the estimators against Ishigami, whose indices are known in closed form.

    At a = 7, b = 0.1 on [-pi, pi]^3 the analytic values are
    S1 = (0.3139, 0.4424, 0) and ST = (0.5576, 0.4424, 0.2437). This verifies the
    estimator, not the model, and is reported separately from any result.
    """

    def ishigami(x: np.ndarray) -> np.ndarray:
        return np.sin(x[:, 0]) + 7.0 * np.sin(x[:, 1]) ** 2 + 0.1 * x[:, 2] ** 4 * np.sin(x[:, 0])

    matrix_a, matrix_b, matrix_ab = sobol_design(n_base, bounds=(1.0, 1.0, 1.0), seed=7)
    to_domain = lambda m: m * 2 * np.pi - np.pi
    estimated = sobol_indices(
        ishigami(to_domain(matrix_a)),
        ishigami(to_domain(matrix_b)),
        np.array([ishigami(to_domain(matrix_ab[i])) for i in range(matrix_ab.shape[0])]),
    )
    analytic = {"S1": [0.3139, 0.4424, 0.0], "ST": [0.5576, 0.4424, 0.2437]}
    error = max(
        max(abs(e - a) for e, a in zip(estimated[key], analytic[key])) for key in ("S1", "ST")
    )
    return {
        "n_base": n_base,
        "estimated": {"S1": estimated["S1"], "ST": estimated["ST"]},
        "analytic": analytic,
        "max_abs_error": float(error),
        "passed": bool(error < 0.01),
    }


def simplex_grid(resolution: int = 10) -> np.ndarray:
    """A regular lattice on the 2-simplex, for locating the persistence maximum.

    Returns an array of shape (M, 3) whose rows are (p_mu, p_delta, p_omega)
    summing to one. Used to report *where* on the simplex persistence peaks:
    H2 predicts the maximum sits near the omega vertex.
    """
    if resolution < 1:
        raise ValueError("resolution must be at least 1")
    points = []
    for i in range(resolution + 1):
        for j in range(resolution + 1 - i):
            k = resolution - i - j
            points.append((i / resolution, j / resolution, k / resolution))
    return np.array(points, dtype=float)


def parameters_from_split(
    split: np.ndarray, s: float, epsilon: float
) -> Parameters:
    """Parameters from an explicit split and total intensity."""
    p_mu, p_delta, p_omega = split
    return Parameters(epsilon=epsilon, mu=s * p_mu, delta=s * p_delta, omega=s * p_omega)
