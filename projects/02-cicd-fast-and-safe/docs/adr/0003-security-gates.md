# ADR-0003: Security gates: block vs warn

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Trivy finds dozens of CVEs in a typical base image. If every finding blocks, people learn to bypass the gate.
If none block, the scan is decoration.

## Options considered

### Option 1: Block on any HIGH/CRITICAL
- **Pros:** Strict.
- **Cons:** Many have no fix yet, so CI is red for things you cannot act on. Teams add blanket ignores.

### Option 2: Block on CRITICAL **with a fix available**, report everything else (starter default)
- **Pros:** Every blocking finding is actionable.
- **Cons:** HIGH vulns with fixes can sit for months unless someone reads the reports.

### Option 3: Warn only, track via dashboards and SLAs (e.g. criticals fixed in 7 days)
- **Pros:** Never blocks delivery.
- **Cons:** Needs an owner and follow-through; easy to ignore.

## Questions to answer before deciding

- Who can add an exception (`.trivyignore`), and does it expire?
- Base image choice: `python:3.12-slim` vs distroless vs Chainguard. How many CVEs does each bring? (Measure it.)
- Sign images (cosign) and verify at deploy, or only sign?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

break-it experiment 2 (introduce a known CVE); CVE counts per base image
