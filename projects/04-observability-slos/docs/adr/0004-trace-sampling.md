# ADR-0004: Trace sampling

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Tracing 100% of requests is ideal for debugging and expensive at scale. The lab uses 100%.

## Options considered

### Option 1: Head sampling at a fixed ratio (e.g. 10%)
- **Pros:** Cheap, simple, decided at the start of the request.
- **Cons:** Rare errors and slow requests are mostly dropped, and those are the ones you need.

### Option 2: Tail sampling in a collector (keep all errors + slow + X% of the rest)
- **Pros:** Keeps the interesting traces.
- **Cons:** The collector must buffer whole traces. Memory-heavy, and stateful when scaled out.

### Option 3: 100% with short retention
- **Pros:** Never miss anything recent.
- **Cons:** Storage cost grows with traffic.

## Questions to answer before deciding

- At 10% head sampling and 0.1% error rate, how many error traces per hour at 50 req/s? Is that enough?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


