# Project 03: Zero-downtime deployments for a stateful app

> **Problem:** Every deploy causes 30–60 seconds of 502s, and database migrations
> sometimes break the version that is still running.

## Decisions this project proves you can make

1. **Rollout strategy:** rolling vs blue/green vs canary, for *this* app and budget.
2. **Schema changes with two app versions alive:** expand/contract.
3. **What "healthy" means:** which probes and signals gate traffic and trigger rollback.
4. **Graceful shutdown:** how a pod leaves without dropping in-flight requests.

## Success criteria

- [ ] A deploy under constant load (50 req/s) produces **0 failed requests**, measured by k6, not eyeballed.
- [ ] A column rename ships across 3 deploys with no errors.
- [ ] A bad version is rolled back automatically (canary) or in under 30 seconds (blue/green).
- [ ] You can explain every number in the Deployment spec (`maxSurge`, `preStop`, grace period, probe timings).

## Prerequisites and cost

- Free and local: Docker, [kind](https://kind.sigs.k8s.io/), kubectl, [k6](https://k6.io/). Optional: Argo Rollouts.
- Later, run it on the cluster from project 01 to compare a cloud load balancer's behaviour.

## Starter layout

```
kind/cluster.yaml               # 3-node local cluster, app on localhost:8080
k8s/base/                       # namespace, lab Postgres, migration Job
k8s/rolling/                    # Deployment + Service + PDB (start here)
k8s/blue-green/                 # two Deployments, Service selector switch
k8s/canary/                     # Argo Rollouts canary + Prometheus analysis
migrations-expand-contract/     # rename a column in 3 safe steps
load/during-deploy.js           # k6 constant-rate load with zero-error threshold
scripts/deploy-under-load.sh    # rollout while measuring
scripts/blue-green-switch.sh
Makefile
```

## Milestones

### Build
- [ ] `make cluster rolling`, then `curl localhost:8080/version`.
- [ ] **Baseline the naive version first:** remove the `preStop`, set `maxUnavailable: 1`, and point both probes at `/healthz`.
      Run `make deploy-v2` and record the failed request count. That number is the "before" in your story.
- [ ] Restore the starter settings and measure again.

### Test
- [ ] Repeat each strategy (rolling, blue/green, canary) 3× under load. Record in the table below.

### Break
- [ ] [`docs/break-it.md`](docs/break-it.md): breaking migration, no preStop, liveness pointing at the DB, bad canary.

### Decide
- [ ] ADR-0001 (strategy), ADR-0002 (migrations), ADR-0003 (health definition), ADR-0004 (rollback trigger).

### Improve
- [ ] Add the canary analysis once project 04's Prometheus exists.
- [ ] Add the deploy to project 02's pipeline.

### Document
- [ ] Results table, a timeline diagram of pod termination (SIGTERM → endpoints removed → exit), and the interview story.

## Results

| Strategy | Config | Failed requests | p99 during deploy | Rollback time | Extra capacity needed |
|----------|--------|-----------------|-------------------|---------------|-----------------------|
| Rolling (naive) | | | | | |
| Rolling (tuned) | | | | | |
| Blue/green | | | | | |
| Canary | | | | | |

## ADRs

| # | Decision | Status |
|---|----------|--------|
| [0001](docs/adr/0001-rollout-strategy.md) | Rolling vs blue/green vs canary | Proposed |
| [0002](docs/adr/0002-schema-migrations.md) | How and when migrations run | Proposed |
| [0003](docs/adr/0003-definition-of-healthy.md) | Probes and health signals | Proposed |
| [0004](docs/adr/0004-rollback-trigger.md) | Automatic vs manual rollback | Proposed |

## Interview story

> "Deploys dropped ___ requests. The cause was ___ (endpoint propagation / probes / migrations).
> I chose ___ over ___ because ___. The migration that broke taught me ___.
> With many services I'd use ___."
