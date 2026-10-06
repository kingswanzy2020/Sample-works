# Project 16: Cross-service reliability reporting

> **Problem:** "Is trading reliability getting worse?" Nobody can answer. Each team has its own dashboard,
> nobody agrees what "available" means, and when five apps degrade because Kafka did, five teams report five unrelated outages.

**Need help while building?** See [`docs/build-plan.md`](docs/build-plan.md): tasks with a goal and a "done when" check, hints hidden in levels (nudge → concept → docs), and a diagnosis table. It never gives you the full solution.

Responsibility this project answers: *"Track reliability and availability across critical trading applications and the platforms they
depend on, and work with users, development teams and IT to find where service levels are degrading."*

## Decisions this project proves you can make

1. **SLA vs SLO vs SLI:** which you report to whom, and what each commits you to.
2. **SLO tooling:** a simple in-house format, or Sloth / Pyrra / OpenSLO.
3. **Measurement window:** trading hours only, or 24/7; rolling or calendar.
4. **Attribution:** how much of a service's bad minutes were its own fault vs a dependency's.
5. **The report itself:** audience, cadence, and what someone can learn from it in 2 minutes.

## Success criteria

- [ ] SLOs for every tier-1 service and every platform dependency, with targets justified in ADR-0001.
- [ ] Trading-hours SLIs, if ADR-0003 chooses them: a night-time outage doesn't count against a market-hours SLO, and a 09:00 outage counts fully.
- [ ] Composite availability: you can say what availability order-gateway *can't exceed* given its dependencies.
- [ ] Attribution: a Kafka game day shows up as **Kafka's** budget burn, with the dependent services marked as impacted, not as culprits.
- [ ] A weekly report (`reports/`), read and understood by a non-engineer in under 2 minutes. Test it on someone.
- [ ] A trend: at least 3 reports showing where service levels are degrading.

## Prerequisites and cost

- Free: Python 3.12, Docker (landscape). Uses incident records from project 12 if you have them.

## Starter layout

```
slos/slos.yaml                  # tool-neutral SLO specs (one example: order-gateway, 24/7)
reliability_report/sources.py   # Prometheus, catalog, project 12 incidents (plumbing)
reliability_report/slo.py       # 24/7 SLI + error budget (done); trading hours, composite, attribution are STUBS
reliability_report/render.py    # plain markdown table: making it useful for its audience is yours
tests/test_slo.py
reports/                        # commit one report per week
```

## Run

```bash
pip install -r requirements-dev.txt && python -m pytest
python -m reliability_report.render --out reports/$(date +%G-W%V).md
```

## How this project connects

| Direction | Project | What flows |
|-----------|---------|------------|
| Uses | Landscape | Metrics, catalog (`depends_on`, tiers, `trading_hours`) |
| Uses | [04 Observability](../04-observability-slos/) | 04 defined one SLO and *alerted* on burn. Here you *report* many SLOs over time, for people. Same concepts, different job |
| Uses | [12 Incident response](../12-incident-response/) | `incidents/*.yaml`: root cause and impacted services for attribution |
| Uses | [14 Triage](../14-alert-triage-pipeline/) | Correlation groups as an independent count of incidents per root cause |
| Uses | [15 Coverage audit](../15-monitoring-coverage-audit/) | Services without SLIs can't be reported, so 15's gaps limit this report |
| Uses | [10 Linux latency](../10-linux-performance-latency/) | How to state latency percentiles honestly in a latency SLO |
| Feeds | [17 Governance](../17-reliability-governance/) | Missed SLOs and budget burn per owner become review items |

**Not in this project:** alerting on burn rate (04), finding missing monitoring (15), and chasing teams to fix things (17).
Here you **measure and explain** reliability across the platform.

## ADRs

| # | Decision | Status |
|---|----------|--------|
| [0001](docs/adr/0001-sla-slo-sli.md) | SLA vs SLO vs SLI, and the targets | Proposed |
| [0002](docs/adr/0002-slo-tooling.md) | In-house format vs Sloth / Pyrra / OpenSLO | Proposed |
| [0003](docs/adr/0003-measurement-window.md) | Trading hours vs 24/7; rolling vs calendar | Proposed |
| [0004](docs/adr/0004-attribution.md) | Attributing impact to dependencies | Proposed |
| [0005](docs/adr/0005-report-audience.md) | Audience, cadence and format of the report | Proposed |

## Interview story

> "Nobody could say whether trading reliability was improving. I defined SLOs for ___ services measured during ___, built a weekly report,
> and found that ___% of the bad minutes on tier-1 apps came from ___. That changed the conversation from ___ to ___."
