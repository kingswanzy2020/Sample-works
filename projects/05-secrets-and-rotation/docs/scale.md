# What I'd do differently at a different scale

## Now: 1 app, 1 DB
- Was Vault justified, or would RDS-managed secrets + IAM auth have covered it?

## 10×: ~10 services, several databases
- Vault HA (integrated raft) or a managed equivalent; Kubernetes auth, per-service policies.
- Secrets inventory: owner, rotation period, last rotated, for every secret.
- Automated offboarding: identity provider deprovisioning revokes everything.

## 100×: org-wide
- Workload identity everywhere (SPIFFE/SPIRE, cloud workload identity) so most "secrets" disappear.
- Policy as code for secret access, with periodic access reviews.
- Break-glass procedures with tamper-evident audit.

## The one-paragraph version for interviews

>
