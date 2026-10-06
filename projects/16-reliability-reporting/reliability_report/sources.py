"""Facts for the report: Prometheus, the catalog, and incident records from project 12. Plumbing only."""
from __future__ import annotations

import json
import os
import pathlib
import urllib.parse
import urllib.request

import yaml

PROMETHEUS = os.getenv("PROMETHEUS_URL", "http://localhost:9090")
_HERE = pathlib.Path(__file__).resolve()


def _first_existing(*paths: pathlib.Path) -> pathlib.Path:
    for p in paths:
        if str(p) not in ("", ".") and p.exists():
            return p
    raise FileNotFoundError(f"none of {[str(p) for p in paths]} exist")


def catalog() -> dict[str, dict]:
    path = _first_existing(pathlib.Path(os.getenv("CATALOG", "")),
                           _HERE.parents[1] / "landscape" / "catalog.yaml",
                           _HERE.parents[3] / "landscape" / "catalog.yaml")
    return {s["name"]: s for s in yaml.safe_load(path.read_text())["services"]}


def incidents() -> list[dict]:
    """Incident records (project 12 schema). Set INCIDENTS_DIR to point at project 12's incidents/."""
    d = pathlib.Path(os.getenv("INCIDENTS_DIR", _HERE.parents[2] / "12-incident-response" / "incidents"))
    if not d.exists():
        return []
    return [yaml.safe_load(p.read_text()) for p in sorted(d.glob("*.yaml")) if p.name != "TEMPLATE.yaml"]


def prom_scalar(expr: str) -> float | None:
    url = f"{PROMETHEUS}/api/v1/query?" + urllib.parse.urlencode({"query": expr})
    with urllib.request.urlopen(url, timeout=10) as r:
        result = json.load(r)["data"]["result"]
    return float(result[0]["value"][1]) if result else None
