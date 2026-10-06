# ADR-0001: Severity model

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Severity decides who gets woken up, how fast, and who is told. If it's unclear, everything gets treated as Sev1 or nothing does.

## Options considered

### Option 1: Impact-based levels (user/business impact only)
- **Pros:** Clear for non-engineers.
- **Cons:** Needs good impact signals; engineers may struggle to estimate impact quickly.

### Option 2: Impact × time (same failure is Sev1 during market hours, Sev3 overnight)
- **Pros:** Matches how a trading business actually feels the impact.
- **Cons:** More complex; overnight batch failures can still threaten the next market open.

### Option 3: Symptom-based (which alert fired determines severity)
- **Pros:** Automatable (project 14 can set it).
- **Cons:** Alerts don't know business impact; they'll be wrong sometimes.

## Questions to answer before deciding

- Classify every landscape service at market open, midday and overnight.
- Who can change severity mid-incident?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


