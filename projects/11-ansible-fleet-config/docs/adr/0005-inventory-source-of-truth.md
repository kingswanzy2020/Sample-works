# ADR-0005: Inventory source of truth

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

The inventory says which servers exist and what they are. If it's wrong, Ansible configures the wrong things, or misses servers.

## Options considered

### Option 1: Static INI/YAML in git (starter)
- **Pros:** Simple, reviewable.
- **Cons:** Goes stale as servers are added and removed.

### Option 2: Dynamic inventory from the cloud provider / hypervisor API
- **Pros:** Always reflects reality.
- **Cons:** Groups depend on tags being correct; bare metal may not be in any API.

### Option 3: Generated from the service catalog / CMDB (the landscape's `catalog.yaml` idea)
- **Pros:** One source of truth for ownership *and* configuration.
- **Cons:** The catalog must be trustworthy (project 17 shows how often it isn't).

## Questions to answer before deciding

- How would you detect a server that exists but isn't in the inventory?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


