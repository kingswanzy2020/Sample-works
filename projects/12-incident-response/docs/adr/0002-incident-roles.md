# ADR-0002: Incident roles and declaring an incident

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Without roles, the most senior person debugs and nobody coordinates or communicates.

## Options considered

### Option 1: No formal roles; the first responder handles it
- **Pros:** No overhead.
- **Cons:** Breaks down past one person; communication is forgotten.

### Option 2: Incident Command System-style roles (IC, ops, comms, scribe), scaled by severity
- **Pros:** Clear ownership; proven in many SRE organisations.
- **Cons:** Needs training and practice; heavy for small incidents.

### Option 3: IC + responders only, with comms delegated to a template/bot
- **Pros:** Light.
- **Cons:** Comms quality depends on the IC remembering.

## Questions to answer before deciding

- With only two people, who does what?
- When is something "an incident" vs "a problem we're looking at"? Is it OK to declare early and downgrade?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

game day timelines
