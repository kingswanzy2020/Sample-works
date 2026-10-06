# ADR-0001: Minimum monitoring standard per tier

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

"Monitor everything" is not a standard. A standard says exactly what's required, by tier, so gaps are measurable.

## Options considered

### Option 1: The same standard for everything
- **Pros:** Simple to explain.
- **Cons:** Too heavy for tier 3, or too light for tier 1.

### Option 2: Tiered standard (stricter for tier 1) (starter structure)
- **Pros:** Effort goes where business impact is.
- **Cons:** Tier assignment must be right; tier-3 services can still take down tier-1 dependents.

### Option 3: Standard by *dependency*: anything a tier-1 service depends on inherits tier-1 requirements
- **Pros:** Covers the platform services that cause most cascades (kafka, postgres).
- **Cons:** Requires a trustworthy dependency map.

## Questions to answer before deciding

- Which check would have caught each game-day scenario from project 12?
- Golden signals (latency, traffic, errors, saturation): which are mandatory for which tier?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

game day results; first scan output
