# Project 15: Monitoring coverage audit and minimum standard

> **Problem:** Nobody knows which services are badly monitored until one fails silently. In the landscape, a slow database
> produces no alert at all, two services have no alerts, and one alert pages on every single error.

**Need help while building?** See [`docs/build-plan.md`](docs/build-plan.md): tasks with a goal and a "done when" check, hints hidden in levels (nudge → concept → docs), and a diagnosis table. It never gives you the full solution.

Responsibility this project answers: *"Push for monitoring, alerting and visibility where gaps exist."*
To push for something, you first need to show where the gaps are, which ones matter most, and what "good enough" means.

## Decisions this project proves you can make

1. **The minimum standard:** what every tier-1/2/3 service must have, and why.
2. **White-box vs black-box:** internal metrics vs synthetic checks from outside, and when you need both.
3. **Report vs enforce:** dashboards and nudges, or a gate (e.g. no tier-1 service goes live without the standard).
4. **Prioritising gaps:** which gap to close first when there are twenty.
5. **Who closes the gap:** SRE adds it, or the owning team does (with SRE help).

## Success criteria

- [ ] A written minimum standard per tier (`monitoring-standard.yaml` + ADR-0001).
- [ ] The scanner checks every catalog service against it, with every check implemented and tested.
- [ ] Synthetic probes for tier-1 services, with an alert that fires on project 12's `slow-postgres` scenario (which nothing catches today).
- [ ] A prioritised gap backlog: each gap with an owner, a severity and a due date (`docs/gap-backlog.md`).
- [ ] At least 3 gaps actually closed in the landscape, with before/after scanner output.

## Prerequisites and cost

- Free: Python 3.12, Docker (landscape). Builds on what you learned in project 04.

## Starter layout

```
monitoring-standard.yaml      # the standard: required checks per tier (EMPTY: ADR-0001)
coverage_audit/sources.py     # catalog + Prometheus queries/rules (plumbing)
coverage_audit/checks.py      # has_metrics implemented as an example; the rest are stubs
coverage_audit/scan.py        # runs required checks per service, prints PASS/FAIL/TODO, optional JSON
tests/test_scan.py
blackbox/                     # blackbox exporter on the landscape network + an http_2xx module
```

The landscape simulator exposes `GET /probe/<service>`, a black-box view of each service that reflects faults and latency.

## Run

```bash
pip install -r requirements-dev.txt && python -m pytest
python -m coverage_audit.scan
cd blackbox && docker compose up -d   # needs the landscape running
curl "localhost:9115/probe?module=http_2xx&target=http://simulator:9200/probe/price-feed"
```

## How this project connects

| Direction | Project | What flows |
|-----------|---------|------------|
| Uses | Landscape | Catalog, existing alert rules, simulator probes |
| Uses | [04 Observability](../04-observability-slos/) | 04 built *good* monitoring for one service. That experience shapes the standard you write here |
| Uses | [12 Incident response](../12-incident-response/) | Game day "silent degradation" is evidence of a real gap |
| Boundary with | [08 Platform scorecard](../08-internal-developer-platform/) | 08 checks a repo's *files* (does it declare probes?). 15 checks *live reality* (is it actually monitored and alerting?) |
| Feeds | [16 Reliability reporting](../16-reliability-reporting/) | A service can't have a reliability number until it has SLIs. 15 finds which don't |
| Feeds | [17 Governance](../17-reliability-governance/) | Gap backlog with owners and due dates; overdue gaps become accountability items |

**Not in this project:** handling alerts as they fire (14), alert *quality* over time (17), and SLO reporting (16).
Here you answer **"is it monitored enough?"**

## ADRs

| # | Decision | Status |
|---|----------|--------|
| [0001](docs/adr/0001-minimum-standard.md) | Minimum monitoring standard per tier | Proposed |
| [0002](docs/adr/0002-white-vs-black-box.md) | Internal metrics vs synthetic probes | Proposed |
| [0003](docs/adr/0003-report-vs-enforce.md) | Report gaps vs block on them | Proposed |
| [0004](docs/adr/0004-prioritising-gaps.md) | Which gaps to close first | Proposed |
| [0005](docs/adr/0005-who-closes-gaps.md) | SRE closes gaps vs owning teams do | Proposed |

## Interview story

> "Nobody could say which services were properly monitored. I wrote a standard (___ for tier 1), built a scanner, and found ___ gaps,
> including ___ which no alert covered at all. I prioritised by ___, closed ___, and got owning teams to close ___ by ___."
