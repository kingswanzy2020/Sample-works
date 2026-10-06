# ADR-0002: GitOps pull vs CI push

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Something has to apply manifests to clusters. That something needs cluster credentials and is the deploy audit trail.

## Options considered

### Option 1: CI pushes (`kubectl apply` / `helm upgrade` from Actions)
- **Pros:** Simple, one system.
- **Cons:** CI holds cluster-admin-ish credentials. No drift correction. The audit trail lives in CI logs.

### Option 2: GitOps pull (Argo CD / Flux) (starter)
- **Pros:** Cluster pulls from git, so no inbound credentials. Self-heals drift. Rollback = `git revert`. Git history = deploy history.
- **Cons:** Another controller to run. Image updates need a commit (bot or CI). Debugging is "why isn't it syncing?"

## Questions to answer before deciding

- Should self-heal be on in prod? During an incident, a manual hotfix gets reverted (compare project 01 ADR-0004).
- One repo for all environments, or one per environment? Who can merge to prod paths (CODEOWNERS)?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiment 3
