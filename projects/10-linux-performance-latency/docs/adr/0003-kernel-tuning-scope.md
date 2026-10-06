# ADR-0003: Kernel and hardware tuning scope

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Many knobs affect tail latency: CPU frequency governor, deep C-states, transparent huge pages, swap, IRQ placement,
interrupt coalescing, busy polling. Each has a cost: power, throughput, or memory.

## Options considered

### Option 1: Vendor/OS profile (e.g. `tuned` `latency-performance` / `network-latency`)
- **Pros:** Sensible, documented defaults in one command.
- **Cons:** A black box unless you know what it changes. May not fit your workload.

### Option 2: Hand-picked knobs, each justified by a measurement
- **Pros:** Every change is understood and evidenced.
- **Cons:** Slow. Risk of cargo-culting from blog posts.

### Option 3: Leave defaults; fix at the application level (batching, avoiding syscalls, allocation)
- **Pros:** Portable. No fleet config.
- **Cons:** Can't remove OS-level jitter.

## Questions to answer before deciding

- For each knob: what did it change in the tuning log, and what does it cost (power draw, throughput, memory)?
- Which changes are safe for a whole fleet, and which only for dedicated latency hosts?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

tuning-log rows; perf/bpftrace evidence
