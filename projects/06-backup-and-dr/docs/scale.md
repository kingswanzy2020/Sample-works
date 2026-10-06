# What I'd do differently at a different scale

## Now: one small DB
- Daily dumps + weekly drill was enough because ___. Measured RTO: ___.

## 10×: larger DB (100s of GB), revenue depends on it
- PITR (pgBackRest/WAL-G or managed PITR); restore time dominated by data size, so test it at real size.
- Pilot-light DR region with replicated backups; DR runbook rehearsed quarterly.

## 100×: many data stores, regulatory requirements
- Central backup policy (AWS Backup / Velero for k8s) with compliance-mode locks and audit reports.
- Tiered RPO/RTO per service, owned by service teams and reviewed yearly.
- Chaos and game days on the calendar, not ad hoc.

## The one-paragraph version for interviews

>
