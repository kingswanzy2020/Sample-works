# ADR-0001: Rollout strategy

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

The app runs 4 replicas behind a Service. We need deploys with no failed requests and a fast rollback,
without doubling the infra bill unless that's justified.

## Options considered

### Option 1: Rolling update (`maxSurge: 1`, `maxUnavailable: 0`)
- **Pros:** Built in, needs only +1 pod of capacity.
- **Cons:** Two versions live for minutes. Rollback is another rollout (slow). No traffic-percentage control.

### Option 2: Blue/green
- **Pros:** Instant switch and instant rollback. Can smoke-test green before it gets traffic.
- **Cons:** 2× capacity during the deploy. The DB is still shared, so migrations remain the hard part.

### Option 3: Canary (Argo Rollouts)
- **Pros:** Limits blast radius to ~25%. Can roll back automatically on metrics.
- **Cons:** Needs good metrics (project 04) and enough traffic for the metrics to mean something.
  Without a mesh/ingress, the weight is approximate (replica ratio).

## Questions to answer before deciding

- At 1 request/minute, could a canary detect a 5% error rate before full rollout? (Statistics matter.)
- What does an hour of degraded service cost vs the extra capacity?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

README results table
