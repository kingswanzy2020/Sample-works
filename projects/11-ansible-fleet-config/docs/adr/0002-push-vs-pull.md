# ADR-0002: Push vs pull

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Someone or something has to run Ansible. That decides how fast changes land and how drift gets corrected.

## Options considered

### Option 1: Push from an engineer's machine
- **Pros:** Immediate, simple.
- **Cons:** No audit trail; "works from my laptop" problems; credentials on laptops.

### Option 2: Push from CI / a control node (AWX, Semaphore, a CI job) on merge
- **Pros:** Reviewed changes, audit log, central credentials.
- **Cons:** The control node needs network access to every host.

### Option 3: Pull (`ansible-pull` on a timer, or an agent-based tool)
- **Pros:** Scales; hosts self-correct drift on a schedule; no central inbound access.
- **Cons:** No single view of "did it apply everywhere?" without extra reporting. Rollout control is harder.

## Questions to answer before deciding

- How quickly must an emergency change reach the whole fleet?
- How do you know a host *didn't* apply a change?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


