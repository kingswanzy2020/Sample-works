# ADR-0003: Report gaps vs enforce the standard

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

A standard nobody enforces is a suggestion. A standard enforced too hard gets bypassed.

## Options considered

### Option 1: Report only (dashboard / weekly email)
- **Pros:** No friction.
- **Cons:** Gaps persist; reports get ignored.

### Option 2: Gate new services and tier changes (CI check on catalog changes, or a launch checklist)
- **Pros:** New gaps can't appear.
- **Cons:** Existing gaps remain; needs an exception process.

### Option 3: Report for existing services, gate for new ones, deadline for old gaps
- **Pros:** Balances progress and fairness.
- **Cons:** Needs tracking (project 17).

## Questions to answer before deciding

- What should the scanner's exit code be, and where does it run?
- Who can grant an exception, for how long?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


