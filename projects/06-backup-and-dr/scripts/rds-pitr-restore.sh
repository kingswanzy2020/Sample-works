#!/usr/bin/env bash
# Tier 2 (cloud): restore the project 01 RDS instance to a point in time, as a NEW instance.
# Usage: scripts/rds-pitr-restore.sh sample-staging-postgres 2026-01-01T12:00:00Z
# Then measure: how long until it's "available"? How do you point the app at it (DNS? config?)
set -euo pipefail
source_id="${1:?source DB identifier}"
restore_time="${2:?UTC restore time, e.g. 2026-01-01T12:00:00Z}"
target_id="${source_id}-pitr-$(date -u +%Y%m%d%H%M)"

start=$(date +%s)
aws rds restore-db-instance-to-point-in-time \
  --source-db-instance-identifier "$source_id" \
  --target-db-instance-identifier "$target_id" \
  --restore-time "$restore_time" \
  --no-publicly-accessible >/dev/null
aws rds wait db-instance-available --db-instance-identifier "$target_id"
echo "restored $target_id in $(( $(date +%s) - start ))s"
echo "Remember to delete it: aws rds delete-db-instance --db-instance-identifier $target_id --skip-final-snapshot"
