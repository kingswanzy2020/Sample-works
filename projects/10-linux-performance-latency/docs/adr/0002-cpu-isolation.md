# ADR-0002: CPU isolation strategy

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

The latency-critical process shares cores with everything else: other processes, kernel threads, interrupts.

## Options considered

### Option 1: No isolation
- **Pros:** Simple. Full use of all cores.
- **Cons:** Any neighbour can steal the core at the worst moment.

### Option 2: Affinity / cgroup cpusets (pin the service, keep others off its cores)
- **Pros:** No reboot. Works in containers (cpuset).
- **Cons:** Kernel threads, timers and IRQs still land on "your" cores.

### Option 3: Kernel isolation (`isolcpus`, `nohz_full`, `rcu_nocbs`) + IRQ affinity
- **Pros:** The quietest cores Linux can give you.
- **Cons:** Reboot to change. Isolated cores are wasted when idle. Easy to misconfigure. Needs fleet-wide config management (project 11).

## Questions to answer before deciding

- Which noise mode in `docs/break-it.md` did each option fix, and which didn't it fix?
- How many cores can the business afford to leave idle for latency?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

tuning-log rows
