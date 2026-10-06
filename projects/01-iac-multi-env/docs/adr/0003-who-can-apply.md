# ADR-0003: Where `apply` is allowed to run

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Right now anyone with AWS admin credentials can run `terraform apply` from a laptop.
That makes changes unauditable and leaves long-lived credentials on laptops.

## Options considered

### Option 1: Laptops, with a convention ("always open a PR first")
- **Pros:** Fast feedback, no CI setup.
- **Cons:** Conventions get skipped at 2am. No audit trail tying an apply to a reviewed plan.

### Option 2: CI applies on merge to `main`
- **Pros:** Every change is reviewed. CI uses short-lived OIDC credentials.
- **Cons:** The plan reviewed on the PR may not be the plan applied after merge (main moved, or drift).
  Need a break-glass path for emergencies.

### Option 3: PR-driven apply (Atlantis / Terraform Cloud / Spacelift)
- **Pros:** Apply the exact reviewed plan *before* merge; locks per directory.
- **Cons:** Another service to run or pay for. Overkill for one person.

## Questions to answer before deciding

- Separate IAM roles for `plan` (read-only) and `apply`? Who/what can assume each?
- What is the break-glass procedure, and how is its use audited?
- How do you guarantee the applied plan is the reviewed plan?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**
