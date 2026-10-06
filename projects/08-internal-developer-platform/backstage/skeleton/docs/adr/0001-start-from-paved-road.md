# ADR-0001: Start from the paved-road template

- **Status:** Accepted
- **Date:** (creation date)
- **Deciders:** ${{ values.owner }}

## Context

New services need CI, security scanning, deploy manifests, probes and metrics. Building these per service
takes days and produces inconsistent results.

## Decision

Start from the platform's `python-service` template and stay on the reusable CI workflow.

## Consequences

- **What this gives us:** deployable on day one; platform improvements arrive automatically.
- **What we give up:** some flexibility. Deviations need their own ADR (copy `template.md`).
- **Revisit when:** the service has needs the template can't meet (e.g. GPU, non-HTTP workloads).
