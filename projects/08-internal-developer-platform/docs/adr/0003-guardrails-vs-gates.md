# ADR-0003: Guardrails vs gates: what's mandatory

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Some defaults protect everyone (signed images, requests, owner labels). Enforcing them too early blocks teams
and makes the platform the enemy. Never enforcing them makes them optional.

## Options considered

### Option 1: Everything optional, documented as best practice
- **Pros:** No friction.
- **Cons:** Adoption depends on goodwill. Incidents come from the gaps.

### Option 2: Audit first, then Enforce with a deadline and an exception process (starter: Kyverno in Audit)
- **Pros:** Teams see violations before they're blocked. Exceptions are visible and expire.
- **Cons:** Needs follow-through and reporting.

### Option 3: Enforce from day one
- **Pros:** Strong guarantees immediately.
- **Cons:** Breaks existing workloads. Teams find ways around it.

## Questions to answer before deciding

- Classify each default: **mandatory** (signing, owner, requests), **default but overridable** (replicas, probes timings), **optional** (tracing).
- Where is each enforced: CI (shift left), admission (last line), or both?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiment 2
