# ADR-0003: What counts as healthy

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Kubernetes routes traffic using readiness and restarts using liveness. Rollouts progress using
both, and canaries use metrics. Getting these wrong causes outages that look like deploy problems.

## Options considered

### Option 1: Both probes on `/healthz` (process up)
- **Pros:** Pods never restart because of a dependency.
- **Cons:** Traffic goes to pods that can't reach the DB.

### Option 2: Readiness checks dependencies (`/readyz`); liveness checks process only (starter default)
- **Pros:** Bad pods leave rotation without restart storms.
- **Cons:** If the DB is down, *every* pod goes unready, so you get a total outage instead of partial errors. Is that what you want?

### Option 3: Option 2 + metric-based rollout gates (error rate, p99)
- **Pros:** Catches "up but wrong" (500s, slow).
- **Cons:** Needs Prometheus and thresholds tuned to real traffic.

## Questions to answer before deciding

- Write down the exact definition of "zero downtime" you are measuring (0 failed requests? p99 < X?).
- Probe timing: how long until a broken pod leaves rotation? (`periodSeconds × failureThreshold`)

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiment 3
