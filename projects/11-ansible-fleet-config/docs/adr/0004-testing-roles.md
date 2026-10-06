# ADR-0004: Testing roles

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Roles are code. Untested roles are found broken on production servers.

## Options considered

### Option 1: `--check --diff` against real hosts
- **Pros:** Zero setup.
- **Cons:** Check mode can't predict everything (commands, things that depend on earlier changes).

### Option 2: Molecule (create a throwaway container/VM, converge, verify, check idempotence)
- **Pros:** Real runs, idempotence check built in, works in CI.
- **Cons:** Setup effort; containers can't test kernel-level roles.

### Option 3: A staging slice of the fleet
- **Pros:** Real hardware and real config.
- **Cons:** Staging drifts too; slower feedback.

## Questions to answer before deciding

- Which roles can be tested in containers, and which need VMs?
- What does "idempotent" mean for each role, and how do you prove it automatically?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


