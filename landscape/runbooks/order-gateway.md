# Runbook: order-gateway

**Owner:** team-execution · **Tier:** 1 · **Last reviewed:** 2026-08-20

## What it does
Accepts orders from strategies, checks them with risk-engine, and publishes them to Kafka.

## Symptoms → first checks
| Symptom | Check | If true |
|---------|-------|---------|
| Error rate up | Is `risk-engine` healthy? (`svc_up{service="risk-engine"}`) | It's a dependency problem: page risk-engine's on-call and follow their runbook |
| Error rate up, risk-engine fine | Is `kafka` degraded? | Follow `kafka.md` |
| Error rate up, dependencies fine | Recent deploy? | Roll back (see deploy tool) and tell #trading-ops |
| Latency up | `auth` latency? | Escalate to platform |

## Escalation
execution-primary → execution-secondary → head of execution engineering.

## Communication
Post in #trading-ops within 5 minutes of a confirmed Sev1/Sev2, then every 15 minutes.
