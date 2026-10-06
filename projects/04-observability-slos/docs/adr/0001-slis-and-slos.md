# ADR-0001: SLIs and SLO targets

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Without an agreed target, every blip is either an emergency or ignored.
An SLO turns "is it good enough?" into a number, and the error budget tells you when to slow down.

## Options considered

### Option 1: Availability only (non-5xx ratio)
- **Pros:** Easy, available today.
- **Cons:** Misses "slow but successful", which is exactly the complaint in this project.

### Option 2: Availability + latency threshold (starter: 99.5% non-5xx, 99% < 250ms)
- **Pros:** Covers both user complaints.
- **Cons:** Server-side only. Doesn't see network/CDN/client problems.

### Option 3: Add synthetic probes / real-user monitoring
- **Pros:** Measures what users actually experience.
- **Cons:** More tooling. Synthetic traffic can skew SLIs if not excluded.

## Questions to answer before deciding

- Which endpoints count? (Probes and `/metrics` are excluded in the starter. Should `/work` be?)
- 99.5% over 30 days = 3h36m of budget. Is that right for this service? What about 99.9% (43m)?
- What happens when the budget runs out? (Freeze features? Who decides?)

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


