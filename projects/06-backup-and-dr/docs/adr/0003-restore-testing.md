# ADR-0003: How restores are tested

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Backup jobs that "succeed" can produce empty, truncated, or unrestorable files. You only find out during the incident.

## Options considered

### Option 1: Monitor backup job success only
- **Pros:** Easy.
- **Cons:** Proves nothing about restorability.

### Option 2: Automated scheduled restore drill with validation (starter default: weekly CI)
- **Pros:** Continuous evidence. Measures real RTO. Catches format/version issues.
- **Cons:** Costs compute. Validation queries need maintenance as the schema changes.

### Option 3: Option 2 + periodic human game days (full DR, including DNS and app cutover)
- **Pros:** Tests people, runbooks and access, not just data.
- **Cons:** Time-consuming; needs scheduling and a safe environment.

## Questions to answer before deciding

- What does "valid" mean for a restore? (Row counts? Checksums? App smoke test against the restored DB?)
- Where do drill results go, and who looks at a failed one?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


