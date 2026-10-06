# ADR-0004: Attributing impact to dependencies

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

When Kafka degrades, order-gateway's SLO burns too. Without attribution, the execution team looks unreliable for a platform problem,
and the platform team never sees its true impact.

## Options considered

### Option 1: No attribution (each service's SLO is its own)
- **Pros:** Simple and honest about user experience.
- **Cons:** Wrong conclusions about *who* needs to improve.

### Option 2: Incident-based attribution (use project 12's root_cause_service)
- **Pros:** Uses human judgement already recorded in postmortems.
- **Cons:** Only as good as the incident records; small blips never become incidents.

### Option 3: Metric-based attribution (when a dependency is burning, count the dependent's bad minutes against the dependency)
- **Pros:** Automatic; catches small blips.
- **Cons:** Correlation isn't causation; needs a trustworthy dependency map.

## Questions to answer before deciding

- Should the user-facing SLO number change, or only the explanation next to it?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

game day: kafka-degraded
