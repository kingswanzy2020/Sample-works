# ADR-0001: Backup strategy for Postgres

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

The `items` table is the only data that can't be recreated. Targets come from `docs/rpo-rto.md`.

## Options considered

### Option 1: Logical dumps (`pg_dump`) on a schedule (starter default)
- **Pros:** Portable across versions, easy to restore a single table, simple.
- **Cons:** RPO = schedule interval (hours). Slow for large DBs. Restore time grows with data size.

### Option 2: Storage snapshots (EBS / RDS automated snapshots)
- **Pros:** Fast to take, managed.
- **Cons:** Coarse RPO, tied to one cloud. Restore = new instance (minutes to hours).

### Option 3: Base backup + continuous WAL archiving (pgBackRest, WAL-G, RDS PITR)
- **Pros:** Point-in-time recovery: RPO of seconds to minutes. Can restore to "just before the bad `DELETE`".
- **Cons:** More moving parts. Must monitor that WAL archiving keeps up.

### Option 4: Streaming replica
- **Pros:** Fastest failover, lowest RPO.
- **Cons:** **Not a backup:** a `DROP TABLE` replicates instantly. Always pair it with Option 3.

## Questions to answer before deciding

- What is the DB size today and in a year? How does restore time scale?
- Which failures does each option *not* protect against? (Bad deploy deleting rows? Region loss? Ransomware?)

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

docs/drills/ reports
