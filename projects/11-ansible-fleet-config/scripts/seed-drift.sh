#!/usr/bin/env bash
# Simulate months of manual changes: randomly mutate some lab servers so they are no longer "identical".
# Your job (break-it experiment 1) is to DETECT this with Ansible, not to read this script.
set -euo pipefail
cd "$(dirname "$0")/../lab"
nodes=(trading-01 trading-02 kafka-01 kafka-02 monitoring-01 monitoring-02)
changes=(
  "echo 'net.core.somaxconn = 512' > /etc/sysctl.d/99-hotfix.conf"
  "sed -i 's/^#\?MaxAuthTries.*/MaxAuthTries 20/' /etc/ssh/sshd_config"
  "useradd -m tempadmin"
  "echo '* * * * * root /bin/true' > /etc/cron.d/someones-job"
  "rm -f /etc/motd"
  "chmod 777 /opt"
  "echo 'export TZ=America/New_York' > /etc/profile.d/tz.sh"
)
for n in "${nodes[@]}"; do
  if (( RANDOM % 2 )); then
    c="${changes[RANDOM % ${#changes[@]}]}"
    docker compose exec -T "$n" sh -c "$c" >/dev/null 2>&1 || true
  fi
done
echo "Drift seeded on a random subset of servers. Now find it."
