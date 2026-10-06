# ADR-0001: Which metrics, and how they get gamed

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Whatever you measure, teams will optimise. If the metric is wrong, they'll optimise the wrong thing.

## Options considered

### Option 1: Volume metrics (alerts per week, incidents per month)
- **Pros:** Easy to compute and explain.
- **Cons:** Easily gamed: delete alerts → fewer alerts → looks better, monitoring got worse.

### Option 2: Quality ratios (actionable %, runbook helped %, actions closed on time %)
- **Pros:** Harder to game; aligned with what matters.
- **Cons:** Depend on feedback data, which people don't always give (missing feedback is itself a finding).

### Option 3: Paired metrics (each metric has a counter-metric: fewer pages AND coverage from project 15 stays green)
- **Pros:** Gaming one shows up in the other.
- **Cons:** More to explain.

## Questions to answer before deciding

- For each metric: how would a team make it look better *without* improving reliability?
- Which metrics would you be comfortable being measured on yourself?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiment 1
