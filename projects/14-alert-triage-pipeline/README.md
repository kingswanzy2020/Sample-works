# Project 14: Automated alert triage pipeline

> **Problem:** First-line receives bare alerts ("HighErrorRate order-gateway") with no owner, no runbook and no context.
> Everyone triages differently. When Kafka degrades, five services alert separately and five people start debugging five "different" problems.

**Need help while building?** See [`docs/build-plan.md`](docs/build-plan.md): tasks with a goal and a "done when" check, hints hidden in levels (nudge → concept → docs), and a diagnosis table. It never gives you the full solution.

Responsibilities this project answers: *"Automate repeatable triage work so first-line responds faster and more consistently,
including alert enrichment, routing, correlation and operational workflows."*

## Decisions this project proves you can make

1. **Where enrichment happens:** in alert rules (labels/annotations) or in a pipeline.
2. **Correlation strategy:** time window, dependency topology, or both, and the risk of merging unrelated incidents.
3. **Automation boundary:** gather information only, or also remediate?
4. **Failure mode:** if the triage service is down, alerts must still reach a human.
5. **Build vs buy:** PagerDuty/Opsgenie/incident.io event rules vs your own service.

## Success criteria

- [ ] Every alert arrives with owner, on-call, tier, runbook (and its age), and dependency health.
- [ ] A Kafka fault produces **one** group with Kafka as the probable cause, not 5 separate pages.
- [ ] The `double-trouble` game-day scenario still produces **two** groups (no false merge).
- [ ] Unowned services are routed according to an explicit rule, not dropped.
- [ ] Triage-service outage loses **no** pages (tested).
- [ ] Measured: time from alert to "responder knows what to do", before vs after (using project 12's game days).

## Prerequisites and cost

- Free: Python 3.12, Docker (for the landscape). Builds on project 12's ADR-0004 (the list of triage steps to automate).

## Starter layout

```
triage/app.py              # FastAPI: POST /alerts (Alertmanager webhook), POST /feedback, GET /healthz
triage/models.py           # webhook payload + TriageRecord (the record 17 reads)
triage/catalog.py          # loads landscape/catalog.yaml (plumbing)
triage/stages/enrich.py    # STUB
triage/stages/correlate.py # STUB: every alert its own group (the problem, reproduced)
triage/stages/route.py     # STUB
triage/stages/diagnose.py  # STUB: read-only checks
tests/fixtures/kafka-storm.json   # a real-shaped alert storm
scripts/replay.sh          # send a fixture without running the landscape
docs/triage-log-schema.md  # the data contract with project 17
```

## Run

```bash
pip install -r requirements-dev.txt && python -m pytest
uvicorn triage.app:app --host 0.0.0.0 --port 8080   # the landscape's Alertmanager already points here
scripts/replay.sh                                    # or run the landscape and inject a fault
```

## How this project connects

| Direction | Project | What flows |
|-----------|---------|------------|
| Uses | Landscape | Catalog (owners, tiers, runbooks, `depends_on`), alerts from its Alertmanager |
| Uses | [12 Incident response](../12-incident-response/) | ADR-0004 there lists which triage steps to automate. Game days measure the effect |
| Uses | [13 Toil automation](../13-toil-automation/) | Read-only toil actions can run as diagnostic steps here |
| Uses | [04 Observability](../04-observability-slos/) | Same alerting concepts; here you *process* alerts rather than define them |
| Feeds | [16 Reliability reporting](../16-reliability-reporting/) | Correlation groups = incident counts per root-cause service |
| Feeds | [17 Governance](../17-reliability-governance/) | `triage-log.jsonl` + `feedback.jsonl`: alert volume, noise, actionability per team |

**Not in this project:** writing alert rules and SLOs (04/16), finding services with *no* alerts (15), and judging alert quality over time (17).
Here you handle each alert **as it arrives**.

## ADRs

| # | Decision | Status |
|---|----------|--------|
| [0001](docs/adr/0001-where-enrichment-happens.md) | Enrich in rules vs in a pipeline; what to add | Proposed |
| [0002](docs/adr/0002-correlation-strategy.md) | Time window vs topology vs both | Proposed |
| [0003](docs/adr/0003-automation-boundary.md) | Diagnose only, or remediate | Proposed |
| [0004](docs/adr/0004-failure-mode.md) | Fail open: what happens when triage is down | Proposed |
| [0005](docs/adr/0005-build-vs-buy.md) | Own service vs incident-management product | Proposed |

## Interview story

> "First-line got bare alerts and a Kafka problem looked like 5 incidents. I built a triage pipeline that adds ___ and groups alerts by ___.
> In game days, time to the right owner went from ___ to ___. Correlation once merged two unrelated incidents, so I ___.
> If triage is down, ___."
