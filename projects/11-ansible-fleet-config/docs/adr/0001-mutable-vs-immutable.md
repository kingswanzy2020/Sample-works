# ADR-0001: Mutable configuration vs immutable images

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Long-lived servers accumulate changes. You can keep correcting them (mutable) or keep replacing them (immutable).

## Options considered

### Option 1: Mutable: Ansible converges long-lived hosts
- **Pros:** Works for bare metal and stateful hosts (Kafka brokers, databases, latency hosts). Small, fast changes.
- **Cons:** Drift between runs. The order of past changes affects the result.

### Option 2: Immutable: bake images (Packer + Ansible inside the build), replace hosts to change
- **Pros:** Every host is exactly the image. Rollback = previous image.
- **Cons:** Replacing bare metal or stateful hosts is slow or impossible. Image pipeline to maintain.

### Option 3: Hybrid: immutable base image, Ansible for the thin host-specific layer
- **Pros:** Most of the benefits of both.
- **Cons:** You must define the boundary clearly, or you get the worst of both.

## Questions to answer before deciding

- Which servers in this fleet can be replaced in minutes, and which can't?
- Where does Terraform (project 01) stop and Ansible start?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


