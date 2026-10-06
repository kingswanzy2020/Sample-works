# What I'd do differently at a different scale

## Now: one lab host
- Which change gave the biggest p99.9 improvement per unit of effort? Which were noise?

## 10×: a rack of latency hosts
- Tuning as code (project 11) with a post-apply latency check that fails the rollout if p99.9 regresses.
- Continuous latency monitoring per host, so drift (BIOS update, kernel update) is caught.

## 100×: firm-wide
- Hardware choices (NICs with kernel bypass, CPU SKUs) become the biggest lever. Software tuning hits a floor.
- Separate "latency-critical" and "general" host classes, with different operating models and change control.

## The one-paragraph version for interviews

>
