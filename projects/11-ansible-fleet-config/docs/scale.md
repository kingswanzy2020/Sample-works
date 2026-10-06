# What I'd do differently at a different scale

## Now: 6 lab servers
- What did idempotence and drift detection actually catch?

## 10×: ~100 servers, several roles
- Roles in their own repo, versioned, with Molecule in CI.
- AWX/Semaphore (or CI) as the only place changes run from; nightly check-mode drift report.
- Dynamic inventory with tag validation.

## 100×: thousands of servers, multiple sites
- Pull-based or agent-based for convergence; push only for urgent changes.
- Immutable images wherever hosts are replaceable; config management only for the remainder.
- Change windows tied to market hours, and automated rollback on health regression.

## The one-paragraph version for interviews

>
