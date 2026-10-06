# ADR-0004: Failure mode: when triage is down

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Putting a service between Alertmanager and humans creates a new way to lose pages.

## Options considered

### Option 1: Triage is the only path
- **Pros:** Simple configuration.
- **Cons:** Triage down = no pages. Unacceptable for tier-1 on its own.

### Option 2: Alertmanager sends to triage **and** a fallback receiver; triage suppresses duplicates downstream
- **Pros:** Pages always arrive, enriched or not.
- **Cons:** Duplicate notifications when triage is healthy, unless handled carefully.

### Option 3: Fallback only when triage is unhealthy (Alertmanager can't do this natively; needs a watchdog)
- **Pros:** No duplicates normally.
- **Cons:** The watchdog is another moving part.

## Questions to answer before deciding

- How do you *test* that pages arrive when triage is down?
- How do you know triage is down before a real incident tells you?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiment 2
