#!/usr/bin/env bash
# Measure request/response latency under a FIXED send rate (open loop) with sockperf, and save results.
# A fixed rate matters: closed-loop tools slow down when the server stalls, hiding the stall
# ("coordinated omission"). See ADR-0001.
#
# Usage: LABEL=pinned SERVER_CPUS=2 CLIENT_CPUS=3 MPS=20000 DURATION=30 scripts/measure.sh
set -euo pipefail
LABEL="${LABEL:-run}"; MPS="${MPS:-20000}"; DURATION="${DURATION:-30}"; MSG_SIZE="${MSG_SIZE:-64}"
SERVER_CPUS="${SERVER_CPUS:-}"; CLIENT_CPUS="${CLIENT_CPUS:-}"; PORT="${PORT:-11111}"
dir="$(dirname "$0")/../results/$(date -u +%Y%m%dT%H%M%SZ)-$LABEL"
mkdir -p "$dir"

pin() { if [[ -n "$1" ]]; then echo "taskset -c $1"; fi; }

# shellcheck disable=SC2046
$(pin "$SERVER_CPUS") sockperf server --tcp -p "$PORT" > "$dir/server.log" 2>&1 &
server=$!
trap 'kill $server 2>/dev/null || true' EXIT
sleep 1

# shellcheck disable=SC2046
$(pin "$CLIENT_CPUS") sockperf under-load --tcp -i 127.0.0.1 -p "$PORT" --mps="$MPS" -t "$DURATION" \
  -m "$MSG_SIZE" --full-rtt > "$dir/client.log" 2>&1

grep -E "Total|Summary: Latency|percentile|MIN|MAX|avg-latency|dropped|duplicated|out-of-order" "$dir/client.log" \
  | sed -e 's/^sockperf: //' -e 's/\x1b\[[0-9;]*m//g' | tee "$dir/summary.txt"
echo "saved to $dir (label=$LABEL mps=$MPS server_cpus=${SERVER_CPUS:-any} client_cpus=${CLIENT_CPUS:-any})"
