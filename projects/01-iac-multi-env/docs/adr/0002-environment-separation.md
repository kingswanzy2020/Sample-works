# ADR-0002: Workspaces vs directory-per-environment vs Terragrunt

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Staging and prod must use the same modules but different inputs, and they must not share state.

## Options considered

### Option 1: Terraform CLI workspaces
- **Pros:** One root module, so it's impossible for envs to diverge in wiring.
- **Cons:** The current workspace is invisible state on your laptop, so `apply` in the wrong workspace is easy.
  Both envs must share a backend and provider config. Per-env differences end up as `terraform.workspace` conditionals.

### Option 2: Directory per environment (starter default)
- **Pros:** Explicit: you `cd` into the environment you mean. Per-env backend, provider and even provider version.
  Easy to read in a PR.
- **Cons:** Duplicated wiring (`main.tf` exists twice). Envs can drift *in code* if someone edits one file and not the other.

### Option 3: Terragrunt
- **Pros:** DRY backend and provider config. Dependency ordering between components (pairs well with ADR-0001 Option 3).
- **Cons:** Another tool to learn and pin. Interviewers will ask "why not plain Terraform?", so you need a real reason.

## Questions to answer before deciding

- What stops someone applying prod when they meant staging, in each option?
- How would you detect the two `main.tf` files diverging (if you choose Option 2)?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**
