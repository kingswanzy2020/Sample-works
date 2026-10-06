"""Build the report. The starter renders a plain table; who reads it, and what they need, is ADR-0005."""
from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import sys

import yaml

from reliability_report.slo import evaluate


def fmt_pct(x: float | None) -> str:
    return "no data" if x is None else f"{x * 100:.3f}%"


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--slos", default="slos/slos.yaml")
    p.add_argument("--out", help="write markdown here (e.g. reports/2026-W41.md)")
    a = p.parse_args(argv)

    slos = yaml.safe_load(pathlib.Path(a.slos).read_text())["slos"]
    lines = [f"# Reliability report ({dt.date.today().isoformat()})", "",
             "| Service | SLO | Objective | Actual | Budget left | Met? |",
             "|---------|-----|-----------|--------|-------------|------|"]
    for slo in slos:
        try:
            r = evaluate(slo)
            met = {True: "yes", False: "**NO**", None: "unknown"}[r.met]
            budget = "n/a" if r.budget_remaining is None else f"{r.budget_remaining * 100:.0f}%"
            lines.append(f"| {r.service} | {r.name} | {fmt_pct(r.objective)} | {fmt_pct(r.actual)} "
                         f"| {budget} | {met} |")
        except NotImplementedError as exc:
            lines.append(f"| {slo['service']} | {slo['name']} | {fmt_pct(slo['objective'])} "
                         f"| not implemented | | ({exc}) |")
    text = "\n".join(lines) + "\n"
    print(text)
    if a.out:
        pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(a.out).write_text(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
