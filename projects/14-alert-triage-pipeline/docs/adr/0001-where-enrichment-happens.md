# ADR-0001: Where enrichment happens, and what to add

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Responders need owner, runbook, dependencies and recent changes. That context can be added in different places.

## Options considered

### Option 1: In the alert rules (labels/annotations)
- **Pros:** Simple; no extra service; visible in Alertmanager.
- **Cons:** Static: the rule can't know who's on call now, or the dependency's current health. Duplicated across rules.

### Option 2: In a pipeline service at alert time (starter)
- **Pros:** Live data (catalog, on-call, health, deploys); one place to change.
- **Cons:** A new critical service; must be fast and fail open.

### Option 3: In the incident tool (PagerDuty/incident.io enrichment, service catalog integrations)
- **Pros:** No code.
- **Cons:** Limited to what the vendor supports; data lives outside your control.

## Questions to answer before deciding

- From project 12's timelines: which lookups cost responders the most time?
- What's the time budget for enrichment before a page must go out?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

game day timings
