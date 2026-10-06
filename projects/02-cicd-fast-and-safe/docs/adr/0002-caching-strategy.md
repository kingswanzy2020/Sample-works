# ADR-0002: Caching strategy

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Dependency installs and Docker builds dominate CI time. Caching cuts that, but a cache
that serves stale or wrong content produces builds that pass in CI and fail in prod.

## Options considered

### Option 1: No cache
- **Pros:** Every build is reproducible from scratch.
- **Cons:** Slow.

### Option 2: Dependency cache keyed on lockfile hash + GHA Docker layer cache (starter default)
- **Pros:** Large speedup with almost no setup.
- **Cons:** GHA cache is limited in size and evicts. It is scoped per branch, with fallback to the default branch.
  Unpinned `apt-get`/`pip` lines inside cached layers silently go stale.

### Option 3: Registry-backed cache (`type=registry`) or a remote build cache
- **Pros:** Shared across branches and runners. Larger.
- **Cons:** Registry storage cost. Cache becomes an attack surface (who can write to it?).

## Questions to answer before deciding

- What is in the cache key? What change *should* invalidate it but doesn't?
- How would you detect a poisoned cache? (Weekly `--no-cache` build that compares results?)

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiment 1 (cache poisoning)
