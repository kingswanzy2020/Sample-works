# ADR-0004: Prioritising gaps

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

The first full scan will find many gaps. You can't close them all at once.

## Options considered

### Option 1: By tier only
- **Pros:** Simple.
- **Cons:** A tier-2 dependency of three tier-1 services may matter more than a tier-1 leaf.

### Option 2: Risk score: tier × blast radius (dependents) × likelihood (incident history from 12)
- **Pros:** Targets the gaps most likely to hurt.
- **Cons:** The score is a judgement; write down the formula.

### Option 3: Cheapest first
- **Pros:** Quick visible progress.
- **Cons:** May leave the riskiest gaps open.

## Questions to answer before deciding

- Which single gap would most have shortened a game-day incident?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

docs/gap-backlog.md
