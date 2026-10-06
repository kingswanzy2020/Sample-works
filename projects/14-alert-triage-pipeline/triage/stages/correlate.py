"""TODO (you): group alerts that share a root cause into one incident (ADR-0002).

The starter puts every alert in its own group: exactly the "30 pages for one Kafka problem" behaviour.
State lives in memory here; think about what happens to it when the service restarts.
"""
from triage.models import TriageRecord


def correlate(record: TriageRecord, catalog: dict[str, dict]) -> TriageRecord:
    record.group_id = record.fingerprint
    return record
