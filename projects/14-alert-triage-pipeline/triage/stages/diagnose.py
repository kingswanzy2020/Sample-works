"""TODO (you): run READ-ONLY diagnostics and attach the results (ADR-0003).

Examples: dependency health from Prometheus, the simulator's /state, consumer lag (project 09),
or project 13's read-only toil actions. Anything that CHANGES the system is outside this stage
unless ADR-0003 says otherwise.
"""
from triage.models import TriageRecord


def diagnose(record: TriageRecord, catalog: dict[str, dict]) -> TriageRecord:
    return record
