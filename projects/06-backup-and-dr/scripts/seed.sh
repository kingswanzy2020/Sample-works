#!/usr/bin/env bash
# Write N items through the API, so backups have something to lose.
set -euo pipefail
n="${1:-100}"

# Wait for the app to be ready (containers can be "up" before the server listens).
for _ in $(seq 1 60); do curl -fsS -o /dev/null localhost:8000/readyz && break; sleep 1; done
for i in $(seq 1 "$n"); do
  curl -fsS -o /dev/null -X POST localhost:8000/items -H 'content-type: application/json' -d "{\"name\":\"seed-$i\"}"
done
echo "seeded $n items"
