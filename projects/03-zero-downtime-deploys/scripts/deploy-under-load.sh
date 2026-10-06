#!/usr/bin/env bash
# Roll out a new image while k6 generates load, then report errors seen during the rollout.
# Usage: scripts/deploy-under-load.sh sample-service:v2
set -euo pipefail
image="${1:?usage: deploy-under-load.sh <image>}"

k6 run --quiet --summary-export=load-summary.json -e DURATION=3m load/during-deploy.js &
k6_pid=$!
sleep 20 # warm-up so the baseline is visible in the results

kubectl -n zdd set image deployment/app app="$image"
kubectl -n zdd rollout status deployment/app --timeout=5m

wait "$k6_pid" || echo "k6 thresholds FAILED: requests failed during the rollout"
python3 -c "import json;m=json.load(open('load-summary.json'))['metrics'];print('failed rate:',m['http_req_failed']['value']);print('p99 ms:',m['http_req_duration'].get('p(99)'))"
