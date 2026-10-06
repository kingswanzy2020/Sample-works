# Project 11: Configuration management for a hybrid fleet (Ansible)

> **Problem:** Twenty "identical" Linux servers aren't identical anymore. Someone applied a hotfix by hand,
> patching is a manual weekend job, and nobody can answer "which kernel is trading-07 running?" without logging in.

**Need help while building?** See [`docs/build-plan.md`](docs/build-plan.md): tasks with a goal and a "done when" check, hints hidden in levels (nudge → concept → docs), and a diagnosis table. It never gives you the full solution.

## Decisions this project proves you can make

1. **Mutable vs immutable:** configure long-lived hosts (Ansible), or replace them from images (Packer)?
2. **Push vs pull:** run from a control node/CI, or have each host pull its config?
3. **Rolling changes safely:** batch size, health gates, and when to stop a rollout.
4. **Testing roles** before they touch a real server.
5. **Source of truth for inventory:** static file, cloud API, or the service catalog.

## Success criteria

- [ ] `site.yml` brings any lab server from "fresh" to "baseline" and a second run reports **0 changed** (idempotent).
- [ ] Drift seeded by `scripts/seed-drift.sh` is **detected and reported** without logging into any server.
- [ ] A bad change rolled out to the fleet stops itself after the first batch.
- [ ] A fleet report answers "what OS/kernel/package version is everywhere?" in one command.
- [ ] Project 10's tuning exists as a role, applied to real VMs, with a check that the setting took effect.

## Prerequisites and cost

- Docker (the lab fleet is 6 SSH-reachable containers), Python 3, `ansible-core`.
- **Containers share the host's kernel.** They're good for packages, users, files, services and SSH config,
  but kernel settings (sysctl, boot parameters) need **VMs** (Multipass, Vagrant, or two small cloud instances).
  Plan which parts of the project need which.

## Starter layout

```
lab/                       # Dockerfile + compose for 6 lab servers (ports 2221–2226), ops user, SSH key auth
scripts/lab-up.sh          # creates the lab SSH key and starts the fleet
scripts/seed-drift.sh      # randomly mutates servers: your drift detection must find it
ansible.cfg  inventory/lab.ini  inventory/group_vars/all.yml
site.yml                   # baseline for all, latency tuning for trading
roles/baseline/            # EMPTY: you write it
roles/latency_tuning/      # EMPTY: you write it from project 10's tuning list
playbooks/ping.yml         # reachability + sudo check
```

## Run

```bash
pip install ansible-core
scripts/lab-up.sh
ansible-playbook playbooks/ping.yml
ansible-playbook site.yml --check --diff
```

## How this project connects

| Direction | Project | What flows |
|-----------|---------|------------|
| Uses | [10 Linux latency](../10-linux-performance-latency/) | Its proven tuning list becomes `roles/latency_tuning` |
| Boundary with | [01 IaC](../01-iac-multi-env/) | 01 **provisions** machines (Terraform). 11 **configures** what runs on them. Writing that boundary down is part of ADR-0001 |
| Optional link | [09 Kafka](../09-kafka-streaming-reliability/) | If 09's ADR-0004 chose self-hosted Kafka on VMs, Ansible is how those brokers would be managed |
| Uses | [05 Secrets](../05-secrets-and-rotation/) | Secrets in playbooks: Ansible Vault vs a lookup from your secrets store |
| Feeds | [13 Toil automation](../13-toil-automation/) | Patching and drift checks you automate here are *removed* from 13's toil list. 13 handles what isn't config management |

**Not in this project:** provisioning cloud resources (01), container platforms (03/08), and the latency research itself (10).

## ADRs

| # | Decision | Status |
|---|----------|--------|
| [0001](docs/adr/0001-mutable-vs-immutable.md) | Configure hosts vs replace them from images | Proposed |
| [0002](docs/adr/0002-push-vs-pull.md) | Push from control node/CI vs pull on hosts | Proposed |
| [0003](docs/adr/0003-rolling-change-strategy.md) | Batch size, health gates, failure thresholds | Proposed |
| [0004](docs/adr/0004-testing-roles.md) | How roles are tested before production | Proposed |
| [0005](docs/adr/0005-inventory-source-of-truth.md) | Where the inventory comes from | Proposed |

## Interview story

> "The fleet had drifted: ___ of 6 servers differed from baseline in ___ ways. I wrote roles for ___, made them idempotent,
> and detect drift with ___. A bad change once ___, so rollouts now go in batches of ___ with ___ as a gate.
> At 1,000 servers I'd ___."
