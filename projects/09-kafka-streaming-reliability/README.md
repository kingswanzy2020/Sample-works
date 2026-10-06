# Project 09: Reliable Kafka streaming pipeline

> **Problem:** A real-time price feed runs over Kafka. When a broker dies, some messages are lost
> or duplicated, and nobody can say how many. During spikes, consumer lag grows silently
> until downstream services are trading on stale prices.

**Need help while building?** See [`docs/build-plan.md`](docs/build-plan.md): tasks with a goal and a "done when" check, hints hidden in levels (nudge → concept → docs), and a diagnosis table. It never gives you the full solution.

## Decisions this project proves you can make

1. **Durability vs latency:** replication factor, `min.insync.replicas` and producer `acks`.
2. **Delivery semantics:** at-most-once, at-least-once or exactly-once, and what each costs.
3. **Partitioning and consumer scaling:** partition count, keys, ordering, and the consumer-group ceiling.
4. **Freshness as an SLO:** how stale can data be before it's an incident?
5. **Run it or buy it:** self-hosted (on VMs or Strimzi on Kubernetes) vs managed (MSK, Confluent Cloud).

## Success criteria

- [ ] You can **prove**, with sequence numbers, how many messages were lost or duplicated in any failure.
- [ ] Killing the leader broker under load loses **0** acknowledged messages with your chosen settings, and you can show the setting that would have lost some.
- [ ] Consumer lag is visible on a dashboard and alerts **before** data is stale enough to matter.
- [ ] A written freshness SLO (e.g. "99% of ticks processed within N ms during trading hours").
- [ ] You know the throughput ceiling of one consumer and of the group.

## Prerequisites and cost

- Free and local: Docker Compose (3 brokers ≈ 2–3 GB RAM), Python 3.12.
- Optional: project 04's Prometheus/Grafana for lag dashboards and alerts.

## Starter layout

```
docker-compose.yml        # 3 KRaft brokers, kafka-exporter (lag metrics), producer + consumer (profile: pipeline)
pipeline/producer.py      # price ticks with a global sequence number; logs every ACKED seq
pipeline/consumer.py      # logs every PROCESSED seq; COMMIT_MODE and PROCESS_MS knobs
scripts/create-topic.sh   # topic with partitions / RF / min.insync.replicas from env
scripts/lag.sh            # consumer group lag per partition
docs/adr/  docs/break-it.md  docs/scale.md  docs/postmortems/  docs/build-plan.md
```

Measuring loss and duplicates from `data/produced.jsonl` vs `data/consumed.jsonl` is **your** first task. The starter records the evidence, and you write the verifier.

## Run

```bash
docker compose up -d kafka1 kafka2 kafka3 kafka-exporter
scripts/create-topic.sh
docker compose --profile pipeline up -d --build producer consumer
scripts/lag.sh
```

## How this project connects

| Direction | Project | What flows |
|-----------|---------|------------|
| Uses | [04 Observability](../04-observability-slos/) | Its Prometheus/Grafana scrape `kafka-exporter` here, for lag dashboards and a freshness SLO alert |
| Uses (optional) | [03 Zero-downtime](../03-zero-downtime-deploys/) | Run Kafka on Kubernetes with Strimzi instead of Compose, if ADR-0004 says so |
| Feeds | [10 Linux latency](../10-linux-performance-latency/) | The consumer's end-to-end latency is a real workload to profile |
| Feeds | [13 Toil automation](../13-toil-automation/) | "Restart a stuck consumer" and "check lag before market open" are toil tasks there |
| Feeds | [14–16](../14-alert-triage-pipeline/) | `kafka` is a platform dependency in the landscape; what you learn here shapes its alerts and runbook |

**Not in this project (so it isn't repeated):** general metrics and alerting setup (04), backups (06), and host-level tuning (10). Here you only *expose* Kafka metrics and define the freshness SLO.

## ADRs

| # | Decision | Status |
|---|----------|--------|
| [0001](docs/adr/0001-durability-settings.md) | Replication, min ISR and acks | Proposed |
| [0002](docs/adr/0002-delivery-semantics.md) | At-most / at-least / exactly-once | Proposed |
| [0003](docs/adr/0003-partitioning-and-scaling.md) | Partitions, keys, ordering, consumer scaling | Proposed |
| [0004](docs/adr/0004-self-hosted-vs-managed.md) | Self-hosted vs managed Kafka | Proposed |

## Interview story

> "Ticks were lost during broker failovers and nobody could quantify it. I added sequence numbers and proved
> ___ messages were lost with `acks=___`. I changed to ___, and the same failure lost 0, at a latency cost of ___.
> A slow consumer taught me ___ about lag, so freshness is now an SLO with an alert at ___."
