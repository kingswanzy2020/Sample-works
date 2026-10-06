# ADR-0004: Detect vs auto-remediate drift

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

`drift-detection.yml` runs `plan -detailed-exitcode` nightly. When drift is found, what happens next?

## Options considered

### Option 1: Detect and alert (starter default: opens a GitHub issue)
- **Pros:** A human decides whether the console change was a valid hotfix (codify it) or a mistake (revert it).
- **Cons:** Alerts get ignored. Drift can sit for days.

### Option 2: Auto-apply to revert drift
- **Pros:** Code is always the truth.
- **Cons:** Can undo an emergency hotfix in the middle of an incident. A bad commit plus auto-apply gives automatic damage.

### Option 3: Prevent drift (remove console write access, SCPs)
- **Pros:** Removes the cause.
- **Cons:** Slows down real incident response. Needs a break-glass path.

## Questions to answer before deciding

- Which resources are safe to auto-revert (tags?) vs never (security groups during an incident)?
- Who owns a drift issue, and what is the SLA for resolving one?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**
