# ADR-0004: Containers vs bare metal for latency-critical services

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

The platform (projects 03, 07, 08) runs on Kubernetes. Should the latency-critical path too?

## Options considered

### Option 1: Bare metal / dedicated hosts, configured by Ansible (project 11)
- **Pros:** Full control of cores, IRQs, NICs. The lowest jitter.
- **Cons:** A separate operating model from the rest of the platform.

### Option 2: Kubernetes with the static CPU manager policy + Guaranteed QoS + dedicated nodes
- **Pros:** One platform. Exclusive cores per pod are possible.
- **Cons:** Network overlay, kubelet, sidecars and noisy daemons on the node. More layers to debug.

### Option 3: Containers on dedicated hosts without an orchestrator
- **Pros:** Packaging benefits, host-level control.
- **Cons:** You rebuild scheduling and failover yourself.

## Questions to answer before deciding

- Measure: same workload in a container with CPU *limits* vs pinned (cpuset) vs bare. What's the difference at p99.9?
- What does the business lose by having two operating models?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiment 5
