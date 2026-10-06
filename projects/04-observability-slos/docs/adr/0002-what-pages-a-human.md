# ADR-0002: What pages a human

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Pages at 3am must mean "users are hurting now and a human must act." Everything else is a ticket or a dashboard.

## Options considered

### Option 1: Threshold alerts on causes (CPU > 80%, memory > 90%, error count > 10)
- **Pros:** Familiar, easy to write.
- **Cons:** High CPU with happy users is fine. Low traffic periods make counts meaningless. Fatigue sets in.

### Option 2: Multi-window burn-rate alerts on SLOs (starter default)
- **Pros:** Pages only when the budget is burning fast. A slow burn becomes a ticket. Low false positives.
- **Cons:** Harder to explain. Needs enough traffic for ratios to be stable.

### Option 3: Option 2 + cause alerts as *tickets only* (disk filling, cert expiring)
- **Pros:** Catches the things that will become outages.
- **Cons:** More rules to maintain.

## Questions to answer before deciding

- At 1 req/min, one error = 100% error ratio for that minute. How do the alerts behave? (Starter: `sli:requests:rate5m > 0.5` guard on latency.)
- Which alerts have a runbook? An alert without a runbook is not ready to page.

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiment 4 (alert fatigue)
