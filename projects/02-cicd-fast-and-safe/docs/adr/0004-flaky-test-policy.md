# ADR-0004: Flaky test policy

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

A test fails ~1 in 10 runs. People press "re-run" until it is green. Trust in CI erodes,
and real failures get re-run too.

## Options considered

### Option 1: Automatic retries (e.g. `pytest-rerunfailures`)
- **Pros:** Green builds immediately.
- **Cons:** Hides real race conditions, including ones that also happen in prod.

### Option 2: Quarantine: move to a non-blocking job, open a ticket with an owner and a deadline
- **Pros:** Unblocks the team, keeps the signal visible.
- **Cons:** Quarantine becomes a graveyard without enforcement.

### Option 3: Fix-forward only: a flaky test is a P1 bug
- **Pros:** Highest quality.
- **Cons:** Can block delivery for days.

## Questions to answer before deciding

- How do you *detect* flakiness (same commit, different result)? Where is that tracked?
- Is the flake in the test or in the code? (A timing bug in the code is a prod bug.)

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiment 3 (flaky test)
