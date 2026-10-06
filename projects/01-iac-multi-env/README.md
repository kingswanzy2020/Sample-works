# Project 01: Multi-environment Infrastructure as Code with drift detection

> **Problem:** Staging and prod have drifted apart. Nobody knows what is actually
> deployed, and someone changed a setting in the console last week.

This is the foundation for every later project. The network, database and state
layout you build here are what projects 02 to 08 deploy onto.

**Need help while building?** See [`docs/build-plan.md`](docs/build-plan.md): tasks with a goal and a "done when" check, hints hidden in levels (nudge → concept → docs), and a diagnosis table. It never gives you the full solution.

## Decisions this project proves you can make

1. **State layout and blast radius:** one state file, one per environment, or one per component?
2. **Environment separation:** workspaces, directory-per-environment, or Terragrunt?
3. **Who can `apply`, and from where:** a laptop, or CI only?
4. **Module versioning:** pinned refs or floating?
5. **Drift policy:** detect and alert, or auto-revert?

## Success criteria

- [ ] `staging` and `prod` are built from the **same modules**, and differ only in inputs.
- [ ] A bad `apply` in staging **cannot** touch prod state.
- [ ] Every change goes through a PR that shows the `plan` output.
- [ ] A manual console change is detected within 24 hours, without a human looking.
- [ ] You can rebuild staging from nothing with one documented command sequence.

## Prerequisites and cost

- Terraform ≥ 1.10 (for S3-native state locking), an AWS account, and the AWS CLI.
- **Cost warning:** a NAT gateway plus a small RDS instance costs roughly $40–70/month per environment.
  Run `terraform destroy` on `envs/*` when you are not working on it. The `bootstrap/` state bucket costs pennies.
- Prefer a different cloud? Keep the structure and ADRs, and swap the provider. That swap is itself a good ADR.

## Starter layout

```
bootstrap/            # one-time: S3 bucket for remote state (local state, chicken-and-egg)
modules/network/      # VPC, public/private subnets, NAT
modules/database/     # RDS Postgres in private subnets
envs/staging/         # root module: wires modules together with staging inputs
envs/prod/            # same wiring, prod inputs, separate state key
.github/workflows/
  terraform-plan.yml  # plan on PR, comment the output
  drift-detection.yml # nightly plan -detailed-exitcode, alerts on drift
scripts/drift-check.sh
docs/adr/             # decisions, with options already listed
docs/break-it.md      # failure experiments to run
docs/scale.md         # what you would do at 10x / 100x
```

## Milestones

### Build
- [ ] Fill in ADR-0001 (state layout) and ADR-0002 (environment separation) **before** writing more Terraform.
- [ ] `cd bootstrap && terraform init && terraform apply` to create the state bucket.
- [ ] Put the bucket name into `envs/*/backend.tf`, then `terraform init` in each environment.
- [ ] Apply staging. Confirm the outputs (VPC ID, DB endpoint).

### Test
- [ ] `terraform fmt -check -recursive` and `terraform validate` run in CI.
- [ ] Add `tflint` and `checkov` (or `trivy config`) to CI, and record what each catches.
- [ ] Show that a PR prints a plan without anyone running Terraform locally.

### Break
- [ ] Run every experiment in [`docs/break-it.md`](docs/break-it.md) and write a postmortem for each.

### Decide
- [ ] Fill in ADR-0003 (apply permissions) and ADR-0004 (drift policy) using what broke.

### Improve
- [ ] Wire `drift-detection.yml` to a real alert (Slack webhook, GitHub issue, or email).
- [ ] Use OIDC from GitHub to AWS. No long-lived keys (this links to project 05).

### Document
- [ ] Draw the architecture (network, DB, state bucket, CI role).
- [ ] Write [`docs/scale.md`](docs/scale.md) in your own words.
- [ ] Fill in the interview story below.

## ADRs

| # | Decision | Status |
|---|----------|--------|
| [0001](docs/adr/0001-state-layout.md) | How to split Terraform state | Proposed |
| [0002](docs/adr/0002-environment-separation.md) | Workspaces vs directories vs Terragrunt | Proposed |
| [0003](docs/adr/0003-who-can-apply.md) | Where `apply` is allowed to run | Proposed |
| [0004](docs/adr/0004-drift-policy.md) | Detect vs auto-remediate drift | Proposed |

## Interview story (fill in when done)

> "The problem was ___. I split state by ___ because ___. When I ___ (break-it),
> ___ happened, so I changed ___. At a larger org I would ___ because ___."
