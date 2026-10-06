# ADR-0005: Behaviour when the secrets store is down

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Centralizing secrets creates a dependency. If Vault (or the cloud API) is down, new pods can't start and dynamic creds can't renew.

## Options considered

### Option 1: Fail closed: no secret, no start
- **Pros:** Never runs with stale or missing config.
- **Cons:** A Vault outage becomes a full outage after the lease TTL.

### Option 2: Longer TTLs + cached last-known secret
- **Pros:** Survives store outages up to the TTL.
- **Cons:** Larger window for leaked creds.

### Option 3: HA store (Vault raft cluster / managed service SLA) + alerting on lease renewal failures
- **Pros:** Reduces the probability rather than designing around it.
- **Cons:** Cost and operational effort.

## Questions to answer before deciding

- With a 1m lease (renewed up to 3m), how long until the app fails after Vault dies? Measure it (break-it experiment 1).
- Can you deploy during a Vault outage? Should you be able to?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiment 1
