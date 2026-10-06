#!/usr/bin/env bash
# Bring up the idle colour, wait until ready, flip the Service, keep the old colour for rollback.
# Usage: scripts/blue-green-switch.sh green sample-service:v2
set -euo pipefail
target="${1:?usage: blue-green-switch.sh <blue|green> <image>}"
image="${2:?image required}"
ns=zdd

kubectl -n $ns set image "deployment/app-$target" app="$image"
kubectl -n $ns scale "deployment/app-$target" --replicas=4
kubectl -n $ns rollout status "deployment/app-$target" --timeout=5m

# Smoke test the new colour directly, before it gets any user traffic.
pod_ip="$(kubectl -n $ns get pod -l "track=$target" -o jsonpath='{.items[0].status.podIP}')"
kubectl -n $ns run "smoke-$RANDOM" --rm -i --restart=Never --image=curlimages/curl -- \
  curl -fsS --max-time 5 "http://$pod_ip:8000/readyz"

kubectl -n $ns patch service app -p "{\"spec\":{\"selector\":{\"app\":\"sample\",\"track\":\"$target\"}}}"
echo "Switched traffic to $target. Old colour still running for instant rollback."
echo "Rollback: kubectl -n $ns patch service app -p '{\"spec\":{\"selector\":{\"app\":\"sample\",\"track\":\"<old>\"}}}'"
