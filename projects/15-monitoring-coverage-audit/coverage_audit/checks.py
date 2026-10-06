"""Coverage checks. Each takes (service_name, catalog_entry, context) and returns (passed, detail).

One example is implemented. The rest are stubs: deciding what "passes" means IS the project.
"""
from __future__ import annotations

from coverage_audit import sources


def has_metrics(name, entry, ctx):
    result = sources.prom_query(f'count(svc_requests_total{{service="{name}"}})')
    found = bool(result) and float(result[0]["value"][1]) > 0
    return found, "metrics scraped" if found else "no request metrics in Prometheus"


def _todo(check_id):
    def check(name, entry, ctx):
        return None, f"{check_id}: not implemented yet"
    return check


has_owner = _todo("has_owner")
has_alert_rule = _todo("has_alert_rule")          # hint: sources.prom_rules() + each rule's query text
alert_has_runbook = _todo("alert_has_runbook")
runbook_fresh = _todo("runbook_fresh")
has_synthetic_probe = _todo("has_synthetic_probe")
has_latency_alert = _todo("has_latency_alert")
has_slo = _todo("has_slo")

REGISTRY = {
    "has_metrics": has_metrics,
    "has_owner": has_owner,
    "has_alert_rule": has_alert_rule,
    "alert_has_runbook": alert_has_runbook,
    "runbook_fresh": runbook_fresh,
    "has_synthetic_probe": has_synthetic_probe,
    "has_latency_alert": has_latency_alert,
    "has_slo": has_slo,
}
