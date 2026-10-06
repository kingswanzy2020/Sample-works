"""TODO (you): decide who gets this, based on ownership and severity (ADR-0001 / project 12's on-call design).

What happens to alerts for services with no owner (risk-engine)? That's a decision, not a default.
"""
from triage.models import TriageRecord


def route(record: TriageRecord, catalog: dict[str, dict]) -> TriageRecord:
    record.routed_to = "default"
    return record
