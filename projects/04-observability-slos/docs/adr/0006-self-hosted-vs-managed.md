# ADR-0006: Self-hosted vs managed observability

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

The lab stack is self-hosted and free in money terms. It is not free in time.

## Options considered

### Option 1: Self-hosted (Prometheus, Loki, Tempo, Grafana)
- **Pros:** No per-GB/per-host bill. Full control.
- **Cons:** You are on call for your monitoring. Upgrades, storage and scaling are your job.

### Option 2: Managed open-source (Grafana Cloud, AWS Managed Prometheus/Grafana)
- **Pros:** Same query languages, less ops.
- **Cons:** Usage-based billing that grows with cardinality and logs.

### Option 3: Full vendor (Datadog, New Relic, Honeycomb)
- **Pros:** Best UX, correlation, and support.
- **Cons:** Highest cost at scale; lock-in through agents and query languages.

## Questions to answer before deciding

- Estimate: hours/month to run it × your hourly cost, vs vendor price at current and 10× volume.
- Who monitors the monitoring? (If Prometheus dies, what alerts?)

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


