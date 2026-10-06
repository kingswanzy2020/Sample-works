"""toil: guarded operational automation.

  python -m toil.cli list
  python -m toil.cli cert-expiry example.com github.com:443
  python -m toil.cli <action> ... --execute --max-targets 3
"""
import argparse
import pathlib
import sys

from toil.actions import ALL
from toil.framework import Runner


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="toil")
    parser.add_argument("--execute", action="store_true", help="actually make changes (default: dry-run)")
    parser.add_argument("--max-targets", type=int, default=5, help="refuse to change more targets than this")
    parser.add_argument("--audit-log", default="audit/toil-audit.jsonl")
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("list", help="list actions")
    actions = {a.name: a for a in ALL}
    for a in ALL:
        a.add_arguments(sub.add_parser(a.name, help=a.help))

    args = parser.parse_args(argv)
    if args.action == "list":
        for a in ALL:
            print(f"{a.name:26} {a.help}")
        return 0

    runner = Runner(pathlib.Path(args.audit_log), execute=args.execute, max_targets=args.max_targets)
    results = runner.run(actions[args.action], args)
    for r in results:
        print(f"{'OK ' if r.ok else 'ERR'} {r.target:30} {r.detail}")
    return 0 if all(r.ok for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
