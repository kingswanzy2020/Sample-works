# Project 06: Backup and disaster recovery that's actually tested

> **Problem:** "We have backups." Nobody has ever restored one. Nobody knows how long
> it would take, or how much data would be lost.

**Need help while building?** See [`docs/build-plan.md`](docs/build-plan.md): tasks with a goal and a "done when" check, hints hidden in levels (nudge → concept → docs), and a diagnosis table. It never gives you the full solution.

## Decisions this project proves you can make

1. **RPO and RTO:** how much data loss and downtime are acceptable, per data store, and who agreed to it.
2. **Backup strategy to meet them:** logical dumps, snapshots, point-in-time recovery, replicas.
3. **Protecting backups from yourself:** separate account, versioning, object lock, a writer that can't delete.
4. **Testing:** restore drills as an automated, scheduled job with a pass/fail result.
5. **Scope:** what else needs backing up (Terraform state, secrets, config).

## Success criteria

- [ ] An inventory of every data store with an agreed RPO/RTO (`docs/rpo-rto.md`).
- [ ] A weekly automated restore drill that **fails CI** if the restore is unusable or slower than the RTO target.
- [ ] **Measured** RTO and RPO for each tier, not estimated ones.
- [ ] Backups survive deletion by an admin credential (object lock + writer without delete).
- [ ] A full "region is gone" game day, written up as a postmortem.

## Prerequisites and cost

- Local: Docker Compose (Postgres + SeaweedFS as an S3-compatible store).
- Cloud (optional): RDS from project 01 for point-in-time recovery; the backup bucket costs pennies at lab volumes.

## Starter layout

```
docker-compose.yml               # db, app, S3-compatible store, throwaway restore-db
scripts/seed.sh                  # write data through the API
scripts/backup.sh                # pg_dump → S3 with checksum
scripts/restore-drill.sh         # fresh DB ← latest backup, validate, time it, write a report
scripts/rds-pitr-restore.sh      # cloud tier: RDS point-in-time restore to a new instance
.github/workflows/restore-drill.yml   # weekly drill, report uploaded as an artifact
terraform/backup-bucket/         # versioned, object-locked, cross-region bucket; writer can't delete
docs/rpo-rto.md                  # the inventory and targets
docs/drills/                     # drill reports land here
```

## Run

```bash
APP_DIR=../../app docker compose up -d --build --wait db s3 app
scripts/seed.sh 200 && scripts/backup.sh && scripts/seed.sh 25
scripts/restore-drill.sh          # reports measured RTO and rows lost (should be 25)
```

## Milestones

### Build
- [ ] Fill in `docs/rpo-rto.md` **first**. Ask: what does an hour of downtime cost? A day of lost data?
- [ ] Run the local backup + drill. Read the report.

### Test
- [ ] Turn on the scheduled drill workflow. Make it fail on purpose once (point at an empty bucket).
- [ ] Cloud tier: RDS PITR restore. Record the time to "available" **and** the time until the app actually uses it.

### Break
- [ ] [`docs/break-it.md`](docs/break-it.md): delete the database, corrupt a backup, ransomware the bucket, lose the region.

### Decide
- [ ] ADR-0001 to ADR-0004.

### Improve
- [ ] Add WAL archiving (pgBackRest or WAL-G) locally to get PITR and an RPO of minutes instead of hours. Re-measure.
- [ ] Back up project 01's Terraform state and project 05's secrets. Can you rebuild everything with only the backup account?
- [ ] Alert when the newest backup is older than RPO (a freshness check), not just when a backup job fails.

### Document
- [ ] A table of documented vs measured RTO/RPO, plus the game day postmortem.

## How this project connects

| Direction | Project | What flows |
|-----------|---------|------------|
| Uses | `app/` | The data being protected |
| Uses | [01 IaC](../01-iac-multi-env/) | RDS PITR; the region-loss game day rebuilds 01's infrastructure |
| Uses | [05 Secrets](../05-secrets-and-rotation/) | Secrets must be part of what you can recover |
| Feeds | [12 Incidents](../12-incident-response/) | Restore drills and the region game day as incident-response practice |
| Feeds | [16 Reliability reporting](../16-reliability-reporting/) | Measured RTO/RPO are reliability facts worth reporting |
| Related, not repeated | [09 Kafka](../09-kafka-streaming-reliability/) | Kafka replication and retention are **not** backups. That's a point to make in both projects |

**Not in this project:** streaming durability (09), incident process (12).

## ADRs

| # | Decision | Status |
|---|----------|--------|
| [0001](docs/adr/0001-backup-strategy.md) | Dumps vs snapshots vs PITR vs replicas | Proposed |
| [0002](docs/adr/0002-dr-topology.md) | Backup-restore vs pilot light vs warm standby | Proposed |
| [0003](docs/adr/0003-restore-testing.md) | How and how often restores are tested | Proposed |
| [0004](docs/adr/0004-backup-isolation.md) | Protecting backups from deletion and compromise | Proposed |

## Interview story

> "Our documented RTO was ___. The first real drill took ___ because ___. I changed ___ and
> got it to ___. Backups now live in ___ with ___ so even a compromised admin can't delete them.
> For a bigger business I'd move to ___ because an hour down costs ___."
