# ADR-0002: Correlation strategy

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

One root cause produces several alerts (see the landscape's `depends_on`). But two unrelated problems at the same time must stay separate.

## Options considered

### Option 1: Time window only (alerts within N minutes = one group)
- **Pros:** Simple.
- **Cons:** Merges unrelated incidents that happen to overlap (`double-trouble`).

### Option 2: Topology: group when one alerting service depends on another alerting service
- **Pros:** Finds the probable root cause, not just "things at the same time".
- **Cons:** Only as good as the dependency map. Missing edges = missed correlation.

### Option 3: Topology + time window, with "probable cause" shown but not hidden
- **Pros:** Best of both; humans see the reasoning.
- **Cons:** More logic; state must survive restarts.

### Option 4: Statistical/ML correlation
- **Pros:** Finds patterns humans don't.
- **Cons:** Opaque; hard to trust at 3am; needs lots of history.

## Questions to answer before deciding

- What's worse for first-line: two incidents wrongly merged, or one incident split in two?
- Should correlated alerts be suppressed, or shown as children of the group?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiments 1 and 3
