#!/usr/bin/env bash
# Show consumer lag per partition for a group.
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose exec -T kafka1 /opt/kafka/bin/kafka-consumer-groups.sh --bootstrap-server kafka1:9092 \
  --describe --group "${GROUP_ID:-order-router}"
