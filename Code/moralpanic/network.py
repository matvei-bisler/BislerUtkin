"""Network generation and the edge structures the update rules consume (spec §4).

The model runs on the FULL generated graph, not the giant component: isolation
is substantively meaningful, because an agent reachable only by a claims-maker
is a real sociological position (spec §4).
"""

from __future__ import annotations

from dataclasses import dataclass

import networkx as nx
import numpy as np

from .config import NetworkSpec, Topology
from .rng import Streams


@dataclass(frozen=True)
class Neighbourhood:
    """Edge structure in the form the vectorised update rules need.

    Every undirected edge appears twice, once in each direction, so that a
    single ``np.bincount`` over ``source`` aggregates each agent's neighbours.

    source, target : int arrays of length 2|E|
    degree         : int array of length N
    """

    n_agents: int
    source: np.ndarray
    target: np.ndarray
    degree: np.ndarray

    @classmethod
    def from_graph(cls, graph: nx.Graph) -> "Neighbourhood":
        n = graph.number_of_nodes()
        if graph.number_of_edges() == 0:
            empty = np.empty(0, dtype=np.int64)
            return cls(n, empty, empty, np.zeros(n, dtype=np.int64))
        edges = np.asarray(graph.edges(), dtype=np.int64)
        source = np.concatenate([edges[:, 0], edges[:, 1]])
        target = np.concatenate([edges[:, 1], edges[:, 0]])
        order = np.argsort(source, kind="stable")  # grouped by source, for the CSR view
        source, target = source[order], target[order]
        degree = np.bincount(source, minlength=n).astype(np.int64)
        return cls(n, source, target, degree)

    @property
    def has_edges(self) -> bool:
        return self.source.size > 0

    def adjacency_index(self) -> np.ndarray:
        """CSR-style offsets into `target`, so agent i's neighbours are
        ``target[offsets[i]:offsets[i+1]]``.

        Needed only by the asynchronous update (spec §12.3), which cannot use
        the vectorised bincount path because each agent must read state that
        earlier agents in the sweep have already written.
        """
        offsets = np.zeros(self.n_agents + 1, dtype=np.int64)
        np.cumsum(self.degree, out=offsets[1:])
        return offsets

    def adjacency_row_stochastic(self) -> np.ndarray:
        """The matrix M of spec §7.3, used only by the verification limits.

        M[i, j] = 1/d_i for j adjacent to i, zero otherwise. Isolate rows are
        all zero.
        """
        matrix = np.zeros((self.n_agents, self.n_agents), dtype=float)
        if self.has_edges:
            matrix[self.source, self.target] = 1.0
        degree = self.degree.astype(float)
        safe = np.where(degree > 0, degree, 1.0)
        return matrix / safe[:, None]


def build_graph(spec: NetworkSpec, streams: Streams) -> nx.Graph:
    """Generate one of the three topologies at the requested mean degree.

    Watts-Strogatz and Holme-Kim take integer structural arguments, so the
    realised mean degree can differ slightly from the target. The realised
    value is recorded per run (spec §4) rather than assumed.
    """
    n = spec.n_agents
    seed = streams.integer_seed()

    if spec.topology is Topology.SMALL_WORLD:
        k = max(2, int(round(spec.mean_degree)))
        if k % 2:  # networkx requires an even ring degree
            k += 1
        k = min(k, n - 1 if (n - 1) % 2 == 0 else n - 2)
        return nx.watts_strogatz_graph(n, k, spec.rewiring_p, seed=seed)

    if spec.topology is Topology.HUB_DOMINATED:
        m = max(1, int(round(spec.mean_degree / 2.0)))
        m = min(m, n - 1)
        return nx.powerlaw_cluster_graph(n, m, spec.triad_p, seed=seed)

    if spec.topology is Topology.RANDOM_GRAPH:
        p = min(1.0, spec.mean_degree / (n - 1))
        return nx.fast_gnp_random_graph(n, p, seed=seed)

    if spec.topology is Topology.EMPIRICAL:
        return load_edge_list(spec.edge_list)

    if spec.topology is Topology.EMPTY:
        return empty_graph(n)

    raise ValueError(f"unknown topology: {spec.topology}")


def load_edge_list(path) -> nx.Graph:
    """Read an empirical network from a whitespace-separated edge list (spec §12.3).

    Lines beginning with ``#`` or ``%`` are skipped, which covers the SNAP and
    KONECT/Netzschleuder conventions. Node labels may be arbitrary integers; they
    are relabelled to 0..N-1 in sorted order, because every operator in the model
    indexes agents positionally.

    The graph enters as **fixed structure only** (spec §9): any node attributes
    the source carries are discarded and agent state is initialized exactly as in
    spec §8. Direction and multiplicity are dropped -- the model is defined on a
    static undirected simple graph -- and self-loops are removed, since an agent
    is not its own neighbour in any operator of §7.
    """
    from pathlib import Path

    file = Path(path)
    if not file.exists():
        raise FileNotFoundError(
            f"empirical edge list not found: {file}. "
            "Run `python fetch_empirical_network.py --list` to see the options."
        )

    opener = __import__("gzip").open if file.suffix == ".gz" else open
    graph = nx.Graph()
    with opener(file, "rt") as handle:
        for line in handle:
            line = line.strip()
            if not line or line[0] in "#%":
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            u, v = int(parts[0]), int(parts[1])
            if u != v:
                graph.add_edge(u, v)

    if graph.number_of_nodes() < 2:
        raise ValueError(f"{file} yielded fewer than two nodes")
    ordering = {node: index for index, node in enumerate(sorted(graph.nodes()))}
    return nx.relabel_nodes(graph, ordering, copy=True)


def empty_graph(n_agents: int) -> nx.Graph:
    """A graph with no edges, used by verification limit 5 (spec §12.3)."""
    graph = nx.Graph()
    graph.add_nodes_from(range(n_agents))
    return graph


def structural_summary(graph: nx.Graph) -> dict:
    """Per-run structural statistics recorded alongside every trajectory (spec §4)."""
    n = graph.number_of_nodes()
    degrees = np.array([d for _, d in graph.degree()], dtype=float)
    return {
        "n_agents": n,
        "n_edges": graph.number_of_edges(),
        "mean_degree": float(degrees.mean()) if n else 0.0,
        "clustering": float(nx.average_clustering(graph)) if graph.number_of_edges() else 0.0,
        "n_components": int(nx.number_connected_components(graph)) if n else 0,
        "isolate_fraction": float((degrees == 0).mean()) if n else 0.0,
    }
