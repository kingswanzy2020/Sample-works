# ADR-0004: Self-hosted vs managed Kafka

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Kafka is stateful, critical and operationally demanding: upgrades, rebalancing, disk, and broker replacement.

## Options considered

### Option 1: Self-hosted on VMs/bare metal (managed with project 11's Ansible)
- **Pros:** Full control, lowest latency possible (co-location, tuned hosts). Common at trading firms.
- **Cons:** You own upgrades, disk failures, rebalancing, and 3am pages.

### Option 2: Self-hosted on Kubernetes (Strimzi operator)
- **Pros:** An operator automates rolling upgrades and config. Fits a k8s platform (projects 03, 08).
- **Cons:** Stateful sets plus network overhead. Debugging spans two complex systems.

### Option 3: Managed (Amazon MSK, Confluent Cloud)
- **Pros:** Little ops burden, SLAs.
- **Cons:** Cost at volume, less tuning control, higher latency, and cloud dependency for a trading-critical path.

## Questions to answer before deciding

- Is this feed latency-critical (co-located with exchanges) or analytics-grade?
- How many hours per month would self-hosting cost you? (Use your break-it postmortems as evidence.)

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


