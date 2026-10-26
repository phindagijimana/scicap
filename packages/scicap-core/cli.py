"""scicap CLI. Default path is decide-only; --approve is a gated dry-run."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Sequence

from .invoke import invoke


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="scicap",
        description="SciCap invoke: bind scientific fields and return ALLOW/REJECT/ABSTAIN.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    invoke_p = sub.add_parser("invoke", help="Decide whether a capability may be invoked.")
    invoke_p.add_argument("capability", help="Path to capability YAML")
    invoke_p.add_argument("--instance", required=True, help="Path to instance JSON sidecar")
    invoke_p.add_argument(
        "--approve",
        action="store_true",
        help=(
            "Record approval and dry-run only: no container pull, "
            "executed=false, qc_status=did_not_run. Without this flag, do not execute."
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command != "invoke":
        parser.error("only invoke is implemented")
    try:
        result = invoke(args.capability, args.instance, approve=args.approve)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    json.dump(result, sys.stdout, indent=2, sort_keys=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
