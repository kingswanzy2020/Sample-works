# ADR-0004: Cost allocation, budgets and ownership

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

"The bill doubled" is unanswerable without knowing who spent what. Costs without owners don't get fixed.

## Options considered

### Option 1: Monthly look at the bill
- **Pros:** Zero effort.
- **Cons:** Finds problems weeks late, with no owner.

### Option 2: Mandatory tags/labels (Project, Environment, Team, CostCenter) + budgets with forecast alerts (starter)
- **Pros:** Per-owner cost; early warning.
- **Cons:** Tags must be enforced (policy as code), otherwise "untagged" becomes the biggest line item.
  Shared costs (NAT, control plane) still need an allocation rule.

### Option 3: Option 2 + in-cluster allocation (OpenCost/Kubecost) + showback/chargeback
- **Pros:** Cost per namespace/team inside shared clusters.
- **Cons:** Another tool; chargeback is political.

## Questions to answer before deciding

- How do you enforce tags? (Project 01 `default_tags`, policy checks in CI, SCPs.)
- How do you split a shared cluster's idle capacity among teams?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


