# Project 04: Observability that answers "why is it slow?"

> **Problem:** Users say the app is slow. Logs exist, but nobody can find the cause.
> Alerts fire on CPU at 3am and nobody knows if users are affected.

## Decisions this project proves you can make

1. **SLIs and SLOs:** what "good" means for users, in numbers.
2. **What pages a human:** symptoms (budget burn) vs causes (CPU, memory).
3. **Metrics pipeline:** Prometheus pull vs OpenTelemetry push.
4. **Trace sampling:** how much you keep and what you lose.
5. **Retention and cardinality:** what you chose *not* to collect, and why.
6. **Self-hosted vs managed.**

## Success criteria

- [ ] SLOs are written down (ADR-0001) and visible on a dashboard with remaining error budget.
- [ ] Inject 300ms DB latency. You find the cause **using traces in under 5 minutes**, starting from the alert.
- [ ] No alert pages on something that doesn't affect users.
- [ ] You can state the monthly cost of this stack, self-hosted vs a vendor, at 10× traffic.

## Prerequisites and cost

- Free and local: Docker Compose, k6. About 3 GB of RAM for the whole stack.

## Starter layout

```
docker-compose.yml            # app (OTel instrumented), db, toxiproxy, prometheus, alertmanager, loki, alloy, tempo, grafana
Dockerfile.otel               # shared app + OpenTelemetry auto-instrumentation, app code unchanged
prometheus/prometheus.yml
prometheus/rules/slo.yml      # SLI recording rules + multi-window burn-rate alerts
alertmanager/alertmanager.yml # page vs ticket routing, inhibition
grafana/                      # datasources (Prometheus/Loki/Tempo, linked) + RED/SLO dashboard
tempo/  alloy/  toxiproxy/
load/steady.js                # background traffic
```

## Run

```bash
# Inside the roadmap repo, point at the shared app. In an extracted repo the default ./app works.
APP_DIR=../../app docker compose up --build -d
k6 run load/steady.js &
open http://localhost:3000   # Grafana → Portfolio → sample-service: RED + SLO
open http://localhost:9090/alerts
```

## Milestones

### Build
- [ ] Fill in ADR-0001 (SLOs) **before** looking at the dashboard. Pick numbers from user expectations, not from what the graphs currently show.
- [ ] Bring the stack up. Find one request's trace in Tempo, then jump to its logs in Loki.

### Test
- [ ] Use toxiproxy to inject an error and confirm `ErrorBudgetFastBurn` fires. Record time to fire.
- [ ] Confirm a CPU spike from `/work?ms=2000` does **not** page. Should it? Write down why.

### Break
- [ ] [`docs/break-it.md`](docs/break-it.md): latency hunt, cardinality explosion, silent failure, alert fatigue.

### Decide
- [ ] ADR-0002 to ADR-0006.

### Improve
- [ ] Add structured JSON logs with `trace_id`, so logs ↔ traces link both ways.
- [ ] Add a runbook link annotation to every paging alert.
- [ ] Deploy the stack to project 03's cluster (kube-prometheus-stack) and turn on canary analysis there.

### Document
- [ ] Screenshot of the trace that found the latency, the timeline, and the interview story.

## ADRs

| # | Decision | Status |
|---|----------|--------|
| [0001](docs/adr/0001-slis-and-slos.md) | SLIs and SLO targets | Proposed |
| [0002](docs/adr/0002-what-pages-a-human.md) | Symptom vs cause alerting | Proposed |
| [0003](docs/adr/0003-metrics-pipeline.md) | Prometheus pull vs OTel push | Proposed |
| [0004](docs/adr/0004-trace-sampling.md) | Head vs tail sampling, ratio | Proposed |
| [0005](docs/adr/0005-retention-and-cardinality.md) | Retention and label budget | Proposed |
| [0006](docs/adr/0006-self-hosted-vs-managed.md) | Run it or buy it | Proposed |

## Interview story

> "We had ___ alerts a week and still missed ___. I defined SLOs of ___, switched to burn-rate
> alerts, and pages dropped to ___. When I injected DB latency, traces found it in ___ minutes
> vs ___ with logs alone. At 500 services I would ___ because ___."
