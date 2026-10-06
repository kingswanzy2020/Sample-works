# ADR-0005: Build once, promote by digest

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

If staging and prod each rebuild the image, they can contain different dependencies.
"It worked in staging" then proves nothing.

## Options considered

### Option 1: Rebuild per environment
- **Pros:** Simple per-env build args.
- **Cons:** Not the same artifact. Non-reproducible builds pull newer base images/deps.

### Option 2: Build once, promote the **digest** (starter `promote.yml`)
- **Pros:** The exact bytes that were tested are deployed. Signature verified before promote.
- **Cons:** Config must come from the environment (env vars / config maps), not build args.

### Option 3: GitOps: CI writes the digest into an environment repo; ArgoCD/Flux deploys (see project 08)
- **Pros:** Full audit trail in git; easy rollback with `git revert`.
- **Cons:** Two repos and a controller to operate.

## Questions to answer before deciding

- Do environment tags (`:staging`, `:prod`) get mutated? Is that acceptable, or should deploys always reference digests?
- How do you roll back? (What digest was running before?)

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


