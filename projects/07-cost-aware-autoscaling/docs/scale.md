# What I'd do differently at a different scale

## Now: one service, one cluster
- Which change saved the most money per hour of work?

## 10×: several services sharing clusters
- Karpenter consolidation + spot diversification; OpenCost showback per team.
- Savings Plans for the stable baseline, spot for burst.
- Policy: no deploy without requests set and an owner label (Kyverno/Gatekeeper).

## 100×: FinOps as a practice
- Unit economics: cost per request / per customer, tracked like latency.
- Teams own their budgets; anomaly detection on daily spend.
- Architecture-level savings (caching, data transfer, storage tiers) beat node tuning.

## The one-paragraph version for interviews

>
