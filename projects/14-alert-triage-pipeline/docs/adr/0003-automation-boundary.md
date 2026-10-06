# ADR-0003: Automation boundary

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Once triage knows a lot, it's tempting to let it fix things. Wrong automation at 3am makes incidents bigger.

## Options considered

### Option 1: Information only (enrich + read-only diagnostics)
- **Pros:** Can't make anything worse.
- **Cons:** A human still has to act on every alert.

### Option 2: Suggested actions with one-click execution by a human
- **Pros:** Faster, still human-approved; good audit trail (project 13's framework).
- **Cons:** People click without thinking under pressure.

### Option 3: Automatic remediation for a short, explicit allow-list
- **Pros:** Fastest for known, safe cases.
- **Cons:** Needs strong preconditions and a kill switch; can hide recurring problems.

## Questions to answer before deciding

- Which actions from project 13 are safe to suggest? Which, if any, to run automatically?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


