# ADR-0002: Static vs dynamic credentials

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

A static DB password is shared by all pods, never expires, and is hard to rotate without downtime.

## Options considered

### Option 1: Static password, rotated manually or on a schedule
- **Pros:** Simple. Works with everything.
- **Cons:** Rotation is a risky event. A leaked password stays valid until someone notices.

### Option 2: Dual-credential rotation (two users, alternate which is active)
- **Pros:** Zero-downtime rotation without Vault. RDS/Secrets Manager supports this ("alternating users").
- **Cons:** Still long-lived (days/weeks).

### Option 3: Dynamic per-instance credentials (Vault database engine, starter default)
- **Pros:** Each instance has its own user, so you know who did what. Leaks expire in minutes.
- **Cons:** Many DB roles get created. Connection pools must handle credential changes. Tight dependency on Vault.

### Option 4: IAM database authentication (RDS IAM auth / Cloud SQL IAM)
- **Pros:** No password at all; 15-minute tokens from the workload's cloud identity.
- **Cons:** Cloud-specific, connection rate limits, not all tools support it.

## Questions to answer before deciding

- Long-lived pooled connections outlive the credential's `VALID UNTIL`. Is that OK? (Postgres checks it only at login.)
- How many DB roles exist at steady state with a 1-minute lease, 3-minute max TTL and N pods?
- Renewal vs rotation: renewing extends the same user's lifetime; only `max_ttl` forces a new user. Which one limits a leak's lifetime?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

scripts/rotation-under-load.sh output; break-it experiment 2
