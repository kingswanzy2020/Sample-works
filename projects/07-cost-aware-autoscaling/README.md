# Project 07: Cost-aware autoscaling, with a written cost decision

> **Problem:** The cloud bill doubled and nobody can say why. Meanwhile, traffic spikes
> still cause slowdowns, because capacity is both too high (idle) and too slow to grow (spikes).

## Decisions this project proves you can make

1. **What to scale on:** CPU (lagging) vs request rate or queue depth (leading).
2. **Requests and limits:** right-sizing from data. Over-provisioning cost vs OOM/throttling risk.
3. **Floors, ceilings and scale-down speed:** idle cost vs cold-start pain.
4. **Spot vs on-demand:** which workloads tolerate interruption.
5. **Cost visibility:** tags/labels so every dollar has an owner.

## Success criteria

- [ ] Measured **capacity per pod** (req/s before p95 degrades). Every scaling number is derived from it.
- [ ] A spike from 5 → 150 req/s keeps the error rate < 1%. You know how many seconds users waited for scale-up.
- [ ] Requests are right-sized from VPA recommendations; you can state the before/after reserved CPU.
- [ ] A one-page cost decision: "We cut cost by X% and accepted Y risk" (`docs/cost-model.md`).
- [ ] A budget alert that fires on **forecast**, before the money is spent.

## Prerequisites and cost

- Local and free: Docker, kind, kubectl, k6, metrics-server. Optional: KEDA, VPA, Prometheus (from project 04).
- Cloud (optional): EKS + Karpenter for spot. **This costs real money.** Set the budget in `terraform/budgets` first.
- The workload is `/work?ms=N` on the shared app (CPU-bound, no database needed).

## Starter layout

```
kind/cluster.yaml
k8s/base/             # Deployment with labelled cost owner, guessed requests, PDB
k8s/hpa-cpu/          # HPA v2 on CPU with explicit scale-up/down behaviour
k8s/keda-rps/         # KEDA ScaledObject on Prometheus request rate
k8s/vpa/              # VPA in recommendation-only mode
k8s/cloud/            # Karpenter spot + on-demand NodePools (EKS)
load/find-capacity.js # step load against one pod
load/spike.js         # quiet → spike → quiet
scripts/watch-scaling.sh  # replicas + CPU requested → CSV for graphs
terraform/budgets/    # AWS budget with forecast alerts, filtered by Project tag
docs/cost-model.md    # the worksheet that turns measurements into dollars
```

## Milestones

### Build
- [ ] `make cluster hpa` (install metrics-server first; see the comment in `k8s/hpa-cpu/hpa.yaml`).
- [ ] **Find capacity:** delete the HPA, scale to 1 replica, run `load/find-capacity.js`. Record the knee of the latency curve.

### Test
- [ ] Run `load/spike.js` with `scripts/watch-scaling.sh` recording. Graph replicas vs load vs p95.
- [ ] Repeat with KEDA on request rate. Compare time-to-scale and errors.

### Break
- [ ] [`docs/break-it.md`](docs/break-it.md): memory limit too low, CPU limits throttling, flapping, spot interruption, runaway scaling.

### Decide
- [ ] ADR-0001 to ADR-0004, with numbers from your graphs.

### Improve
- [ ] Apply VPA recommendations, then re-run capacity and spike tests.
- [ ] Add OpenCost (or Kubecost) and show cost per team label.
- [ ] Schedule non-prod to scale to zero outside working hours. What does that save per month?

### Document
- [ ] `docs/cost-model.md` filled in, with a before/after graph.

## ADRs

| # | Decision | Status |
|---|----------|--------|
| [0001](docs/adr/0001-scaling-signal.md) | CPU vs request rate vs queue depth | Proposed |
| [0002](docs/adr/0002-requests-and-limits.md) | Right-sizing and CPU limits | Proposed |
| [0003](docs/adr/0003-spot-vs-on-demand.md) | Where spot is allowed | Proposed |
| [0004](docs/adr/0004-cost-allocation.md) | Tagging, budgets and ownership | Proposed |

## Interview story

> "Each pod handled ___ req/s before p95 went over ___ms. Requests were set to ___ but VPA showed
> ___, so we were paying for ___% idle. Switching to ___ scaling cut time-to-scale from ___ to ___.
> Spot saved ___% but ___, so we kept ___ on on-demand."
