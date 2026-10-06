# ADR-0005: Retention and cardinality budget

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Every unique label combination is a new time series. One unbounded label (user ID, raw URL path)
can multiply series by 1000× and take down Prometheus. Retention multiplies storage.

## Options considered

### Option 1: Collect everything, long retention
- **Pros:** Answers any future question.
- **Cons:** Cost and instability. Most of it is never queried.

### Option 2: Explicit label budget + short raw retention (starter: 7d) + recording rules for long-term SLIs
- **Pros:** Predictable cost. SLO history survives in downsampled form.
- **Cons:** Some questions about the past can't be answered.

### Option 3: Long-term store (Thanos / Mimir / vendor) with downsampling
- **Pros:** Months of history.
- **Cons:** More moving parts or vendor cost.

## Questions to answer before deciding

- What is the series count now? (`count({__name__=~".+"})`) What is your ceiling?
- Which labels are allowed on app metrics? (The app uses the route *template*, not the raw path. Why?)
- The 30-day error budget panel needs 30d of data. With 7d retention, what does it show?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiment 2 (cardinality)
