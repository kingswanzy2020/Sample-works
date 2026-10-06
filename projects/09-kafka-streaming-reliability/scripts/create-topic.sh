#!/usr/bin/env bash
# Create the price-ticks topic with the durability settings from your ADR-0001.
# Usage: PARTITIONS=6 RF=3 MIN_ISR=2 scripts/create-topic.sh
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose exec -T kafka1 /opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka1:9092 \
  --create --if-not-exists --topic "${TOPIC:-price-ticks}" \
  --partitions "${PARTITIONS:-6}" --replication-factor "${RF:-3}" \
  --config min.insync.replicas="${MIN_ISR:-2}"
docker compose exec -T kafka1 /opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka1:9092 \
  --describe --topic "${TOPIC:-price-ticks}"
