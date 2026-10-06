# ADR-0003: Spot vs on-demand

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Spot capacity is typically 60–90% cheaper but can be reclaimed with a 2-minute warning.

## Options considered

### Option 1: All on-demand
- **Pros:** Predictable.
- **Cons:** Highest cost.

### Option 2: Stateless app pods on spot, with on-demand fallback (starter NodePools)
- **Pros:** Big saving on the bulk of compute.
- **Cons:** Interruptions during a spike are the worst case. Needs PDBs, graceful shutdown (project 03), and instance diversity.

### Option 3: Mixed: a baseline of N replicas on on-demand, burst on spot
- **Pros:** Guaranteed minimum capacity even during a spot shortage.
- **Cons:** More scheduling configuration (topology spread, node affinity weights).

### Option 4: Commitments (Savings Plans / Reserved Instances) for the steady baseline
- **Pros:** ~30–60% off without interruption.
- **Cons:** 1–3 year commitment. Wrong if usage drops.

## Questions to answer before deciding

- Which workloads must never be on spot? (Databases, singletons, long batch jobs without checkpoints.)
- What happens if *all* spot capacity of your types disappears at once?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiment 4
