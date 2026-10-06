# ADR-0003: CI-to-cloud authentication (OIDC) and trust scoping

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

CI needs cloud access. Long-lived access keys in GitHub secrets can be exfiltrated by any workflow change or compromised action.

## Options considered

### Option 1: Long-lived IAM user keys in GitHub secrets
- **Pros:** Works everywhere, two minutes to set up.
- **Cons:** Never expire unless rotated. Any workflow (including from a malicious PR, depending on settings) can read them.

### Option 2: OIDC federation, one role, `sub` = `repo:owner/repo:*`
- **Pros:** No stored keys, short-lived credentials.
- **Cons:** Any branch, and any PR workflow, gets the same power, including prod.

### Option 3: OIDC with separate roles: read-only plan for any ref, apply only for `environment:prod` with required reviewers (starter default)
- **Pros:** Least privilege per stage. Prod access requires a protected environment approval.
- **Cons:** More roles and conditions to maintain. Easy to get the `sub` format wrong.

## Questions to answer before deciding

- What exactly is in the `sub` claim for a PR, a branch push, and an environment job?
- Could another repo in your account assume the role? (Test it: break-it experiment 4.)

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


