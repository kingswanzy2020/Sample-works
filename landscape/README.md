# The landscape: a simulated trading platform

Projects 12–17 are about running **many** services, not building one. They need a platform with several
services, dependencies between them, uneven monitoring and imperfect ownership. This is that platform.

| Piece | What it is |
|-------|------------|
| `catalog.yaml` | 8 services (tiers, owners, on-call, runbooks, dependencies, trading hours). **Deliberately imperfect.** |
| `simulator/` | Emits Prometheus metrics for every catalog service. Failures propagate along `depends_on`. |
| `prometheus/rules/fleet-alerts.yml` | The platform's "existing" alerts. **Deliberately uneven:** gaps, a noisy alert, bare alerts. |
| `alertmanager/` | Sends alerts to project 14's triage service on `:8080` (if it's running). |

## Run

```bash
docker compose up -d --build
curl localhost:9200/state                      # every service and its current error rate
curl -XPOST localhost:9200/fault -d '{"service":"kafka","error_rate":0.3}'
curl -XPOST localhost:9200/fault -d '{"service":"risk-engine","down":true}'
curl -XPOST localhost:9200/clear
curl -i localhost:9200/probe/order-gateway       # black-box view of one service (used by project 15)
```

A fault on `kafka` leaks into `price-feed`, `order-gateway` and `positions-api` (70% of the error rate by default,
`PROPAGATION`). One root cause therefore shows up as several alerts. That's the point.

## Ground rules

- **Don't clean up the catalog or alerts in advance.** Finding the flaws with your own tooling is the work of projects 15 and 17.
- When a project fixes something (e.g. assigns an owner), commit the change and reference the ADR or postmortem that justified it.
- The simulator is a stand-in. Where a project says "real services", you can point the same tooling at the sample app (project 04) or the Kafka pipeline (project 09).
