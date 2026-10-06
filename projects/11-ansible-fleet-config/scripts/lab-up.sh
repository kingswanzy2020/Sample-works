#!/usr/bin/env bash
# Create the lab SSH key (once) and start the six lab servers.
set -euo pipefail
cd "$(dirname "$0")/../lab"
mkdir -p .ssh
[[ -f .ssh/lab_key ]] || ssh-keygen -t ed25519 -N "" -C "ansible-lab" -f .ssh/lab_key >/dev/null
chmod 600 .ssh/lab_key
docker compose up -d --build
echo "Lab up. Try: ansible all -m ping"
