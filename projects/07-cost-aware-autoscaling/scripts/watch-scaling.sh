#!/usr/bin/env bash
# Record replicas, ready pods and total CPU requested every 5s to a CSV, for the cost graph.
# Usage: scripts/watch-scaling.sh scaling.csv
set -euo pipefail
out="${1:-scaling.csv}"
echo "time,desired,ready,cpu_requested_millicores" > "$out"
while true; do
  desired=$(kubectl -n scale get deploy app -o jsonpath='{.spec.replicas}')
  ready=$(kubectl -n scale get deploy app -o jsonpath='{.status.readyReplicas}')
  cpu=$(kubectl -n scale get pods -l app=sample -o jsonpath='{range .items[*]}{.spec.containers[0].resources.requests.cpu}{"\n"}{end}' \
        | sed 's/m$//' | awk '{s+=$1} END {print s+0}')
  echo "$(date +%T),$desired,${ready:-0},$cpu" | tee -a "$out"
  sleep 5
done
