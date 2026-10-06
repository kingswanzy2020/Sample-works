# ADR-0004: What stays human, what gets automated

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Every game day repeats some steps: look up the owner, find the runbook, check dependencies, check recent deploys.

## Options considered

### Option 1: Runbooks only
- **Pros:** Flexible; humans adapt.
- **Cons:** Slow and inconsistent under stress; runbooks rot.

### Option 2: Automate information gathering, keep decisions human
- **Pros:** Faster, consistent context; no risk of automation making things worse.
- **Cons:** Still needs a human to act.

### Option 3: Automate remediation for known, safe cases
- **Pros:** Fastest recovery.
- **Cons:** Wrong automation at 3am makes incidents bigger.

## Questions to answer before deciding

- List each step from your game-day timelines with its time cost. Which steps were pure lookup?
- This ADR is the input to project 14. Write down the list you'll hand over.

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

game day timelines
