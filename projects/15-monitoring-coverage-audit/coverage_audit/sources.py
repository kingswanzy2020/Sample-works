"""Where the scanner gets its facts. Plumbing: queries, not judgement."""
from __future__ import annotations

import json
import os
import pathlib
import urllib.parse
import urllib.request

import yaml

PROMETHEUS = os.getenv("PROMETHEUS_URL", "http://localhost:9090")
_HERE = pathlib.Path(__file__).resolve()
CATALOG_CANDIDATES = [
    pathlib.Path(os.getenv("CATALOG", "")),
    _HERE.parents[1] / "landscape" / "catalog.yaml",   # extracted repo
    _HERE.parents[3] / "landscape" / "catalog.yaml",   # roadmap repo
]


def catalog() -> dict[str, dict]:
    for c in CATALOG_CANDIDATES:
        if str(c) not in ("", ".") and c.exists():
            return {s["name"]: s for s in yaml.safe_load(c.read_text())["services"]}
    raise FileNotFoundError("landscape/catalog.yaml not found; set CATALOG")


def prom_query(expr: str) -> list[dict]:
    url = f"{PROMETHEUS}/api/v1/query?" + urllib.parse.urlencode({"query": expr})
    with urllib.request.urlopen(url, timeout=5) as r:
        return json.load(r)["data"]["result"]


def prom_rules() -> list[dict]:
    """Every alerting and recording rule Prometheus has loaded, flattened."""
    with urllib.request.urlopen(f"{PROMETHEUS}/api/v1/rules", timeout=5) as r:
        groups = json.load(r)["data"]["groups"]
    return [rule for g in groups for rule in g["rules"]]
