# ADR-0003: Metrics pipeline: Prometheus pull vs OpenTelemetry push

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

The app exposes `/metrics` (Prometheus client) and sends traces via OTLP. Metrics could also go via OTLP.

## Options considered

### Option 1: Prometheus pull for metrics, OTLP for traces (starter default)
- **Pros:** `up` tells you when a target dies. Mature ecosystem.
- **Cons:** Two pipelines. Pull needs service discovery and network reachability.

### Option 2: Everything via OTLP to an OpenTelemetry Collector
- **Pros:** One protocol, vendor-neutral, central processing (redaction, sampling, routing).
- **Cons:** The collector becomes critical infrastructure. Absence of data is harder to alert on.

## Questions to answer before deciding

- How do you detect a service that stopped *sending* metrics?
- If you switch vendor next year, what has to change?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


