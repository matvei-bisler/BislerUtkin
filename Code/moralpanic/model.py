"""The model: four rules, synchronous updating (spec §6, §7).

Everything dated t+1 is computed from quantities dated t. In particular the
othering exposure Phi_i(t) reads b(t), never the freshly computed b(t+1), so
all time-t quantities are evaluated before either state array is written.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import networkx as nx
import numpy as np

from .actors import select_targets
from .config import (
    SOFT_CORE,
    BoundMode,
    ExposureMode,
    PositionRegime,
    Repertoire,
    RunConfig,
    ThresholdRegime,
    UpdateOrder,
)
from .measures import StepRecord, measure_step
from .network import Neighbourhood, build_graph, structural_summary
from .rng import Streams


# --------------------------------------------------------------------------- #
# The soft bound of the artifact check (spec §14.2)
# --------------------------------------------------------------------------- #


def soft_bound(raw: np.ndarray, core: float = SOFT_CORE) -> np.ndarray:
    """The identity on [-core, core], with a tanh knee beyond it.

        f(x) = x                                        for |x| <= core
        f(x) = sign(x) (core + (1-core) tanh(u)),  u = (|x| - core)/(1 - core)

    Continuous and continuously differentiable at the join, since the knee's
    slope there is sech^2(0) = 1; strictly inside (-1, 1) everywhere, so no
    boundary atom can form; and the identity wherever the hard clip would not
    have bound, so the replication changes the dynamics only where the artifact
    lives. A plain tanh would instead contract the whole interior toward zero and
    dissolve manufactured division for reasons unrelated to the boundary.
    """
    magnitude = np.abs(raw)
    knee = core + (1.0 - core) * np.tanh(
        (magnitude - core) / (1.0 - core), where=magnitude > core, out=np.zeros_like(magnitude)
    )
    # float64 tanh saturates at exactly 1.0 once its argument passes about 19,
    # i.e. |raw| > 2.9, which would quietly put an atom back on the pole. The
    # clamp keeps the map strictly interior for every representable input.
    knee = np.minimum(knee, 1.0 - 1e-12)
    return np.where(magnitude <= core, raw, np.sign(raw) * knee)


# --------------------------------------------------------------------------- #
# Initialization (spec §8)
# --------------------------------------------------------------------------- #


def draw_positions(regime: PositionRegime, n: int, rng: np.random.Generator) -> np.ndarray:
    """Initial positions b_i(0), also retained as each agent's anchor (spec §8).

    The polarized regime is truncated BY REJECTION, never by clipping: clipping
    a Normal onto [-1, 1] leaves point atoms at the bounds that are
    indistinguishable from the boundary pile-up the dynamics produce (spec §8,
    §14.2).
    """
    if regime is PositionRegime.CONSENSUAL:
        return rng.uniform(-0.2, 0.2, size=n)

    if regime is PositionRegime.POLARIZED:
        centres = rng.choice(np.array([-0.7, 0.7]), size=n)
        draws = np.empty(n)
        pending = np.arange(n)
        while pending.size:
            candidate = rng.normal(centres[pending], 0.15)
            accepted = np.abs(candidate) <= 1.0
            draws[pending[accepted]] = candidate[accepted]
            pending = pending[~accepted]
        return draws

    raise ValueError(f"unknown position regime: {regime}")


def draw_thresholds(regime: ThresholdRegime, n: int, rng: np.random.Generator) -> np.ndarray:
    """Panic thresholds theta_i, the model's only heterogeneous trait (spec §2.2)."""
    if regime is ThresholdRegime.DISPERSED:
        return rng.uniform(0.0, 1.0, size=n)
    if regime is ThresholdRegime.UNIFORM:
        return np.full(n, 0.5)
    raise ValueError(f"unknown threshold regime: {regime}")


@dataclass
class InitialState:
    """The step-0 state shared by all four runs of a counterfactual set (spec §10.1)."""

    graph: nx.Graph
    positions: np.ndarray
    alarm: np.ndarray
    thresholds: np.ndarray
    structure: Dict[str, float] = field(default_factory=dict)

    def fingerprint(self) -> tuple:
        """A cheap identity check asserted across the 2x2 runs (spec §15)."""
        return (
            self.graph.number_of_nodes(),
            self.graph.number_of_edges(),
            float(self.positions.sum()),
            float(self.alarm.sum()),
            float(self.thresholds.sum()),
        )


