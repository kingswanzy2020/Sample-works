# ADR-0001: Scaling signal

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

The app must absorb spikes (5 → 150 req/s in 20s) without errors, and shrink when quiet.

## Options considered

### Option 1: CPU utilization (HPA v2)
- **Pros:** Built in, no extra components.
- **Cons:** Lagging: CPU rises only after requests queue. Depends entirely on correct CPU *requests*.
  Useless for I/O-bound services.

### Option 2: Request rate per pod (KEDA + Prometheus)
- **Pros:** Leading indicator. Target maps directly to measured capacity.
- **Cons:** Requires Prometheus to be healthy. If it isn't, scaling stops (what's the fallback?).

### Option 3: Queue depth / lag (KEDA on SQS, Kafka, Redis)
- **Pros:** Ideal for async workers; can scale to zero.
- **Cons:** Only for queue-driven workloads.

### Option 4: Scheduled scaling (known daily peaks)
- **Pros:** Capacity is ready before the spike.
- **Cons:** Wrong when traffic doesn't follow the schedule.

## Questions to answer before deciding

- How long from spike start until new pods are *ready*? (Pod start + image pull + node provisioning if the cluster is full.)
- What should min replicas be, given that time-to-ready?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

scaling.csv graphs from load/spike.js
