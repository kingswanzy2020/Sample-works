# ADR-0003: Escalation and SRE's own authority

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

SRE usually can't order other teams to fix things. Some findings will be ignored.

## Options considered

### Option 1: No escalation; persuasion only
- **Pros:** Good relationships.
- **Cons:** Important issues stay open indefinitely.

### Option 2: Time-based escalation (overdue N weeks → team lead → engineering head)
- **Pros:** Predictable and fair.
- **Cons:** Can feel bureaucratic.

### Option 3: Escalation + limited unilateral authority (e.g. SRE may downgrade a noisy page to a ticket after notice; risk acceptance must be signed by the service owner's manager)
- **Pros:** Protects on-call immediately; makes "won't fix" an explicit, owned decision.
- **Cons:** Needs leadership agreement on what SRE may do.

## Questions to answer before deciding

- What's the difference between "they won't fix it" and "they've accepted the risk"? Who signs that?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


