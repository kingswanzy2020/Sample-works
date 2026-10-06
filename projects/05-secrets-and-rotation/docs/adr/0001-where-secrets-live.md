# ADR-0001: Where secrets live

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Secrets are in `.env` files and CI variables, with no audit trail, no rotation and no central revocation.

## Options considered

### Option 1: SOPS + age/KMS, encrypted in git
- **Pros:** Versioned with code, reviewable diffs, no extra service to run.
- **Cons:** Revoking access means re-encrypting **and rotating** every secret the person could read (they have old ciphertext + key).
  No dynamic secrets. No access audit.

### Option 2: Cloud secrets manager (AWS Secrets Manager / GCP Secret Manager)
- **Pros:** Managed, IAM-integrated, audit via CloudTrail, built-in rotation for RDS.
- **Cons:** Per-secret and per-API-call cost. Cloud-specific.

### Option 3: HashiCorp Vault (or OpenBao)
- **Pros:** Dynamic secrets for many backends, leases, fine-grained policies, multi-cloud.
- **Cons:** You operate a critical, stateful, security-sensitive cluster (unseal, HA, backups, upgrades).

## Questions to answer before deciding

- How many secrets, how many consumers, how many clouds?
- Who will be on call for the secrets system?
- Offboarding: walk through removing one engineer's access in each option.

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


