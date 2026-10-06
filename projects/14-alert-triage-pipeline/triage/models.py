"""Alertmanager webhook payload (v4) and the triage record this service produces."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class Alert(BaseModel):
    status: str
    labels: dict[str, str]
    annotations: dict[str, str] = {}
    startsAt: datetime
    endsAt: datetime | None = None
    fingerprint: str


class WebhookPayload(BaseModel):
    version: str
    status: str
    receiver: str
    groupLabels: dict[str, str] = {}
    commonLabels: dict[str, str] = {}
    alerts: list[Alert]


class TriageRecord(BaseModel):
    """One line in data/triage-log.jsonl. Project 17 reads these: keep the field names stable."""

    received_at: datetime
    fingerprint: str
    alertname: str
    status: str                       # firing | resolved
    service: str | None = None
    severity: str | None = None
    starts_at: datetime
    enrichment: dict = Field(default_factory=dict)   # owner, oncall, runbook, tier, dependencies, ...
    group_id: str | None = None                      # set by correlation
    routed_to: str | None = None                     # set by routing
    diagnostics: list[dict] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
