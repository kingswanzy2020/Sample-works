# ADR-0003: Rolling change strategy

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

A bad change applied to every server at once is an outage. Applied to one server first, it's a finding.

## Options considered

### Option 1: All at once (default `forks`)
- **Pros:** Fastest.
- **Cons:** Blast radius = the whole fleet.

### Option 2: Fixed batches (`serial`) with a failure threshold (`max_fail_percentage`)
- **Pros:** Limits damage; stops automatically.
- **Cons:** Ansible only knows a *task* failed, not that the *service* is broken.

### Option 3: Canary host first, then batches, with a real health check between batches
- **Pros:** Catches "applied fine, broke the service".
- **Cons:** Slower; health checks must be meaningful (project 03's readiness lessons apply).

## Questions to answer before deciding

- For a trading fleet: should changes be allowed during market hours at all? (Connects to 12/16.)
- What exactly does your health gate check?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiment 3
