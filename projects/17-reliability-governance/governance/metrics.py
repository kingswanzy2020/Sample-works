"""Governance metrics. One is implemented as an example.
Choosing and defining the rest is the project (ADR-0001).

Every metric returns a list of FINDINGS: {"service", "owner", "metric", "value", "detail"}.
A finding should be specific enough that the owning team knows exactly what to fix.
"""

from __future__ import annotations


def ownership_gaps(catalog: dict[str, dict]) -> list[dict]:
    """Example: services with no owner or no on-call."""
    findings = []
    for name, s in catalog.items():
        missing = [field for field in ("owner", "oncall") if not s.get(field)]
        if missing:
            findings.append(
                {
                    "service": name,
                    "owner": s.get("owner") or "(none)",
                    "metric": "ownership_gap",
                    "value": len(missing),
                    "detail": f"missing: {', '.join(missing)} (tier {s.get('tier')})",
                }
            )
    return findings


def alert_quality(triage_log: list[dict], feedback: list[dict], catalog: dict[str, dict]) -> list[dict]:
    """TODO (you): noisy and non-actionable alerts, per alert and per owner.

    Ideas to define precisely: actionable %, alerts per week, pages per on-call shift,
    alerts with no feedback at all, alerts routed nowhere.
    """
    raise NotImplementedError


def runbook_quality(incidents: list[dict], catalog: dict[str, dict], max_age_days: int = 180) -> list[dict]:
    """TODO (you): missing, stale, and unhelpful runbooks (did it help when it was used?)."""
    raise NotImplementedError


def action_followthrough(incidents: list[dict], today: str) -> list[dict]:
    """TODO (you): overdue and unowned postmortem actions, and repeat incidents with the same root cause."""
    raise NotImplementedError


def slo_misses(slo_results: list[dict]) -> list[dict]:
    """TODO (you): missed SLOs per owner, from project 16's output.

    Agree the format with yourself in project 16's Phase 6.
    """
    raise NotImplementedError
