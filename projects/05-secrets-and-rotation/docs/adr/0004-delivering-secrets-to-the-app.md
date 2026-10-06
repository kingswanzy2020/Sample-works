# ADR-0004: Delivering secrets to the app

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

However secrets are stored, the app must receive them, and receive *new* ones after rotation.

## Options considered

### Option 1: Environment variables
- **Pros:** Universal (12-factor).
- **Cons:** Fixed at process start, so rotation needs a restart. Visible in `docker inspect`, `/proc/<pid>/environ`, crash dumps.

### Option 2: File rendered by a sidecar/agent, re-read on use (starter default: Vault Agent + `DATABASE_URL_FILE`)
- **Pros:** Rotation without restart. App stays secrets-store-agnostic.
- **Cons:** A sidecar per pod. The app must re-read (the shared app re-reads on every connection, which is fine without a pool).

### Option 3: App calls the secrets store SDK directly
- **Pros:** Full control over leases and renewal.
- **Cons:** Couples the app to one vendor. Every service reimplements it.

### Option 4: Kubernetes Secret synced by External Secrets Operator
- **Pros:** Native to k8s, works with any store.
- **Cons:** The secret is copied into etcd (is etcd encrypted?). Mounted secrets update in ~1 min; env-var secrets never update.

## Questions to answer before deciding

- With a connection pool, when do new connections pick up new creds? What happens to old ones?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


