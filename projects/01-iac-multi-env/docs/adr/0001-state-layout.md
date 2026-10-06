# ADR-0001: How to split Terraform state

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

All infrastructure (network, database, later the cluster and app) is described in Terraform.
State records what Terraform thinks exists. How you split it decides:
- **Blast radius:** what a single bad `apply` can touch.
- **Lock contention:** who has to wait for whom.
- **Wiring cost:** how much plumbing you need to pass outputs between states.

## Options considered

### Option 1: One state for everything
- **Pros:** Simplest. Cross-resource references just work. One `plan` shows everything.
- **Cons:** A staging change can destroy prod. Plans slow down as the codebase grows. One lock for everyone.

### Option 2: One state per environment (starter default)
- **Pros:** Staging cannot touch prod. Still simple wiring within an environment.
- **Cons:** Network and DB share a state, so a DB change still plans (and locks) the network.

### Option 3: One state per environment *and* per component (network / data / compute)
- **Pros:** Smallest blast radius. The DB can't be destroyed by a networking PR. Faster plans.
- **Cons:** You must pass outputs between states (`terraform_remote_state`, SSM parameters, or data lookups).
  You need ordering when building from nothing.

## Questions to answer before deciding

- How many people will run Terraform at the same time?
- Which resource would hurt most to destroy by accident? Should it share a state with things that change weekly?
- How often does each component change?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

(link break-it experiment 3: state lock / corruption)
