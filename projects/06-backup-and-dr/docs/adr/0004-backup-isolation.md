# ADR-0004: Protecting backups from deletion and compromise

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Ransomware and compromised credentials target backups first. If prod admin can delete backups, an attacker with prod admin can too.

## Options considered

### Option 1: Same account, same credentials
- **Pros:** Simple.
- **Cons:** One compromise destroys data and backups.

### Option 2: Versioning + writer role without delete permission
- **Pros:** Accidental and job-level deletes are recoverable.
- **Cons:** An account admin can still delete versions.

### Option 3: Separate backup account + object lock (governance/compliance) + cross-region (starter terraform)
- **Pros:** Survives prod account compromise and region loss.
- **Cons:** Compliance mode is irreversible until expiry, so mistakes cost money. Cross-account IAM is more complex.

## Questions to answer before deciding

- Governance vs compliance mode: who should be able to bypass, if anyone?
- Retention: how long? (Legal requirements? Cost?)

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiment 3
