# ADR-0002: Schema migrations with two app versions alive

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

During any rollout, old and new pods share the database. A migration that is fine for the
new code can break the old code that is still serving traffic.

## Options considered

### Option 1: Migrate in the app on startup
- **Pros:** No extra moving parts.
- **Cons:** N pods race to migrate. Slow migrations block startup and fail readiness.

### Option 2: Separate migration Job before rollout (starter default) + expand/contract discipline
- **Pros:** Runs once. Rollout only starts if it succeeds. Each step is backward-compatible.
- **Cons:** A rename becomes 3 deploys. Requires discipline and review.

### Option 3: Downtime window for breaking changes
- **Pros:** Simple and honest.
- **Cons:** Users see downtime. Doesn't scale with deploy frequency.

## Questions to answer before deciding

- Who checks that a migration is backward-compatible? Can CI check it (e.g. run old app tests against new schema)?
- How do you roll back a migration? (Often: you don't; you roll forward.)
- What about locks? Adding a column with a volatile default or creating an index without `CONCURRENTLY` locks the table.

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiment 1
