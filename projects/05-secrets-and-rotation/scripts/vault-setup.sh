#!/bin/sh
# Configure dynamic Postgres credentials. Runs inside the vault-setup container.
set -eu

until vault status >/dev/null 2>&1; do sleep 1; done

vault secrets enable database 2>/dev/null || true

# Vault connects as a privileged user to create short-lived roles.
# DECISION (ADR-0002): in real life this is a dedicated `vault` DB user, and its password
# is rotated by Vault itself (`vault write -f database/rotate-root/app`).
vault write database/config/app \
  plugin_name=postgresql-database-plugin \
  allowed_roles=app \
  connection_url='postgresql://{{username}}:{{password}}@db:5432/app?sslmode=disable' \
  username=app password=app

# Short TTLs on purpose, so you can watch rotation in minutes. The agent RENEWS the lease
# (same user, later VALID UNTIL) until max_ttl, then fetches a brand-new user.
vault write database/roles/app \
  db_name=app \
  default_ttl=1m max_ttl=3m \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
GRANT SELECT, INSERT ON items TO \"{{name}}\"; GRANT USAGE ON SEQUENCE items_id_seq TO \"{{name}}\";"

# Least-privilege policy for the app: it can only read its own DB creds.
vault policy write app - <<'POLICY'
path "database/creds/app" { capabilities = ["read"] }
POLICY

# Lab shortcut: a token for the agent, written to a shared volume.
# Production: Kubernetes / AWS IAM auth so no token is ever stored (ADR-0002).
vault token create -policy=app -period=1h -field=token > /token/agent-token
# The agent runs as the image's `vault` user; let it write the rendered secret.
chown vault:vault /token/agent-token /secrets
echo "vault configured"
