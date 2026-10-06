# ADR-0002: Delivery semantics

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Failures happen between "processed" and "committed". Whichever comes first decides whether you lose or duplicate.

## Options considered

### Option 1: At-most-once (commit before processing)
- **Pros:** Never duplicates. Fastest.
- **Cons:** A crash loses the in-flight message. Is a lost price tick acceptable? (Maybe, if the next tick supersedes it.)

### Option 2: At-least-once (process, then commit) + idempotent processing (starter)
- **Pros:** Never loses. Duplicates are handled by making processing idempotent (e.g. ignore seq ≤ last seen per key).
- **Cons:** You must design idempotency into every consumer.

### Option 3: Exactly-once (transactions: read-process-write within Kafka)
- **Pros:** Strong guarantee for Kafka-to-Kafka pipelines.
- **Cons:** Only covers Kafka-to-Kafka. Side effects outside Kafka (DB writes, orders sent) still need idempotency. Adds latency and complexity.

## Questions to answer before deciding

- For a *price* feed vs an *order* feed, would your answer differ? Why?
- What does the producer's idempotence setting protect against, and what doesn't it cover?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiment 3
