# Project 05: Secrets management and credential rotation

> **Problem:** Secrets live in `.env` files and CI variables. They never rotate.
> An ex-employee still knows the production database password.

**Need help while building?** See [`docs/build-plan.md`](docs/build-plan.md): tasks with a goal and a "done when" check, hints hidden in levels (nudge → concept → docs), and a diagnosis table. It never gives you the full solution.

## Decisions this project proves you can make

1. **Where secrets live:** a secrets store (Vault / cloud manager) vs encrypted in git (SOPS).
2. **Static vs dynamic credentials:** long-lived passwords or short-lived leases.
3. **How workloads authenticate to the secrets store:** the "secret zero" problem.
4. **How the app picks up a rotated secret:** restart, re-read, or a sidecar.
5. **CI to cloud without long-lived keys:** OIDC federation and how tightly to scope it.
6. **What happens when the secrets store is down.**

## Success criteria

- [ ] No long-lived cloud keys in GitHub. CI uses OIDC (`terraform/github-oidc`).
- [ ] The app's DB credentials are leased for 1 minute, replaced with a new DB user at least every 3 minutes, and rotation causes **0 failed requests** (`scripts/rotation-under-load.sh`).
- [ ] A secret committed by mistake is blocked by pre-commit **and** CI.
- [ ] A written answer to "Vault is down: can we still serve traffic? Can we deploy?"
- [ ] An offboarding runbook: what to rotate when someone leaves, and how long it takes.

## Prerequisites and cost

- Free and local: Docker Compose (Vault dev mode, Postgres).
- Optional AWS pieces (OIDC roles, External Secrets) build on project 01 and cost almost nothing.

## Starter layout

```
docker-compose.yml          # Postgres + Vault (dev) + Vault Agent + app reading DATABASE_URL_FILE
scripts/vault-setup.sh      # database secrets engine, dynamic creds (1m lease, 3m max), least-privilege policy
vault/agent.hcl             # renders the DB URL to a shared file, re-renders before expiry
scripts/rotation-under-load.sh
terraform/github-oidc/      # GitHub → AWS OIDC, separate plan/apply roles scoped by `sub`
k8s/external-secrets/       # sync RDS-managed secret (project 01) into Kubernetes
sops/                       # SOPS + age, for the "secrets in git" option
.gitleaks.toml  .pre-commit-config.yaml  .github/workflows/secret-scan.yml
```

## Run

```bash
APP_DIR=../../app docker compose up --build -d     # in an extracted repo: docker compose up --build -d
docker compose exec app cat /secrets/database_url  # note the generated username
./scripts/rotation-under-load.sh 300               # 5 minutes = at least 2 rotations
```

## Milestones

### Build
- [ ] **Start with the "before":** a static password in `.env`. Write down every place it ends up (shell history, CI logs, `docker inspect`, image layers?).
- [ ] Bring up the Vault stack. Watch `rolvaliduntil` move forward on each renewal, then the username change at `max_ttl`. Explain renewal vs rotation in ADR-0002.
- [ ] Apply `terraform/github-oidc` and switch project 01/02 workflows to OIDC.

### Test
- [ ] Rotation under load: record failures over 10 minutes.
- [ ] `gitleaks` catches a fake AWS key in a commit, and in an *old* commit (history scan).

### Break
- [ ] [`docs/break-it.md`](docs/break-it.md): Vault down, lease revoked, leaked secret, over-broad OIDC trust.

### Decide
- [ ] ADR-0001 to ADR-0005.

### Improve
- [ ] Replace the lab token with a real auth method (Kubernetes or AWS IAM auth). No token on disk.
- [ ] Let Vault rotate its own root DB credential (`database/rotate-root/app`).
- [ ] Narrow the `apply` role from `PowerUserAccess` to least privilege. Use IAM Access Analyzer to generate the policy from real usage.

### Document
- [ ] Diagram of the trust chain: GitHub → AWS role → Secrets Manager / Vault → DB.
- [ ] `docs/offboarding-runbook.md`.

## ADRs

| # | Decision | Status |
|---|----------|--------|
| [0001](docs/adr/0001-where-secrets-live.md) | Secrets store vs encrypted in git | Proposed |
| [0002](docs/adr/0002-static-vs-dynamic-credentials.md) | Static passwords vs dynamic leases | Proposed |
| [0003](docs/adr/0003-ci-to-cloud-auth.md) | OIDC federation and trust scoping | Proposed |
| [0004](docs/adr/0004-delivering-secrets-to-the-app.md) | Env var vs file vs SDK; rotation pickup | Proposed |
| [0005](docs/adr/0005-secrets-store-availability.md) | Behaviour when the store is down | Proposed |

## Interview story

> "The DB password hadn't changed in ___ and was in ___ places. I moved to ___ with ___-minute
> credentials. Rotation initially caused ___ errors because ___; I fixed it by ___. When Vault
> was down, ___ — so I decided ___."
