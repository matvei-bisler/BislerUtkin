"""Random number discipline (spec §8, §15).

Three independent named streams are spawned from one recorded seed:

    setup     -- network, initial positions, initial alarm, thresholds
    targeting -- `random` repertoire selection and tie-breaking
    noise     -- per-step idiosyncratic noise on positions

Keeping targeting and noise apart is not cosmetic. In the null and
othering-only runs of the 2x2 design the actors are silent, so no targeting
draws are consumed. If the two shared a stream, the noise sequence would
desynchronise between runs and the counterfactual comparison of spec §10.1
would no longer hold the same population fixed.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

_STREAM_NAMES = ("setup", "targeting", "noise")


@dataclass(frozen=True)
class Streams:
    """Independent PCG64 generators derived from a single seed."""

    seed: int
    setup: np.random.Generator
    targeting: np.random.Generator
    noise: np.random.Generator

    @classmethod
    def from_seed(cls, seed: int) -> "Streams":
        children = np.random.SeedSequence(seed).spawn(len(_STREAM_NAMES))
        generators = [np.random.Generator(np.random.PCG64(child)) for child in children]
        return cls(seed=seed, **dict(zip(_STREAM_NAMES, generators)))

    def integer_seed(self) -> int:
        """A deterministic integer for library calls that take `seed=` (networkx)."""
        return int(self.setup.integers(0, 2**31 - 1))

    _ACTOR_TAGS = {"D": 1, "C": 2}

    def fixed_audience(self, actor: str, n_agents: int, n_targets: int) -> np.ndarray:
        """The permanent audience of the `fixed_random` repertoire (spec §7.1).

        Derived from (seed, actor) through a throwaway generator, for the same
        reason as `sweep_order`: drawn from the `targeting` stream it would
        differ across the arms of the 2x2, because the silent arms consume no
        targeting draws, and the counterfactual would no longer hold the same
        population fixed.

        Audiences are **nested** in reach: the subset is the first `n_targets` of
        one permutation, so raising rho adds people rather than replacing them.
        That is what makes a sweep in reach a sweep in one thing.
        """
        tag = self._ACTOR_TAGS.get(actor, 0)
        entropy = np.random.SeedSequence([self.seed, 0xF1AED, tag])
        order = np.random.Generator(np.random.PCG64(entropy)).permutation(n_agents)
        return order[:n_targets]

    def sweep_order(self, step: int, n_agents: int) -> np.ndarray:
        """Agent visiting order for the asynchronous update (spec §12.3).

        Derived from (seed, step) through a throwaway generator rather than from
        any of the three streams. Taking it from `targeting` would desynchronise
        it across the arms of the 2x2 -- the silent arms consume no targeting
        draws -- and taking it from `noise` would desynchronise the noise. Either
        would break the common random numbers the counterfactual rests on.
        """
        entropy = np.random.SeedSequence([self.seed, 0xA5EDC, step])
        return np.random.Generator(np.random.PCG64(entropy)).permutation(n_agents)
