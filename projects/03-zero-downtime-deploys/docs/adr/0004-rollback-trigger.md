# ADR-0004: Automatic vs manual rollback

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

When a deploy goes bad, someone has to notice and act. Each minute adds user impact.

## Options considered

### Option 1: Manual (`kubectl rollout undo` or Service selector flip)
- **Pros:** A human judges context.
- **Cons:** Needs someone watching. Slower at night.

### Option 2: Automatic on analysis failure (Argo Rollouts)
- **Pros:** Fast, consistent.
- **Cons:** False positives roll back good deploys. A rollback is unsafe if a non-backward-compatible migration already ran.

### Option 3: Automatic pause + page a human
- **Pros:** Limits blast radius, human makes the final call.
- **Cons:** Still needs on-call.

## Questions to answer before deciding

- Is every migration you ship safe to run with the previous app version? If not, auto-rollback is dangerous.

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiment 4
