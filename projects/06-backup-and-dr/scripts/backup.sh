#!/usr/bin/env bash
# Logical backup: pg_dump (custom format) → object storage.
# DECISION (ADR-0001): this is the "Tier 1" strategy. RPO = time since the last run.
set -euo pipefail
cd "$(dirname "$0")/.."

# Object storage can take ~30s to accept requests after start.
for _ in $(seq 1 30); do docker compose run --rm awscli s3 ls >/dev/null 2>&1 && break; sleep 2; done

ts="$(date -u +%Y%m%dT%H%M%SZ)"
file="app-$ts.dump"
mkdir -p backups

docker compose run --rm awscli s3 mb s3://backups >/dev/null 2>&1 || true

start=$(date +%s)
docker compose exec -T db pg_dump -U app -d app --format=custom > "backups/$file"
docker compose run --rm awscli s3 cp "/backups/$file" "s3://backups/app/$file" --only-show-errors
sha256sum "backups/$file" | awk '{print $1}' > "backups/$file.sha256"
docker compose run --rm awscli s3 cp "/backups/$file.sha256" "s3://backups/app/$file.sha256" --only-show-errors
rm -f "backups/$file" "backups/$file.sha256" # the local copy is not the backup

echo "backup ok: s3://backups/app/$file ($(( $(date +%s) - start ))s)"
