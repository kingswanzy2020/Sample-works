# What I'd do differently at a different scale

## Now: 1 service, local cluster
- Was canary worth it at this traffic level? What was the cheapest setting that gave zero errors?

## 10×: ~10 services, real traffic
- Argo Rollouts / Flagger with an ingress or service mesh for precise traffic weights.
- A migration linter in CI (e.g. `squawk` for Postgres) to block locking or breaking DDL.
- Feature flags so code deploy ≠ feature release.

## 100×: many teams, many deploys per day
- Progressive delivery by cell/region, with automated analysis per cell.
- An online schema change tool for huge tables (pg_repack / gh-ost style approaches).
- Deploy freezes and change management driven by error budgets (project 04).

## The one-paragraph version for interviews

>
