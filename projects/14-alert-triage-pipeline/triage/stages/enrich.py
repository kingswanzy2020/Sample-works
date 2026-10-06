"""TODO (you): add the context a first-line responder needs, to each record.

Ideas (decide which matter, ADR-0001): owner and on-call, tier, runbook link (and whether it's stale),
dependencies and their current health, a dashboard link, recent deploys, related active alerts.

Constraint: enrichment must never block or drop an alert. If a source is slow or down, note it and move on.
"""
from triage.models import TriageRecord


def enrich(record: TriageRecord, catalog: dict[str, dict]) -> TriageRecord:
    return record
