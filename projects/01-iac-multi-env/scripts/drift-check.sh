#!/usr/bin/env bash
# Exit codes from `terraform plan -detailed-exitcode`:
#   0 = no changes, 1 = error, 2 = drift (live infra != code)
set -uo pipefail
env_dir="${1:?usage: drift-check.sh envs/<env>}"

cd "$env_dir"
terraform init -input=false -no-color >/dev/null
terraform plan -input=false -no-color -lock=false -detailed-exitcode -out=drift.tfplan > plan.txt 2>&1
code=$?

case $code in
  0) echo "No drift in $env_dir" ;;
  2) echo "DRIFT DETECTED in $env_dir"; terraform show -no-color drift.tfplan | grep -E '^\s+[~+-/]' | head -50 ;;
  *) echo "terraform plan failed in $env_dir"; tail -30 plan.txt ;;
esac
exit $code
