# ADR-0001: Lab environment and measurement method

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Latency results are only as good as the measurement. Wrong method = confident wrong answers.

## Options considered (environment)

### Option 1: Your own Linux machine / bare-metal cloud instance
- **Pros:** Real hardware, full control (BIOS, kernel cmdline).
- **Cons:** Availability and cost (bare-metal instances are expensive).

### Option 2: Cloud VM with dedicated cores
- **Pros:** Easy, cheap per hour.
- **Cons:** Hypervisor jitter you can't remove. Some knobs (C-states, frequency) are invisible.

### Option 3: Local VM / Docker
- **Pros:** Free.
- **Cons:** Most noise comes from the host OS. Fine for learning tools, weak for conclusions.

## Options considered (method)

- **Closed loop** (send next request after reply): simple, but hides stalls (coordinated omission).
- **Open loop at a fixed rate** (starter's `sockperf under-load`): stalls show up as latency, which is honest.
- **Which percentiles:** p50 for typical, p99/p99.9 for the tail, max for the worst. How many samples does p99.9 need to mean anything?

## Questions to answer before deciding

- How many observations does each run actually record? Is that enough for p99.9? (Look at `summary.txt`.)
- How much do two identical runs differ? That spread is your noise floor. Smaller differences aren't real.

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

results/ baseline runs
