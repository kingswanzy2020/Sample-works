# ADR-0002: Requests, limits and right-sizing

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Requests decide scheduling **and cost** (nodes are bought for requested, not used, resources).
They also decide HPA percentages. The starter values are guesses.

## Options considered

### Option 1: Generous requests and limits "to be safe"
- **Pros:** Few OOMs or throttling.
- **Cons:** You pay for idle reservations. HPA thinks utilization is low and scales late.

### Option 2: Requests from VPA recommendations (P90 usage + headroom); memory limit = request; no CPU limit (starter direction)
- **Pros:** Pays for what is used. No CPU throttling on bursts.
- **Cons:** A runaway pod can use spare node CPU (noisy neighbour). Recommendations must be revisited.

### Option 3: VPA in auto mode
- **Pros:** Continuous right-sizing.
- **Cons:** Restarts pods to resize; conflicts with HPA on the same metric.

## Questions to answer before deciding

- CPU limits: what does throttling do to p99 latency? (Break-it experiment 2.)
- Memory: what happens at the limit? (OOMKill, not slowdown.) How much headroom is right?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiments 1 and 2
