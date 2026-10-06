# ADR-0001: Durability settings: replication, min ISR, acks

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

The price feed must survive a broker failure without losing acknowledged ticks. Each extra guarantee adds latency,
and a trading firm cares about that too.

## Options considered

### Option 1: RF=3, min.insync.replicas=2, acks=all (starter)
- **Pros:** An acked message is on at least 2 brokers. Survives one broker loss with no data loss and no write outage.
- **Cons:** Highest produce latency. If 2 brokers are down, producers get errors instead of silently losing data.

### Option 2: RF=3, acks=1
- **Pros:** Lower latency; only the leader must write.
- **Cons:** If the leader dies before followers copy the message, acked messages are lost.

### Option 3: RF=3, min.insync.replicas=1, acks=all
- **Pros:** Keeps accepting writes even with 2 brokers down.
- **Cons:** "all" can mean "just the leader" when followers fall behind. A false sense of safety.

## Questions to answer before deciding

- What's worse for this feed: a lost tick, a late tick, or the producer refusing writes for 30 seconds?
- Measure produce latency (p99) for options 1 and 2. Is the difference significant for your SLO?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiments 1 and 2
