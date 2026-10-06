# ADR-0005: Developer portal: build vs buy

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

A portal gives a catalog (who owns what), templates, docs and scorecards in one place.

## Options considered

### Option 1: No portal: template repo + README + scorecard script (starter fallback)
- **Pros:** Zero ops.
- **Cons:** Discoverability; no catalog.

### Option 2: Backstage (open source)
- **Pros:** Flexible, large plugin ecosystem, free licence.
- **Cons:** A TypeScript app you build, upgrade and staff. Often underestimated.

### Option 3: Commercial portal (Port, Cortex, Roadie for hosted Backstage)
- **Pros:** Fast to adopt, maintained for you.
- **Cons:** Per-seat cost, less flexibility, data leaves your control.

## Questions to answer before deciding

- How many engineers would use it? At 10 engineers, is a portal solving a real problem?
- Who maintains Backstage upgrades, and how many hours per month is that?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


