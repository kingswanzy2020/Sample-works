#!/usr/bin/env bash
# Send a saved Alertmanager payload to the triage service (no landscape needed).
# Usage: scripts/replay.sh [tests/fixtures/kafka-storm.json]
set -euo pipefail
cd "$(dirname "$0")/.."
curl -fsS -XPOST localhost:8080/alerts -H 'content-type: application/json' -d @"${1:-tests/fixtures/kafka-storm.json}"
echo
