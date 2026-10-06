# Triage data: the contract with project 17

This service writes two append-only files. **Project 17 reads them**, so treat the field names as an API:
add fields freely, but don't rename or remove them without updating 17.

## `data/triage-log.jsonl`: one line per alert event (firing or resolved)

| Field | Meaning |
|-------|---------|
| `received_at` | when triage received it (UTC) |
| `fingerprint` | Alertmanager's stable id for this alert |
| `alertname`, `service`, `severity`, `status`, `starts_at` | from the alert |
| `enrichment` | what your enrich stage added (owner, runbook, tier…) |
| `group_id` | correlation group (one per probable incident) |
| `routed_to` | who was notified |
| `diagnostics` | results of read-only checks |
| `notes` | anything that went wrong while triaging (e.g. "catalog lookup failed") |

## `data/feedback.jsonl`: responder feedback

`{"fingerprint": "...", "actionable": true|false, "note": "..."}`. How responders give this feedback
(a link in the notification? a bot button?) is part of your design.
