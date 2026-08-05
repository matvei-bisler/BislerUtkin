"""Targeting: the three claims-making repertoires (spec §7.1).

Each actor reaches n_X = min(N, ceil(rho_X * N)) agents per step and sets
g^X_i(t) = 1 for those it selects. Ties in the ranked repertoires are broken
uniformly at random and redrawn each step, which matters for `hub` on
near-regular graphs where the repertoire degenerates toward `random`.
"""

from __future__ import annotations

from typing import Optional

import numpy as np

from .config import ActorSpec, Repertoire


def _lowest_n(keys: np.ndarray, n: int, rng: np.random.Generator) -> np.ndarray:
    """Indices of the n smallest keys, ties broken uniformly at random."""
    tiebreak = rng.random(keys.size)
    order = np.lexsort((tiebreak, keys))
    return order[:n]


def select_targets(
    actor: ActorSpec,
    step: int,
    positions: np.ndarray,
    degree: np.ndarray,
    rng: np.random.Generator,
    fixed_audience: Optional[np.ndarray] = None,
) -> np.ndarray:
    """Return the indicator g^X(t) as a boolean array of length N (spec §7.1).

    An inactive or silent actor returns an all-false indicator and consumes no
    randomness beyond what the repertoire would have used, because it is not
    called at all.

    `fixed_audience` supplies the permanent subset the `fixed_random` repertoire
    addresses; it is computed once per run from (seed, actor) rather than drawn
    here, so that it is identical across the four arms of the 2x2.
    """
    n_agents = positions.size
    chosen = np.zeros(n_agents, dtype=bool)

    if not actor.is_active(step):
        return chosen

    n_targets = actor.n_targets(n_agents)
    if n_targets == 0:
        return chosen

    if actor.repertoire is Repertoire.RANDOM:
        picks = rng.choice(n_agents, size=n_targets, replace=False)
    elif actor.repertoire is Repertoire.FIXED_RANDOM:
        if fixed_audience is None:
            raise ValueError("the fixed_random repertoire needs a precomputed audience")
        picks = fixed_audience
    elif actor.repertoire is Repertoire.HUB:
        # highest degree == lowest negative degree
        picks = _lowest_n(-degree.astype(float), n_targets, rng)
    elif actor.repertoire is Repertoire.BASE:
        picks = _lowest_n(np.abs(positions - actor.pole), n_targets, rng)
    else:
        raise ValueError(f"unknown repertoire: {actor.repertoire}")

    chosen[picks] = True
    return chosen
