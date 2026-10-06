# ADR-0003: When not to automate

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Automating a symptom can hide a problem that should be fixed. A cleanup script that runs every hour is a disk-full bug with a timer.

## Options considered

### Option 1: Automate the manual task as-is
- **Pros:** Immediate relief.
- **Cons:** The cause stays; the automation becomes permanent.

### Option 2: Fix the cause (config, code, alert), and automate only if the cause can't be fixed
- **Pros:** Removes the work entirely.
- **Cons:** Needs another team or project; slower.

### Option 3: Automate now, with a ticket and expiry date to fix the cause
- **Pros:** Relief now, pressure to fix later.
- **Cons:** "Temporary" automations tend to stay.

## Questions to answer before deciding

- For each top inventory item: what's the root cause, and who owns it?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


