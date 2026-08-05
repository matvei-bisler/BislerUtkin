#!/usr/bin/env python3
"""Run the verification limits and property checks (spec §12.3).

    python run_verification.py

Verification asks only whether the code implements the specification. It is
reported separately from any substantive result.
"""

import sys

from moralpanic.verification import run_all


def main() -> int:
    results = run_all()
    for result in results:
        print(result)
    passed = sum(r.passed for r in results)
    print(f"\n{passed}/{len(results)} checks passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
