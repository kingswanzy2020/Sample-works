# ADR-0002: SLO tooling

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

SLOs can be hand-written rules, generated from a spec, or managed in a vendor tool.

## Options considered

### Option 1: Simple in-house YAML read by your report (starter)
- **Pros:** Transparent; no extra tools.
- **Cons:** You'll reinvent burn-rate alerts and dashboards.

### Option 2: Sloth or Pyrra (generate Prometheus recording + alerting rules from a spec)
- **Pros:** Battle-tested rules; consistent burn-rate alerts across services.
- **Cons:** Another tool and spec format to learn.

### Option 3: OpenSLO spec as the source of truth, translated to whatever runs it
- **Pros:** Vendor-neutral standard.
- **Cons:** Tooling support varies.

## Questions to answer before deciding

- Should SLO alerts (project 04 style) come from the same spec as the report? If not, how do they stay in sync?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


