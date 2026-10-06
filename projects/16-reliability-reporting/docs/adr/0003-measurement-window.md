# ADR-0003: Measurement window

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

A trading platform's impact is concentrated in market hours. A 24/7 SLO treats a Sunday 03:00 outage the same as 09:01 on a Monday.

## Options considered

### Option 1: 24/7 rolling window (starter)
- **Pros:** Simple; standard tooling supports it.
- **Cons:** Overnight maintenance burns budget that doesn't matter; market-open spikes are diluted.

### Option 2: Trading hours only
- **Pros:** Reflects business impact.
- **Cons:** Harder to compute; overnight batch failures that break the next open are invisible unless measured separately.

### Option 3: Different windows per service (trading-hours for desk-facing, 24/7 for batch/platform)
- **Pros:** Each service measured the way it's used.
- **Cons:** Harder to compare across services.

### Rolling vs calendar
- Rolling (last 7/28 days): smooth, good for operations.
- Calendar (this month): matches business reporting and SLAs.

## Questions to answer before deciding

- How will you handle daylight-saving changes and exchange holidays?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


