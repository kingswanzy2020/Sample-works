# ADR-0001: SLA vs SLO vs SLI, and the targets

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

The words get mixed up, and so do the commitments. An SLA is a promise with consequences, an SLO is an internal target,
and an SLI is the measurement.

## Options considered

### Option 1: Internal SLOs only
- **Pros:** Freedom to set ambitious targets and learn.
- **Cons:** Users (traders, desks) may not know or trust them.

### Option 2: SLOs internally, SLAs to internal customers (desks) with a looser target
- **Pros:** The SLO is your early warning before the SLA is breached.
- **Cons:** Two numbers to explain.

### Option 3: Targets based on current performance ("we're at 99.95%, so that's the SLO")
- **Pros:** Easy to meet.
- **Cons:** Says nothing about what users need. Locks in today's level.

## Questions to answer before deciding

- What do traders actually notice? (A 2-second outage at market open? A slow risk check?)
- Why is a dependency's SLO usually stricter than its dependents'?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


