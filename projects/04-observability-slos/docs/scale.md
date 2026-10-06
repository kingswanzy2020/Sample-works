# What I'd do differently at a different scale

## Now: 1 service, local stack
- Which signal actually found the problem fastest? Which component would you drop?

## 10×: ~20 services
- OpenTelemetry Collector as the single pipeline (agents per node, gateway tier) with tail sampling.
- SLOs per user journey (checkout, login), not per service.
- kube-prometheus-stack + Thanos/Mimir for long-term SLO history.

## 100×: hundreds of services, many teams
- Cardinality limits enforced per team, with chargeback.
- Buy vs build is driven by people cost: a vendor is often cheaper than an observability team, until it isn't.
- Error budgets in planning: teams that blow the budget spend the next sprint on reliability.

## The one-paragraph version for interviews

>
