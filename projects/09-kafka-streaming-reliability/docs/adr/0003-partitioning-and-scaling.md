# ADR-0003: Partitioning, ordering and consumer scaling

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Ordering only holds within a partition. One consumer per partition, at most, is active within a group.
So partition count is both your parallelism ceiling and your ordering boundary.

## Options considered

### Option 1: Key by instrument, modest partitions (starter: 6)
- **Pros:** Per-instrument ordering. Simple.
- **Cons:** Hot instruments create hot partitions. Max 6 parallel consumers.

### Option 2: Many partitions (e.g. 48+)
- **Pros:** Room to scale consumers.
- **Cons:** More open files, longer leader elections, slower rebalances. Can't easily *reduce* later.

### Option 3: No key (round-robin)
- **Pros:** Even load.
- **Cons:** No ordering per instrument. Is that acceptable for prices?

## Questions to answer before deciding

- Measure one consumer's max throughput. Peak rate ÷ that number = minimum partitions. What headroom do you add?
- What happens to ordering when you add partitions to an existing keyed topic?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiment 4 (slow consumer / rebalance)
