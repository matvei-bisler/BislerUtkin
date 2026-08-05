#!/usr/bin/env python3
"""Retrieve the empirical network used by the appendix replication (spec §12.3).

    python fetch_empirical_network.py --list
    python fetch_empirical_network.py ego-facebook
    python fetch_empirical_network.py ego-facebook --describe   # no download

The spec asks for "one empirical network (a platform ego-network or friendship
graph from a public repository, Leskovec & Krevl 2014), reported with its source,
retrieval date, size, mean degree and clustering". This script performs the
retrieval and writes a provenance record next to the edge list, so the appendix
table can name where the graph came from and when.

The graph enters as **fixed structure only** (spec §9). Node attributes, edge
direction, weights and timestamps are all discarded; agent state is initialized
exactly as in spec §8.

Nothing is downloaded unless a dataset is named on the command line.
"""

from __future__ import annotations

import argparse
import datetime as dt
import gzip
import hashlib
import json
import shutil
import sys
import urllib.request
from pathlib import Path
from typing import Dict

DATA_DIR = Path(__file__).resolve().parent / "networks"

# --------------------------------------------------------------------------- #
# The registry
# --------------------------------------------------------------------------- #

DATASETS: Dict[str, Dict[str, object]] = {
    "ego-facebook": {
        "url": "https://snap.stanford.edu/data/facebook_combined.txt.gz",
        "filename": "facebook_combined.txt",
        "repository": "SNAP (Leskovec & Krevl 2014)",
        "citation": "Leskovec, J. & McAuley, J. (2012). Learning to discover social "
                    "circles in ego networks. NIPS 25.",
        "page": "https://snap.stanford.edu/data/ego-Facebook.html",
        "kind": "platform ego-network (Facebook friendship circles, anonymised)",
        "expected": {"nodes": 4039, "edges": 88234, "mean_degree": 43.7,
                     "clustering": 0.606, "components": 1},
        "why": (
            "The spec's own example, and the canonical instance of the type. Ten "
            "ego-networks merged: a locally dense, globally connected social world, "
            "which is what the Watts-Strogatz generator idealises. Its mean degree "
            "is 4x the operating point, so it brackets the sweep from above."
        ),
    },
    "ca-grqc": {
        "url": "https://snap.stanford.edu/data/ca-GrQc.txt.gz",
        "filename": "ca-GrQc.txt",
        "repository": "SNAP (Leskovec & Krevl 2014)",
        "citation": "Leskovec, J., Kleinberg, J. & Faloutsos, C. (2007). Graph "
                    "evolution: densification and shrinking diameters. ACM TKDD 1(1).",
        "page": "https://snap.stanford.edu/data/ca-GrQc.html",
        "kind": "collaboration network (arXiv General Relativity co-authorship)",
        "expected": {"nodes": 5242, "edges": 14496, "mean_degree": 5.53,
                     "clustering": 0.530, "components": 355},
        "why": (
            "Brackets the operating point from below at mean degree 5.5, and is the "
            "only candidate with substantial component structure -- 355 components. "
            "The model runs on the full graph rather than the giant component "
            "precisely because isolation is substantively meaningful (spec §4), so "
            "this is the case that exercises that choice."
        ),
    },
    "email-eu-core": {
        "url": "https://snap.stanford.edu/data/email-Eu-core.txt.gz",
        "filename": "email-Eu-core.txt",
        "repository": "SNAP (Leskovec & Krevl 2014)",
        "citation": "Yin, H., Benson, A. R., Leskovec, J. & Gleich, D. F. (2017). "
                    "Local higher-order graph clustering. KDD.",
        "page": "https://snap.stanford.edu/data/email-Eu-core.html",
        "kind": "institutional communication network (European research institution)",
        "expected": {"nodes": 1005, "edges": 16064, "mean_degree": 32.0,
                     "clustering": 0.399, "components": 20},
        "why": (
            "N = 1005 matches the headline population almost exactly, so the "
            "empirical replication and the headline runs differ in structure and "
            "not in size. Directed in the source; direction is discarded, which is "
            "a real simplification and should be reported as one."
        ),
    },
}

