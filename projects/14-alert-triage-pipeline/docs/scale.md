# What I'd do differently at a different scale

## Now: 8 simulated services
- Which enrichment field saved the most time in game days?

## 10×: ~100 services
- Correlation state in a shared store (Redis/DB) so triage can run more than one replica.
- Dependency map generated from tracing (project 04) instead of hand-maintained.
- Integration with a paging product for escalation and mobile.

## 100×: firm-wide
- Event pipeline (Kafka, from project 09) in front of triage to absorb storms.
- Correlation tuned per domain; ML-assisted grouping only with human-visible reasoning.

## The one-paragraph version for interviews

>
