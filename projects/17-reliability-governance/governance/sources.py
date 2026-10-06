"""Loaders for every input. Defaults point at sample-data/out; switch to real data with env vars:

TRIAGE_DIR     project 14's data/ (triage-log.jsonl, feedback.jsonl)
INCIDENTS_DIR  project 12's incidents/
CATALOG        landscape/catalog.yaml
"""

from __future__ import annotations

import json
import os
import pathlib

import yaml

_HERE = pathlib.Path(__file__).resolve()
SAMPLE = _HERE.parents[1] / "sample-data" / "out"


def _jsonl(path: pathlib.Path) -> list[dict]:
    return (
        [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.exists() else []
    )


def triage_log() -> list[dict]:
    return _jsonl(pathlib.Path(os.getenv("TRIAGE_DIR", SAMPLE)) / "triage-log.jsonl")


def feedback() -> list[dict]:
    return _jsonl(pathlib.Path(os.getenv("TRIAGE_DIR", SAMPLE)) / "feedback.jsonl")


def incidents() -> list[dict]:
    d = pathlib.Path(os.getenv("INCIDENTS_DIR", SAMPLE / "incidents"))
    return [yaml.safe_load(p.read_text()) for p in sorted(d.glob("*.yaml")) if p.name != "TEMPLATE.yaml"]


def catalog() -> dict[str, dict]:
    for p in [
        pathlib.Path(os.getenv("CATALOG", "")),
        _HERE.parents[1] / "landscape" / "catalog.yaml",
        _HERE.parents[3] / "landscape" / "catalog.yaml",
    ]:
        if str(p) not in ("", ".") and p.exists():
            return {s["name"]: s for s in yaml.safe_load(p.read_text())["services"]}
    raise FileNotFoundError("landscape/catalog.yaml not found; set CATALOG")
