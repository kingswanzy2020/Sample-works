# Project 13: Toil automation with guardrails

> **Problem:** The team loses hours every week to the same manual tasks: the pre-market checklist, restarting a stuck consumer,
> checking certificates, clearing disks. It's done slightly differently each time, and when someone is on holiday it's done late or not at all.

**Need help while building?** See [`docs/build-plan.md`](docs/build-plan.md): tasks with a goal and a "done when" check, hints hidden in levels (nudge → concept → docs), and a diagnosis table. It never gives you the full solution.

## Decisions this project proves you can make

1. **What to automate first:** measured toil (hours × risk), not whatever is most fun to build.
2. **Safety model:** dry-run by default, blast-radius limits, confirmation, audit trail.
3. **When *not* to automate:** fix the cause instead (log rotation in project 11, a better alert in 04).
4. **Interface:** CLI, chat bot, scheduled job, or self-healing controller.
5. **Ownership:** who maintains an automation once it exists, and how it's retired.

## Success criteria

- [ ] A toil inventory with **measured** hours/month, ranked by hours × risk (`docs/toil-inventory.md`).
- [ ] The top 2–3 items automated as `toil` actions, with tests.
- [ ] Every action is dry-run by default, refuses large blast radii, and writes an audit log.
- [ ] At least one item **removed** instead of automated (fixed at the cause), with the reasoning in an ADR.
- [ ] Before/after hours per month for the automated items.

## Prerequisites and cost

- Free: Python 3.12. Optional: the landscape (for market readiness) and project 09 (for consumer restarts).

## Starter layout

```
toil/framework.py          # Action/Step/Result + Runner: dry-run, --max-targets, audit log (done, tested)
toil/cli.py                # `python -m toil.cli <action>`
toil/actions/cert_expiry.py         # a finished read-only example to copy the pattern from
toil/actions/market_readiness.py    # STUB: you write it
toil/actions/restart_stuck_consumer.py  # STUB: you write it
toil/actions/disk_cleanup.py        # STUB: maybe you delete it instead (read its docstring)
tests/test_framework.py    # the safety rails are tested; your actions need tests too
docs/toil-inventory.md     # measure first
```

## Run

```bash
pip install -r requirements-dev.txt
python -m pytest
python -m toil.cli list
python -m toil.cli cert-expiry github.com example.com
```

## How this project connects

| Direction | Project | What flows |
|-----------|---------|------------|
| Uses | [09 Kafka](../09-kafka-streaming-reliability/) | Consumer lag and offsets: the input for `restart-stuck-consumer` |
| Uses | Landscape + [12 Incidents](../12-incident-response/) | Market readiness reads service health and open incidents |
| Boundary with | [11 Ansible](../11-ansible-fleet-config/) | Host configuration and patching belong in 11. If a toil item is really config drift, fix it there |
| Feeds | [14 Triage pipeline](../14-alert-triage-pipeline/) | 14 can call your **read-only** actions as diagnostic steps when an alert fires. The framework's dry-run and audit carry over |
| Feeds | [17 Governance](../17-reliability-governance/) | The audit log shows how often automation ran, and toil hours become a tracked metric |

**Not in this project:** reacting to alerts (that's 14, event-driven), and config management (11).
Here you build **operator-triggered and scheduled** automation, and decide what deserves it.

## ADRs

| # | Decision | Status |
|---|----------|--------|
| [0001](docs/adr/0001-what-to-automate-first.md) | Ranking toil: what to automate first | Proposed |
| [0002](docs/adr/0002-safety-model.md) | Dry-run, blast radius, confirmation, audit | Proposed |
| [0003](docs/adr/0003-when-not-to-automate.md) | Fix the cause vs automate the symptom | Proposed |
| [0004](docs/adr/0004-interface.md) | CLI vs bot vs scheduled vs self-healing | Proposed |

## Interview story

> "We spent about ___ hours a month on ___. I measured it, automated the top ___ with guardrails (___),
> and deleted ___ by fixing the cause in ___. Toil dropped to ___ hours. The audit log once showed ___, which led to ___."
