#!/usr/bin/env bash
# Restore the latest backup into a FRESH database, validate it, and time everything.
# Writes a report to docs/drills/. Exit code != 0 if validation fails or RTO target is missed.
#
# Usage: RTO_TARGET_SECONDS=900 scripts/restore-drill.sh
set -euo pipefail
cd "$(dirname "$0")/.."
RTO_TARGET_SECONDS="${RTO_TARGET_SECONDS:-900}"
mkdir -p backups docs/drills

# Object storage can take ~30s to accept requests after start.
for _ in $(seq 1 30); do docker compose run --rm awscli s3 ls >/dev/null 2>&1 && break; sleep 2; done

t0=$(date +%s)

# 1. Find the latest backup.
latest="$(docker compose run --rm awscli s3 ls s3://backups/app/ | awk '{print $4}' | grep '\.dump$' | sort | tail -1)"
[[ -n "$latest" ]] || { echo "no backups found"; exit 1; }
echo "latest backup: $latest"

# 2. Download and verify integrity.
docker compose run --rm awscli s3 cp "s3://backups/app/$latest" "/backups/$latest" --only-show-errors
docker compose run --rm awscli s3 cp "s3://backups/app/$latest.sha256" "/backups/$latest.sha256" --only-show-errors
echo "$(cat "backups/$latest.sha256")  backups/$latest" | sha256sum -c -
t_download=$(date +%s)

# 3. Restore into a fresh instance.
docker compose --profile drill rm -sf restore-db >/dev/null 2>&1 || true
docker compose --profile drill up -d --wait restore-db
docker compose exec -T restore-db pg_restore -U app -d app --no-owner --exit-on-error < "backups/$latest"
t_restore=$(date +%s)

# 4. Validate: the restore must be usable, not just "exit 0".
restored_rows=$(docker compose exec -T restore-db psql -U app -d app -tAc "SELECT count(*) FROM items")
restored_last=$(docker compose exec -T restore-db psql -U app -d app -tAc "SELECT coalesce(max(created_at)::text,'none') FROM items")
primary_rows=$(docker compose exec -T db psql -U app -d app -tAc "SELECT count(*) FROM items" 2>/dev/null || echo "unavailable")
primary_last=$(docker compose exec -T db psql -U app -d app -tAc "SELECT coalesce(max(created_at)::text,'none') FROM items" 2>/dev/null || echo "unavailable")
t_end=$(date +%s)

rto=$(( t_end - t0 ))
status=PASS
[[ "$restored_rows" =~ ^[0-9]+$ && "$restored_rows" -gt 0 ]] || status=FAIL
(( rto <= RTO_TARGET_SECONDS )) || status=FAIL

report="docs/drills/$(date -u +%Y-%m-%dT%H%M%SZ)-restore-drill.md"
cat > "$report" <<REPORT
# Restore drill: $status

| Measure | Value |
|---------|-------|
| Backup restored | \`$latest\` |
| Download + verify | $(( t_download - t0 ))s |
| Restore | $(( t_restore - t_download ))s |
| Validate | $(( t_end - t_restore ))s |
| **Measured RTO** | **${rto}s** (target ${RTO_TARGET_SECONDS}s) |
| Rows restored / in primary | $restored_rows / $primary_rows |
| Newest restored row / newest in primary | $restored_last / $primary_last |
| **Data lost (rows)** | $( [[ "$primary_rows" =~ ^[0-9]+$ ]] && echo $(( primary_rows - restored_rows )) || echo "primary unavailable" ) |

Measured RPO ≈ time between the newest restored row and the newest primary row.
REPORT

cat "$report"
docker compose --profile drill rm -sf restore-db >/dev/null
rm -f "backups/$latest" "backups/$latest.sha256"
[[ "$status" == PASS ]]
