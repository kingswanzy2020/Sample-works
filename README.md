# decision-driven-devops

A DevOps portfolio built on decisions, not tool lists.

> **Build. Test. Break. Decide. Improve. Document.**

This repo is the hub: a roadmap of seventeen DevOps and SRE projects. Each one starts from a real problem and is built
to answer one question: **"What decisions do I want this project to prove I can make?"**

The goal is to say more than *"I used Docker, Terraform and GitHub Actions"* in an interview. The goal is:

> I built this system. This was the problem. This is why I chose this approach.
> This is what broke. This is what I changed. And this is what I'd do differently at a different scale.

Every project comes with:

| What | Why it's there |
|------|----------------|
| `README.md` | The problem, the decisions it proves, measurable success criteria, and a Build → Document checklist |
| Starter code | Enough to get running quickly, with the decision points marked `DECISION (ADR-NNNN)` in comments |
| `docs/adr/` | ADRs with the context and options already written. **You** write the decision |
| `docs/break-it.md` | Failure experiments with a hypothesis, procedure and what to measure |
| `docs/postmortems/` | Where each break-it experiment gets written up |
| `docs/scale.md` | "What I'd do at 10× / 100×", the closing line of your interview story |
| `docs/build-plan.md` | Tasks, levelled hints and a diagnosis table for when you're stuck |

## The projects

The projects come in three tracks. Many of them connect: one produces something the next one uses.
**[PROJECT-MAP.md](PROJECT-MAP.md)** shows every connection, the boundaries that keep projects from repeating each other,
and a suggested order. Each project README also has a "How this project connects" section.

### Track A: build and run one system well (01–08)

Each one is an **evolution of the same system** (one app, growing up), so each has a natural "why":
*"Once I could deploy, I couldn't tell if deploys were healthy, so I added observability."*

| # | Project | The problem | Key decisions | Runs on |
|---|---------|-------------|---------------|---------|
| 01 | [Multi-env IaC + drift detection](projects/01-iac-multi-env/) | Staging and prod drifted; someone changed something in the console | State layout and blast radius, env separation, who can `apply`, drift policy | AWS (Terraform) |
| 02 | [Fast and safe CI/CD](projects/02-cicd-fast-and-safe/) | CI takes 25 min; flaky tests; unknown image contents | What runs per change, caching, security gates, flaky policy, promote by digest | GitHub Actions |
| 03 | [Zero-downtime deploys](projects/03-zero-downtime-deploys/) | Every deploy drops requests; migrations break the old version | Rolling vs blue/green vs canary, expand/contract, health definition, rollback | kind (local) |
| 04 | [Observability + SLOs](projects/04-observability-slos/) | "It's slow" and nobody can find out why; noisy alerts | SLOs, symptom vs cause alerting, sampling, cardinality, buy vs run | Docker Compose |
| 05 | [Secrets + rotation](projects/05-secrets-and-rotation/) | Secrets in `.env`, never rotated, ex-employees still have access | Store choice, static vs dynamic creds, OIDC trust, behaviour when Vault is down | Docker Compose + AWS |
| 06 | [Backup + disaster recovery](projects/06-backup-and-dr/) | "We have backups" but nobody has restored one | RPO/RTO, dumps vs PITR, DR topology, restore drills, backup isolation | Docker Compose + AWS |
| 07 | [Cost-aware autoscaling](projects/07-cost-aware-autoscaling/) | Bill doubled *and* spikes still cause slowdowns | Scaling signal, right-sizing, spot vs on-demand, cost ownership | kind (+ EKS optional) |
| 08 | [Internal developer platform](projects/08-internal-developer-platform/) | Each new service takes a week and is built differently | Abstraction level, GitOps, guardrails vs gates, measuring the platform | kind + Argo CD |

> In my earlier list the numbering was different. Here the folders follow the **build order**:
> IaC first (foundation), the platform last (it packages everything else).

### Track B: the systems underneath (09–11)

| # | Project | The problem | Key decisions | Runs on |
|---|---------|-------------|---------------|---------|
| 09 | [Reliable Kafka streaming](projects/09-kafka-streaming-reliability/) | Broker failures lose or duplicate ticks; lag grows silently | acks/ISR/replication, delivery semantics, partitioning, freshness SLO, run vs buy | Docker Compose |
| 10 | [Linux performance and tail latency](projects/10-linux-performance-latency/) | p99.9 spikes while averages look fine | Measurement method, CPU isolation, kernel tuning scope, containers vs bare metal | A Linux host / VM |
| 11 | [Ansible for a hybrid fleet](projects/11-ansible-fleet-config/) | "Identical" servers have drifted; patching is manual | Mutable vs immutable, push vs pull, rolling strategy, role testing, inventory source | Docker lab + VMs |

### Track C: reliability operations across many services (12–17)

These run on the shared **landscape**: a simulated trading platform with 8 services, dependencies, alerts and runbooks,
all deliberately imperfect. The projects find and fix those flaws.

