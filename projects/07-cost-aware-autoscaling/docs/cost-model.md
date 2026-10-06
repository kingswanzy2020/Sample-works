# Cost model: turning measurements into a decision

Fill this in from **your measurements**, not vendor marketing. Prices change, so note the date and region.

## Inputs (measured)

| Input | Value | Source |
|-------|-------|--------|
| Capacity per pod (req/s at p95 < target) | | `load/find-capacity.js` |
| CPU / memory request per pod (before) | 250m / 192Mi | `k8s/base` |
| CPU / memory request per pod (after VPA) | | `kubectl describe vpa` |
| Peak traffic (req/s) | | |
| Average traffic (req/s) | | |
| Node type and $/hour (on-demand / spot) | | AWS pricing page, date: |

## Scenarios

| Scenario | Avg pods | Reserved vCPU | Nodes | $/month | Error rate in spike test | Notes |
|----------|----------|---------------|-------|---------|--------------------------|-------|
| A. Static, sized for peak | | | | | | the "before" |
| B. HPA on CPU | | | | | | |
| C. HPA + right-sized requests | | | | | | |
| D. C + spot for app pods | | | | | | interruption risk |
| E. C + non-prod scaled to zero at night | | | | | | |

## Decision

> We chose scenario ___. It costs $___/month (___% less than A). The accepted tradeoff is ___.
> We will revisit when ___.
