# ADR-0002: White-box vs black-box monitoring

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

The landscape's alerts are all white-box (the service's own metrics). The `slow-postgres` game day showed they can miss things users feel.

## Options considered

### Option 1: White-box only
- **Pros:** Rich detail; cheap.
- **Cons:** If the service can't report (it's down, or the problem is between user and service), you see nothing.

### Option 2: Black-box only (synthetic probes)
- **Pros:** Sees what users see.
- **Cons:** Says *that* it's broken, not *why*. Probes test only the paths you script.

### Option 3: Both, with alerts primarily on black-box/SLO symptoms and white-box for diagnosis
- **Pros:** Catches user impact and explains it.
- **Cons:** More to maintain; probe traffic must be excluded from SLIs (project 04 lesson).

## Questions to answer before deciding

- Where should probes run from (same network, another region, outside)? What does each detect?
- Should probes run outside trading hours?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiment 1
