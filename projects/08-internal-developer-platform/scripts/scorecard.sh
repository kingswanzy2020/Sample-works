#!/usr/bin/env bash
# Paved-road scorecard: how far is a service repo from the golden path?
# Usage: scripts/scorecard.sh /path/to/service-repo
set -uo pipefail
repo="${1:?usage: scorecard.sh <repo-dir>}"
score=0; total=0

check() {
  local name="$1"; shift
  total=$((total + 1))
  if "$@" >/dev/null 2>&1; then score=$((score + 1)); echo "  [x] $name"; else echo "  [ ] $name"; fi
}

echo "Scorecard for $repo"
check "catalog-info.yaml (has an owner)"         grep -q "owner:" "$repo/catalog-info.yaml"
check "Dockerfile runs as non-root"              grep -qE "^USER [^r]" "$repo/Dockerfile"
check "uses org reusable CI workflow"            grep -rq "uses: .*/platform/.github/workflows/" "$repo/.github/workflows"
check "readiness probe defined"                  grep -rq "readinessProbe" "$repo/k8s"
check "resource requests defined"                grep -rq "requests:" "$repo/k8s"
check "PodDisruptionBudget defined"              grep -rq "kind: PodDisruptionBudget" "$repo/k8s"
check "exposes /metrics"                         grep -rq "/metrics" "$repo/src"
check "has at least one ADR"                     sh -c "ls '$repo'/docs/adr/0*.md"
check "no :latest image tags"                    sh -c "[ -d '$repo/k8s' ] && ! grep -rq ':latest' '$repo/k8s'"

echo "Score: $score/$total"
