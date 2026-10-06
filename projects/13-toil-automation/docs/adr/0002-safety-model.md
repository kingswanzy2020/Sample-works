# ADR-0002: Safety model

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Automation runs faster than humans, including when it's wrong. The starter framework defaults to dry-run,
limits targets to 5 and logs everything. Those are *starting* choices for you to keep or change.

## Options considered

### Option 1: Dry-run by default, `--execute` to act (starter)
- **Pros:** Safe default; you see the plan first.
- **Cons:** Scheduled jobs must pass `--execute`, which makes that the default in practice there.

### Option 2: Confirmation prompt for changes above N targets
- **Pros:** A human checkpoint where it matters.
- **Cons:** Doesn't work unattended.

### Option 3: Preconditions per action (e.g. "never during market hours", "never if an incident is open")
- **Pros:** Encodes context humans would check.
- **Cons:** More logic to get right and test.

## Questions to answer before deciding

- What's the right `--max-targets` per action? Is one number right for all?
- Who reads the audit log, and when?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiments 1 and 2