| # | Project | The problem | Key decisions | Runs on |
|---|---------|-------------|---------------|---------|
| 12 | [Incident response and on-call](projects/12-incident-response/) | Chaotic incidents; actions never done; unowned services | Severity model, roles, on-call design, runbook vs automation, postmortem policy | Landscape + game days |
| 13 | [Toil automation with guardrails](projects/13-toil-automation/) | Hours a week on repetitive manual tasks | What to automate first, safety model, when not to automate, interface | Python |
| 14 | [Automated alert triage](projects/14-alert-triage-pipeline/) | Bare alerts; one root cause pages five teams | Enrichment, correlation, automation boundary, fail-open, build vs buy | Landscape + Python |
| 15 | [Monitoring coverage audit](projects/15-monitoring-coverage-audit/) | Nobody knows which services are badly monitored | Minimum standard per tier, white vs black box, report vs enforce, who closes gaps | Landscape + Python |
| 16 | [Cross-service reliability reporting](projects/16-reliability-reporting/) | "Is reliability getting worse?" has no answer | SLA/SLO/SLI, SLO tooling, trading-hours windows, dependency attribution, report audience | Landscape + Python |
| 17 | [Reliability governance](projects/17-reliability-governance/) | Weak ownership, noisy alerts, stale runbooks, open actions | Metrics that resist gaming, visibility, escalation, bad-alert policy, review forum | Python (+ data from 12–16) |

## Start a project in its own repo

Each project is meant to become its own portfolio repo. Copy one out with:

```bash
scripts/new-project-repo.sh 03 ../zero-downtime-deploys
cd ../zero-downtime-deploys
```

The new repo contains the project files at its root, plus `templates/` and the shared directories the project needs
(listed in its `SHARED` file: `app/` for most of 01–08, `landscape/` for 12–17).
Inside an extracted repo, Docker Compose and Makefiles find the app at `./app` by default.
To run a project **inside this roadmap repo** instead, point at the shared app: `APP_DIR=../../app docker compose up`.

## What's shared

```
app/                    # the sample service projects 02–08 deploy (FastAPI + Postgres)
                        #   /healthz /readyz /metrics /version /items /work, plus failure injection via env vars
landscape/              # simulated trading platform for projects 12–17: catalog, metrics simulator with
                        #   fault injection, Prometheus, Alertmanager, runbooks (deliberately imperfect)
templates/
  adr-template.md       # Architecture Decision Record
  postmortem-template.md
  break-it-template.md
scripts/new-project-repo.sh
```

## When you need help

Each project has a **`docs/build-plan.md`**. It's a guide for when you're stuck, not a walkthrough:

- Every task gives a **goal** and a **"done when"** check, never the steps.
- **Hints are hidden in levels:** Hint 1 is a nudge, Hint 2 names the concept or tool, Hint 3 links the docs. Open one at a time, after a real attempt.
- **"Depends on your ADR"** notes tell you what to think about for the option you chose.
- A **"Stuck? Diagnose before you search"** table gives the questions to ask yourself for common failures.

Keep a short journal of which hints you needed. It's honest evidence of what you learned.

## How to work each project

1. **Read the problem.** Rewrite it in your own words with your constraints (budget, time, team size).
2. **Fill in the first ADRs before writing code.** Choosing *before* you build is the point.
3. **Measure the "before."** Every project asks for a baseline (CI minutes, failed requests, time to find a bug, restore time). Without it, "I improved X" isn't credible.
4. **Build** from the starter code. Search for `DECISION (ADR-` comments: they mark the decision points.
5. **Break it** using `docs/break-it.md`. Write the hypothesis first.
6. **Write a postmortem** for each break: what happened, how you found out, what you changed.
7. **Supersede, don't edit.** If a break proves an ADR wrong, write a new ADR that supersedes it. The change of mind is the best part of the story.
8. **Write `docs/scale.md`** and the interview story at the bottom of the project README.

## What a finished project looks like

- An ADR log where at least one decision was **reversed** by evidence.
- At least three postmortems with **measured** numbers (time to detect, time to recover, errors).
- A before/after table or graph.
- A README that opens with the problem and closes with "at 10× I would…".
- Short enough to explain in 2 minutes, deep enough to survive 20 minutes of follow-up questions.

## Cost and safety

- Projects 03, 04, 07, 08, 09 and 11–17 run fully locally for free. Projects 01, 05 and 06 have optional AWS parts. Project 10 needs a Linux host (your own, or a small cloud VM).
- Before any AWS work: set a budget alert (`projects/07-cost-aware-autoscaling/terraform/budgets`), and `terraform destroy` when you stop for the day.
- Lab shortcuts (Vault dev mode, `app:app` passwords, anonymous Grafana) are marked as such. Never copy them to anything real.
- Image tags and action versions were current when this was written. Bumping them is part of the work, and Dependabot (project 02) does it for you.
