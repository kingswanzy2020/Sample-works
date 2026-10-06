"""Loads the landscape service catalog. Plumbing only; what you DO with it is the project."""
from __future__ import annotations

import os
import pathlib

import yaml

DEFAULT = pathlib.Path(__file__).resolve().parents[1] / "landscape" / "catalog.yaml"
# Inside the roadmap repo, the landscape lives three levels up.
FALLBACK = pathlib.Path(__file__).resolve().parents[3] / "landscape" / "catalog.yaml"


def load(path: str | None = None) -> dict[str, dict]:
    candidates = [pathlib.Path(p) for p in [path or os.getenv("CATALOG", "")] if p] + [DEFAULT, FALLBACK]
    for c in candidates:
        if c.exists():
            return {s["name"]: s for s in yaml.safe_load(c.read_text())["services"]}
    raise FileNotFoundError(f"catalog.yaml not found in {[str(c) for c in candidates]}")
