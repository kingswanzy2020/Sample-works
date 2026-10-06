# ADR-0004: What happens to bad alerts

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

An alert that's rarely actionable trains people to ignore pages. But deleting it might hide a real problem.

## Options considered

### Option 1: Owner decides, always
- **Pros:** Respects ownership.
- **Cons:** Noisy alerts survive for months.

### Option 2: Policy: below X% actionable for N weeks → must be changed (rewrite, downgrade to ticket, or delete with a replacement signal)
- **Pros:** Clear rule; protects on-call.
- **Cons:** Low-volume alerts have unstable percentages.

### Option 3: Replace with SLO burn-rate alerts (project 04/16) by default
- **Pros:** Fixes the class of problem, not one alert.
- **Cons:** Requires SLOs to exist first (project 15/16 gaps).

## Questions to answer before deciding

- How many data points do you need before an actionable % means anything?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


