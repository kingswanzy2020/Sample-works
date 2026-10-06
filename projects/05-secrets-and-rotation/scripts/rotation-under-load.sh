#!/usr/bin/env bash
# Hit the app continuously for N seconds and count failures, while Vault renews (1m lease) and rotates (3m max TTL) creds.
# Usage: scripts/rotation-under-load.sh 300
set -uo pipefail
duration="${1:-300}"
end=$((SECONDS + duration))
ok=0; fail=0
while (( SECONDS < end )); do
  if curl -fsS -o /dev/null --max-time 2 localhost:8000/items; then ok=$((ok+1)); else fail=$((fail+1)); echo "$(date +%T) failure"; fi
  sleep 0.2
done
echo "ok=$ok fail=$fail"
echo "Vault-created DB roles that still exist (expired leases are revoked by Vault):"
docker compose exec -T db psql -U app -d app -c "SELECT rolname, rolvaliduntil FROM pg_roles WHERE rolname LIKE 'v-%' ORDER BY rolvaliduntil;"
