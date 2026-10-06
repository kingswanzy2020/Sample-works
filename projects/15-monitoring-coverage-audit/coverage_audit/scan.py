"""Scan every catalog service against monitoring-standard.yaml.

    python -m coverage_audit.scan                 # table
    python -m coverage_audit.scan --json report.json

Result per check: PASS, FAIL, or TODO (check not implemented). How the exit code should behave
(always 0? non-zero on tier-1 gaps?) is ADR-0003, so the starter always exits 0.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import yaml

from coverage_audit import sources
from coverage_audit.checks import REGISTRY


def required_checks(entry: dict, standard: dict) -> list[str]:
    if entry.get("kind") == "platform":
        return standard.get("required_for_platform") or []
    return (standard.get("required_by_tier") or {}).get(entry.get("tier"), []) or []


def scan(standard: dict) -> list[dict]:
    rows, ctx = [], {"standard": standard}
    for name, entry in sources.catalog().items():
        for check_id in required_checks(entry, standard):
            fn = REGISTRY.get(check_id)
            if fn is None:
                rows.append({"service": name, "tier": entry.get("tier"), "check": check_id,
                             "result": "TODO", "detail": "unknown check id"})
                continue
            try:
                passed, detail = fn(name, entry, ctx)
            except Exception as exc:  # a broken check must not hide the others
                passed, detail = False, f"check error: {exc}"
            result = "TODO" if passed is None else ("PASS" if passed else "FAIL")
            rows.append({"service": name, "tier": entry.get("tier"), "check": check_id,
                         "result": result, "detail": detail})
    return rows


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--standard", default="monitoring-standard.yaml")
    p.add_argument("--json")
    a = p.parse_args(argv)
    standard = yaml.safe_load(pathlib.Path(a.standard).read_text())
    rows = scan(standard)
    if not rows:
        print("No checks required yet. Fill in required_by_tier in monitoring-standard.yaml (ADR-0001).")
    for r in rows:
        print(f"{r['result']:4} tier{r['tier']} {r['service']:16} {r['check']:20} {r['detail']}")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(rows, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
