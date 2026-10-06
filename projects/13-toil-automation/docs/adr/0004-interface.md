# ADR-0004: Interface

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

The same action can be triggered by a person (CLI, chat), a schedule (cron), or an event (project 14).

## Options considered

### Option 1: CLI (starter)
- **Pros:** Simple; easy to test; composable.
- **Cons:** Needs access to a machine with credentials.

### Option 2: Chat bot (e.g. `/toil market-readiness` in Slack)
- **Pros:** Visible to the team; easy for first-line.
- **Cons:** Bot auth and permissions become a security concern.

### Option 3: Scheduled (cron / CI schedule / Kubernetes CronJob)
- **Pros:** Happens even when nobody remembers.
- **Cons:** Silent failures, so it needs its own "did it run?" check.

### Option 4: Self-healing controller (watches and acts continuously)
- **Pros:** Fastest response.
- **Cons:** Most dangerous; hardest to reason about. Belongs in 14's ADR on automation boundaries.

## Questions to answer before deciding

- Who runs each action, how often, and from where?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


