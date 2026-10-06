# ADR-0002: DR topology

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Backups recover data. DR recovers the *service*: infra, app, config, DNS, people.

## Options considered (cheapest/slowest first)

### Option 1: Backup and restore
- **Pros:** Lowest cost. Rebuild infra with Terraform (project 01), restore data.
- **Cons:** RTO of hours. Depends on your IaC actually working in another region.

### Option 2: Pilot light (data replicated, minimal infra running in DR region)
- **Pros:** RTO of tens of minutes.
- **Cons:** Ongoing cost of replication + standby DB.

### Option 3: Warm standby (scaled-down full stack in DR region)
- **Pros:** RTO of minutes.
- **Cons:** Significant cost. Drift between regions.

### Option 4: Multi-region active-active
- **Pros:** Near-zero RTO.
- **Cons:** Very high complexity (data consistency, conflicts). Rarely justified.

## Questions to answer before deciding

- Annual expected cost of downtime (probability × duration × cost/hour) vs annual cost of each option.
- Has the project 01 Terraform ever been applied to a second region? (Experiment 4.)

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiment 4 (region loss game day)
