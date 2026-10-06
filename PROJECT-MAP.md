# Project map: how the 17 projects connect

Every project stands on its own and can be extracted into its own repo. Many of them also **use something another project
produces**, or **feed something into a later one**. This page shows those links, and the boundaries that stop projects repeating each other.

Each project README also has a **"How this project connects"** section with the same information from that project's point of view.

---

## The three tracks

| Track | Projects | What it proves |
|-------|----------|----------------|
| **A. Build and run one system well** | 01–08 | Infrastructure as code, CI/CD, deploys, observability, secrets, DR, cost, platform |
| **B. Systems underneath** | 09–11 | Streaming (Kafka), host performance (Linux), fleet configuration (Ansible) |
| **C. Reliability operations across many services** | 12–17 | Incident response, toil, triage, monitoring coverage, reliability reporting, governance |

Track C runs on the shared **landscape** (`landscape/`): a simulated trading platform with 8 services, dependencies,
alerts and runbooks, all deliberately imperfect.

---

## Data and dependency flow

```
                         ┌──────────────── Track A ────────────────┐
   01 IaC ──► 02 CI/CD ──► 03 Deploys ──► 04 Observability ──► 05 Secrets ──► 06 DR ──► 07 Cost ──► 08 Platform
     │                        │                 │
     │ provisions             │ canary uses     │ concepts, Prometheus/Grafana
     ▼                        ▼                 ▼
   11 Ansible ◄── tuning ── 10 Linux latency   09 Kafka ──────────────┐
   (configures hosts)        ▲                   │ lag, freshness SLO  │
                             └── workload ───────┘                     │
                                                                       ▼
   ┌──────────────────────────── Track C (uses landscape/) ─────────────────────────────────┐
   │                                                                                         │
   │  12 Incident response ──(triage steps to automate)──► 14 Triage pipeline                │
   │        │  incidents/*.yaml                               │  triage-log, feedback        │
   │        │                         13 Toil ──(read-only    │                              │
   │        │                          diagnostics)──────────►│                              │
   │        ▼                                                 ▼                              │
   │  16 Reliability reporting ◄── SLI gaps ── 15 Coverage audit                             │
   │        │  missed SLOs per owner                │ gap backlog with owners                 │
   │        └──────────────────────► 17 Governance ◄┘◄── triage data (14), incidents (12)    │
   └─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Every connection, in one table

| From | To | What flows | Required or optional? |
|------|----|------------|-----------------------|
| 01 IaC | 11 Ansible | 01 provisions machines, 11 configures them (boundary decided in 11's ADR-0001) | Optional |
| 01 IaC | 05, 06, 07 | AWS account, tags, state bucket, RDS secret | Optional (their AWS parts only) |
| 02 CI/CD | 03, 08 | Signed images, promote-by-digest | Optional |
| 03 Deploys | 09 Kafka | Run Kafka on Kubernetes (Strimzi) if 09's ADR-0004 chooses it | Optional |
| 04 Observability | 03, 09, 15, 16 | Prometheus/Grafana stack and SLO concepts | Recommended first |
| 05 Secrets | 01, 02, 11 | OIDC roles; secrets in playbooks | Optional |
| 09 Kafka | 10 Linux latency | Consumer latency as a second workload | Optional |
| 09 Kafka | 13 Toil | Lag/offsets for `restart-stuck-consumer` and market readiness | Optional |
| 09 Kafka | Landscape `kafka` | What you learn shapes the Kafka runbook and alerts used in 12–17 | Optional |
| 10 Linux latency | 11 Ansible | The proven tuning list becomes `roles/latency_tuning` | **Required for 11's last task** |
| 12 Incidents | 14 Triage | ADR-0004: the triage steps to automate; game days to measure the effect | **Recommended before 14** |
| 12 Incidents | 16, 17 | `incidents/*.yaml` (schema in 12) | **Required** for attribution (16) and follow-through (17); 17 has sample data meanwhile |
| 13 Toil | 14 Triage | Read-only actions run as diagnostics | Optional |
| 14 Triage | 16 Reporting | Correlation groups = incidents per root cause | Optional |
| 14 Triage | 17 Governance | `triage-log.jsonl`, `feedback.jsonl` (contract in 14's `docs/triage-log-schema.md`) | **Required** for real data; 17 has sample data meanwhile |
| 15 Coverage | 16 Reporting | Services without SLIs can't be reported | Recommended |
| 15 Coverage | 17 Governance | Gap backlog with owners and due dates | Recommended |
| 16 Reporting | 17 Governance | Missed SLOs and budget burn per owner | Recommended |

---

## Boundaries: who does what (so nothing is repeated)

Where two projects touch the same topic, each one does a **different job**:

| Topic | Project | Its job | Not its job (see) |
|-------|---------|---------|-------------------|
| Monitoring | 04 | Build good metrics, logs, traces and SLO alerts for **one** service | Auditing many services (15) |
| | 15 | Check **many** services against a standard; find gaps | Handling alerts as they fire (14) |
| SLOs | 04 | Define one SLO and **alert** on its burn | Reporting across services (16) |
| | 16 | **Report** many SLOs over time, with attribution, for people | Alerting (04) |
| Alerts | 04 / landscape | Write alert rules | Processing them (14) |
| | 14 | Process each alert **as it arrives**: enrich, correlate, route | Judging alert quality over weeks (17) |
| | 17 | Judge alert **quality over time** and drive owners to fix it | Writing or processing alerts |
| Incidents | 12 | Handle **one incident** at a time: roles, comms, postmortem | Trends across incidents (16, 17) |
| | 17 | **Patterns** across incidents: repeats, overdue actions | Running the incident |
| Automation | 11 | Host **configuration** and patching (desired state) | Operational tasks (13) |
| | 13 | **Operator-triggered/scheduled** tasks with guardrails | Reacting to alerts (14) |
| | 14 | **Event-driven** triage when alerts fire | Scheduled toil (13) |
| CPU / latency | 07 | CPU limits from a **cost and throughput** angle in Kubernetes | Host-level tail latency (10) |
| | 10 | **Host-level** tail latency: cores, IRQs, kernel | Autoscaling and cost (07) |
| Infrastructure | 01 | **Provision** cloud resources (Terraform) | Configure what runs on hosts (11) |
| | 11 | **Configure** hosts (Ansible) | Provisioning (01) |
| Scorecards | 08 | Check a repo's **files** against the paved road | Live monitoring reality (15) |
| | 15 | Check **live** monitoring against a standard | Repo contents (08) |
| | 17 | Score **team behaviour**: follow-through, alert hygiene | Technical coverage (15) |

---

## Suggested order

- **Track A in order (01 → 08).** Each builds on the one before.
- **Track B after 04:** 09 → 10 → 11 (10 feeds 11).
- **Track C after 04 and at least one of 09–11:** **12 → 13 → 14 → 15 → 16 → 17.**
  12 creates the incident data and the list of triage steps. 14 automates them. 15 and 16 measure. 17 drives change using everything before it.

**Short on time for an SRE role?** Do **04 → 09 → 12 → 14 → 16 → 17**. That covers streaming, incidents, triage automation,
reliability reporting and accountability, which is most of a typical SRE job description.

---

## Shared directories

| Directory | Used by | Notes |
|-----------|---------|-------|
| `app/` | 02–08 | The sample web service |
| `landscape/` | 12–17 | Simulated trading platform. Don't fix its flaws in advance; the projects find them |
| `templates/` | all | ADR, postmortem, break-it templates |

`scripts/new-project-repo.sh <NN> <dest>` copies a project plus the shared directories listed in its `SHARED` file.