def initialise(config: RunConfig, streams: Streams) -> InitialState:
    """Build the network and draw all agent state from the `setup` stream.

    The population is read off the realised graph rather than off the config,
    because an empirical edge list (spec §12.3) fixes N itself.
    """
    graph = build_graph(config.network, streams)
    n = graph.number_of_nodes()
    positions = draw_positions(config.position_regime, n, streams.setup)
    alarm = streams.setup.uniform(0.0, config.initial_alarm_max, size=n)
    thresholds = draw_thresholds(config.threshold_regime, n, streams.setup)
    return InitialState(graph, positions, alarm, thresholds, structural_summary(graph))


# --------------------------------------------------------------------------- #
# Run result
# --------------------------------------------------------------------------- #


@dataclass
class RunResult:
    """One trajectory, plus the structural statistics and seed behind it."""

    config: RunConfig
    structure: Dict[str, float]
    records: List[StepRecord]
    positions_final: np.ndarray
    alarm_final: np.ndarray
    reach_counts_d: np.ndarray = field(default_factory=lambda: np.zeros(0))
    position_states: Optional[np.ndarray] = None
    alarm_states: Optional[np.ndarray] = None

    def series(self, name: str) -> np.ndarray:
        return np.array([getattr(record, name) for record in self.records], dtype=float)

    @property
    def n_steps(self) -> int:
        return len(self.records)


# --------------------------------------------------------------------------- #
# The model
# --------------------------------------------------------------------------- #


