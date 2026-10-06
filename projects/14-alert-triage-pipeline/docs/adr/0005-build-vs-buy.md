# ADR-0005: Build vs buy

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

PagerDuty, Opsgenie, incident.io and others offer event rules, enrichment, deduplication and routing.

## Options considered

### Option 1: Build (this project)
- **Pros:** Full control; uses your catalog directly; no per-user fees.
- **Cons:** You own a critical service.

### Option 2: Buy
- **Pros:** Mature on-call, escalation, mobile apps, reliability SLAs.
- **Cons:** Cost; enrichment limited to integrations; correlation rules in a vendor UI.

### Option 3: Buy for paging and on-call, build the enrichment and correlation in front of it
- **Pros:** Each part does what it's best at.
- **Cons:** Two places to look when something goes wrong.

## Questions to answer before deciding

- Which parts of this project would you keep if the firm already had PagerDuty?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


