# Incident record schema

Every incident (real or game day) gets a file `incidents/YYYY-MM-DD-<slug>.yaml`.
The structure is fixed because **projects 16 and 17 read these files**:
16 counts impact per service and attributes it to dependencies, and 17 tracks whether actions are completed.

```yaml
id: 2026-10-01-kafka-degraded
title: Kafka degradation caused order and price errors
severity: 2                      # your levels from process/severity-levels.md
game_day: true                   # false for real incidents
services_impacted: [order-gateway, price-feed, positions-api]
root_cause_service: kafka        # where the cause was, not where it was seen
timeline:                        # UTC, ISO 8601
  started: 2026-10-01T09:12:00Z  # when impact began (from injection log / metrics)
  detected: 2026-10-01T09:15:30Z # first alert or human notice
  mitigated: 2026-10-01T09:31:00Z
  resolved: 2026-10-01T09:40:00Z
detection: alert                 # alert | human | customer
alerts_fired: [KafkaDegraded, HighErrorRate]
runbooks_used:
  - { runbook: runbooks/kafka.md, helped: true, notes: "" }
actions:
  - { id: A1, description: "", owner: team-platform, due: 2026-10-15, status: open }  # open | done | wont_do
postmortem: docs/postmortems/2026-10-01-kafka-degraded.md
```
