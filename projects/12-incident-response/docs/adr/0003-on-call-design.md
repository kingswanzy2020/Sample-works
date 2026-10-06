# ADR-0003: On-call design

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

The landscape has services with clear on-call, and some with none (risk-engine, reporting-batch).

## Options considered

### Option 1: Each team owns on-call for its services
- **Pros:** The people who know the service get the page.
- **Cons:** Small teams get burned out. Unowned services fall through.

### Option 2: Central SRE/first-line handles all first response, escalates to teams
- **Pros:** Consistent triage; protects teams' time.
- **Cons:** First-line needs good runbooks and context (project 14 helps).

### Option 3: Hybrid: first-line for tier-1 during market hours, team on-call otherwise
- **Pros:** Matches business hours and risk.
- **Cons:** More rules; handoffs at the boundaries.

## Questions to answer before deciding

- What happens *today* if risk-engine goes down? Run that scenario and find out.
- What's a sustainable number of pages per shift?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

game day: risk-engine-down