RECOMMENDED = ("ego-facebook", "ca-grqc")
"""Two networks rather than one, chosen to bracket the operating point.

The appendix needs to show that the headline conclusions are not an artifact of
the generators. One empirical graph cannot do that on its own, because any single
network differs from the generators in size, density and clustering at once. Two
that sit on opposite sides of the operating mean degree (5.5 and 43.7) separate a
density effect from a structure effect at no extra conceptual cost, and the
generators are re-run matched to each (see `appendix.check_empirical_network`).
"""


# --------------------------------------------------------------------------- #
# Retrieval
# --------------------------------------------------------------------------- #


def describe(name: str) -> None:
    entry = DATASETS[name]
    print(f"\n{name}")
    print(f"  kind        {entry['kind']}")
    print(f"  repository  {entry['repository']}")
    print(f"  page        {entry['page']}")
    print(f"  url         {entry['url']}")
    expected = entry["expected"]
    print(f"  expected    N = {expected['nodes']}, E = {expected['edges']}, "
          f"<k> = {expected['mean_degree']}, C = {expected['clustering']}, "
          f"components = {expected['components']}")
    print(f"  citation    {entry['citation']}")
    print(f"  why         {entry['why']}")


def fetch(name: str, force: bool = False) -> Path:
    """Download one dataset, decompress it, and write a provenance record."""
    entry = DATASETS[name]
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    target = DATA_DIR / str(entry["filename"])

    if target.exists() and not force:
        print(f"{target} already present; pass --force to re-download")
        return target

    url = str(entry["url"])
    print(f"downloading {url}")
    archive = DATA_DIR / (target.name + ".gz")
    with urllib.request.urlopen(url, timeout=120) as response, archive.open("wb") as handle:
        shutil.copyfileobj(response, handle)
    with gzip.open(archive, "rb") as source, target.open("wb") as handle:
        shutil.copyfileobj(source, handle)
    archive.unlink()

    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    provenance = {
        "dataset": name,
        "url": url,
        "page": entry["page"],
        "repository": entry["repository"],
        "citation": entry["citation"],
        "kind": entry["kind"],
        "retrieved": dt.date.today().isoformat(),
        "sha256": digest,
        "bytes": target.stat().st_size,
    }

    try:  # report the realised structure, which is what the appendix must cite
        from moralpanic.network import load_edge_list, structural_summary

        summary = structural_summary(load_edge_list(target))
        provenance["realised"] = {k: (float(v) if isinstance(v, float) else int(v))
                                  for k, v in summary.items()}
        print(f"  N = {summary['n_agents']}, E = {summary['n_edges']}, "
              f"<k> = {summary['mean_degree']:.2f}, C = {summary['clustering']:.3f}, "
              f"components = {summary['n_components']}, "
              f"isolates = {summary['isolate_fraction']:.3f}")
    except Exception as error:  # pragma: no cover - provenance still gets written
        print(f"  (could not summarise: {error})")

    (DATA_DIR / f"{name}.provenance.json").write_text(json.dumps(provenance, indent=2))
    print(f"wrote {target} and its provenance record")
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("dataset", nargs="?", choices=sorted(DATASETS), default=None)
    parser.add_argument("--list", action="store_true", help="describe every option and exit")
    parser.add_argument("--describe", action="store_true", help="describe one option and exit")
    parser.add_argument("--force", action="store_true", help="re-download if present")
    args = parser.parse_args()

    if args.list or args.dataset is None:
        print(__doc__.split("\n\n")[0])
        for name in DATASETS:
            describe(name)
        print(f"\nrecommended for the appendix: {', '.join(RECOMMENDED)}")
        print(RECOMMENDED.__doc__ if hasattr(RECOMMENDED, "__doc__") else "")
        print("\nNothing was downloaded. Name a dataset to retrieve it.")
        return 0

    if args.describe:
        describe(args.dataset)
        return 0

    fetch(args.dataset, force=args.force)
    return 0


if __name__ == "__main__":
    sys.exit(main())
