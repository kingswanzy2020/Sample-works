"""Alert triage service: receives Alertmanager webhooks and runs each alert through the pipeline.

    uvicorn triage.app:app --port 8080

Pipeline: enrich → correlate → route → diagnose → record (data/triage-log.jsonl) → notify (stdout for now).
"""
from __future__ import annotations

import json
import os
import pathlib
from datetime import UTC, datetime

from fastapi import FastAPI

from triage import catalog as catalog_mod
from triage.models import TriageRecord, WebhookPayload
from triage.stages.correlate import correlate
from triage.stages.diagnose import diagnose
from triage.stages.enrich import enrich
from triage.stages.route import route

DATA = pathlib.Path(os.getenv("TRIAGE_DATA", "data"))
STAGES = [enrich, correlate, route, diagnose]

app = FastAPI(title="alert-triage")
catalog = catalog_mod.load()


def _append(name: str, obj: dict) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    with (DATA / name).open("a") as f:
        f.write(json.dumps(obj, default=str) + "\n")


@app.post("/alerts")
def receive(payload: WebhookPayload):
    out = []
    for alert in payload.alerts:
        record = TriageRecord(
            received_at=datetime.now(UTC),
            fingerprint=alert.fingerprint,
            alertname=alert.labels.get("alertname", "unknown"),
            status=alert.status,
            service=alert.labels.get("service"),
            severity=alert.labels.get("severity"),
            starts_at=alert.startsAt,
        )
        for stage in STAGES:
            record = stage(record, catalog)
        _append("triage-log.jsonl", record.model_dump(mode="json"))
        print(f"[{record.status}] {record.alertname} service={record.service} "
              f"group={record.group_id} → {record.routed_to}", flush=True)
        out.append(record.fingerprint)
    return {"processed": out}


@app.post("/feedback")
def feedback(body: dict):
    """Responders mark an alert as actionable or not. Project 17 uses this to measure alert quality."""
    _append("feedback.jsonl", {"received_at": datetime.now(UTC).isoformat(), **body})
    return {"ok": True}


@app.get("/healthz")
def healthz():
    return {"status": "ok", "services_in_catalog": len(catalog)}