class Model:
    """One trajectory of the moral panic model.

    Usage::

        streams = Streams.from_seed(config.seed)
        result = Model(config, streams).run()
    """

    def __init__(
        self,
        config: RunConfig,
        streams: Streams,
        initial: Optional[InitialState] = None,
    ) -> None:
        self.config = config
        self.streams = streams
        self.initial = initial if initial is not None else initialise(config, streams)

        self.neighbourhood = Neighbourhood.from_graph(self.initial.graph)
        self.positions = self.initial.positions.copy()
        self.alarm = self.initial.alarm.copy()
        self.anchor = self.initial.positions.copy()  # b_i(0), fixed for the run
        self.thresholds = self.initial.thresholds.copy()

        self._degree = self.neighbourhood.degree
        self._degree_positive = self._degree > 0
        self._offsets = (
            self.neighbourhood.adjacency_index()
            if config.update_order is UpdateOrder.ASYNCHRONOUS
            else None
        )
        # the permanent audience of the `fixed_random` repertoire (spec §7.1),
        # computed once per run and identical across the arms of the 2x2
        self._fixed_audience = {
            name: (
                streams.fixed_audience(name, self.neighbourhood.n_agents,
                                       actor.n_targets(self.neighbourhood.n_agents))
                if actor.repertoire is Repertoire.FIXED_RANDOM
                else None
            )
            for name, actor in (("D", config.actor_d), ("C", config.actor_c))
        }
        self.step_index = 0
        self.clip_events = 0
        # cumulative per-agent exposure to D, for the concentration measure (spec §10.3)
        self.reach_counts_d = np.zeros(self.neighbourhood.n_agents, dtype=np.int64)

    # -- derived quantities (spec §2.3) ------------------------------------ #

    def social_weight(self) -> np.ndarray:
        """kappa_i(t): gamma when past threshold, 1 otherwise (spec §2.3)."""
        amplifying = self.alarm > self.thresholds
        return np.where(amplifying, self.config.constants.gamma, 1.0)

    # -- the four rules ---------------------------------------------------- #

    def _neighbour_sums(self, kappa: np.ndarray) -> Dict[str, np.ndarray]:
        """Aggregate the three neighbour sums in one pass over the edge list.

        Returns the raw numerators of S_i (spec §7.2), Phi_i and the peer part
        of E_i (spec §7.4), plus the shared denominator sum_j kappa_j.
        """
        n = self.neighbourhood.n_agents
        zeros = np.zeros(n)
        if not self.neighbourhood.has_edges:
            return {"pull": zeros, "distance": zeros, "alarm": zeros, "weight": zeros}

        src = self.neighbourhood.source
        dst = self.neighbourhood.target
        w = kappa[dst]

        gap = self.positions[dst] - self.positions[src]
        distance = np.abs(gap)
        within = distance <= self.config.parameters.epsilon

        return {
            "pull": np.bincount(src, weights=w * within * gap, minlength=n),
            "distance": np.bincount(src, weights=w * distance / 2.0, minlength=n),
            "alarm": np.bincount(src, weights=w * self.alarm[dst], minlength=n),
            "weight": np.bincount(src, weights=w, minlength=n),
        }

    def _targets(self) -> Dict[str, np.ndarray]:
        """g^D(t) and g^C(t) (spec §7.1)."""
        return {
            name: select_targets(
                actor,
                self.step_index,
                self.positions,
                self._degree,
                self.streams.targeting,
                self._fixed_audience[name],
            )
            for name, actor in (("D", self.config.actor_d), ("C", self.config.actor_c))
        }

    def _bound(self, raw: np.ndarray) -> np.ndarray:
        """Keep positions inside [-1, 1] (spec §7.3), counting where it binds.

        Under CLIP the count is the number of agents the clip actually moved,
        which is the diagnostic spec §14.2 (1) asks to report. Under TANH nothing
        is ever pinned, so no atom forms and the count stays zero.
        """
        if self.config.bound_mode is BoundMode.TANH:
            return soft_bound(raw)
        self.clip_events += int(np.count_nonzero(np.abs(raw) > 1.0))
        return np.clip(raw, -1.0, 1.0)

    def step(self) -> StepRecord:
        """Advance one step and return the measurements taken at time t.

        The record describes the state at the START of the step, so a run of T
        steps yields T records covering t = 0 .. T-1.
        """
        if self.config.update_order is UpdateOrder.ASYNCHRONOUS:
            return self._step_asynchronous()
        params = self.config.parameters
        consts = self.config.constants

        # --- all time-t quantities, evaluated before anything is written ---
        kappa = self.social_weight()
        targets = self._targets()
        reached_d = targets["D"]
        reached_c = targets["C"]
        m = reached_d.astype(float) + reached_c.astype(float)
        self.reach_counts_d += reached_d

        sums = self._neighbour_sums(kappa)
        weight = sums["weight"]
        safe_weight = np.where(self._degree_positive, weight, 1.0)

        # peer pull S_i (spec §7.2); zero for isolates
        pull = np.where(self._degree_positive, sums["pull"] / safe_weight, 0.0)

        # othering exposure Phi_i (spec §7.4); zero for isolates
        othering = np.where(self._degree_positive, sums["distance"] / safe_weight, 0.0)

        # alarm exposure E_i (spec §7.4); a claims-maker enters as one
        # maximally alarmed, permanently amplifying contact
        exposure_numer = sums["alarm"] + consts.gamma * m
        if self.config.exposure_mode is ExposureMode.REINFORCING:
            # divide by the neighbour COUNT: amplifying neighbours add rather
            # than re-weight, so E_i can exceed every individual a_j
            exposure_denom = self._degree.astype(float) + m
        else:
            exposure_denom = weight + consts.gamma * m
        present = exposure_denom > 0.0
        exposure = np.where(
            present, exposure_numer / np.where(present, exposure_denom, 1.0), 0.0
        )
        if self.config.exposure_mode is ExposureMode.REINFORCING:
            exposure = np.clip(exposure, 0.0, 1.0)

        record = measure_step(
            step=self.step_index,
            positions=self.positions,
            alarm=self.alarm,
            thresholds=self.thresholds,
            othering=othering,
            neighbourhood=self.neighbourhood,
            reached_d=reached_d,
        )

        # --- position update (spec §7.3) ---
        push_d = self.config.actor_d.alpha * reached_d * (1.0 - self.positions)
        push_c = self.config.actor_c.alpha * reached_c * (1.0 + self.positions)
        noise = (
            self.streams.noise.normal(0.0, consts.zeta, size=self.positions.size)
            if consts.zeta > 0.0
            else 0.0
        )
        raw_positions = (
            consts.sigma * self.anchor
            + (1.0 - consts.sigma) * (self.positions + pull + push_d - push_c)
            + noise
        )
        new_positions = self._bound(raw_positions)

        # --- alarm update (spec §7.4) ---
        raw_alarm = params.mu * self.alarm + params.delta * exposure + params.omega * othering
        new_alarm = np.clip(raw_alarm, 0.0, 1.0)

        self.positions = new_positions
        self.alarm = new_alarm
        self.step_index += 1
        return record

    # -- asynchronous updating (spec §12.3) -------------------------------- #

    def _step_asynchronous(self) -> StepRecord:
        """One random-order sequential sweep, as the appendix check on §6.

        Agents are visited in a fresh random order and each writes immediately,
        so later agents read some already-updated neighbours. Targeting is still
        decided once per step from the step-start state: re-deciding it inside
        the sweep would give the actors within-step information the synchronous
        scheme does not, and the check is meant to isolate the update order.

        The sweep order is derived from (seed, step) through its own throwaway
        generator rather than from any of the three streams. Drawing it from
        `targeting` would desynchronise it across the arms of the 2x2, because
        the silent arms consume no targeting draws; drawing it from `noise` would
        desynchronise the noise itself. Both would break the common random
        numbers the counterfactual rests on (spec §15).
        """
        params = self.config.parameters
        consts = self.config.constants
        gamma = consts.gamma

        targets = self._targets()
        reached_d, reached_c = targets["D"], targets["C"]
        self.reach_counts_d += reached_d
        m_all = reached_d.astype(float) + reached_c.astype(float)

        # measurements describe the state at the START of the step, exactly as
        # in the synchronous path, so the two are comparable record for record
        kappa = self.social_weight()
        sums = self._neighbour_sums(kappa)
        weight = np.where(self._degree_positive, sums["weight"], 1.0)
        othering_now = np.where(self._degree_positive, sums["distance"] / weight, 0.0)
        record = measure_step(
            step=self.step_index,
            positions=self.positions,
            alarm=self.alarm,
            thresholds=self.thresholds,
            othering=othering_now,
            neighbourhood=self.neighbourhood,
            reached_d=reached_d,
        )

        offsets = self._offsets
        neighbours = self.neighbourhood.target
        positions, alarm, thresholds = self.positions, self.alarm, self.thresholds
        alpha_d = self.config.actor_d.alpha
        alpha_c = self.config.actor_c.alpha
        epsilon = params.epsilon
        noise = (
            self.streams.noise.normal(0.0, consts.zeta, size=positions.size)
            if consts.zeta > 0.0
            else np.zeros(positions.size)
        )
        order = self.streams.sweep_order(self.step_index, positions.size)

        for i in order:
            start, end = offsets[i], offsets[i + 1]
            degree = end - start
            m = m_all[i]
            b_i = positions[i]

            if degree:
                js = neighbours[start:end]
                b_j = positions[js]
                w = np.where(alarm[js] > thresholds[js], gamma, 1.0)
                gap = b_j - b_i
                distance = np.abs(gap)
                total = w.sum()
                pull = float((w * (distance <= epsilon) * gap).sum() / total)
                othering = float((w * distance / 2.0).sum() / total)
                neighbour_alarm = float((w * alarm[js]).sum())
            else:
                pull = othering = neighbour_alarm = 0.0
                total = 0.0

            if self.config.exposure_mode is ExposureMode.REINFORCING:
                denominator = degree + m
                exposure = (
                    min(1.0, (neighbour_alarm + gamma * m) / denominator)
                    if denominator > 0.0
                    else 0.0
                )
            else:
                denominator = total + gamma * m
                exposure = (
                    (neighbour_alarm + gamma * m) / denominator if denominator > 0.0 else 0.0
                )

            raw = (
                consts.sigma * self.anchor[i]
                + (1.0 - consts.sigma)
                * (
                    b_i
                    + pull
                    + alpha_d * reached_d[i] * (1.0 - b_i)
                    - alpha_c * reached_c[i] * (1.0 + b_i)
                )
                + noise[i]
            )
            if self.config.bound_mode is BoundMode.TANH:
                positions[i] = float(soft_bound(np.array(raw)))
            else:
                if abs(raw) > 1.0:
                    self.clip_events += 1
                positions[i] = min(1.0, max(-1.0, raw))
            alarm[i] = min(
                1.0,
                max(0.0, params.mu * alarm[i] + params.delta * exposure + params.omega * othering),
            )

        self.step_index += 1
        return record

    def run(self) -> RunResult:
        """Run for `n_steps` steps and return the trajectory."""
        records: List[StepRecord] = []
        keep = self.config.record_states
        position_states = [] if keep else None
        alarm_states = [] if keep else None

        for _ in range(self.config.n_steps):
            if keep:
                position_states.append(self.positions.copy())
                alarm_states.append(self.alarm.copy())
            records.append(self.step())

        return RunResult(
            config=self.config,
            structure=dict(self.initial.structure, clip_events=self.clip_events),
            records=records,
            positions_final=self.positions.copy(),
            alarm_final=self.alarm.copy(),
            reach_counts_d=self.reach_counts_d.copy(),
            position_states=np.array(position_states) if keep else None,
            alarm_states=np.array(alarm_states) if keep else None,
        )
