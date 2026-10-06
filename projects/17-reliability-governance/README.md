# Project 17: Reliability governance: ownership, alert quality, runbooks, follow-through

> **Problem:** A tier-1 service has no owner. One alert pages 40 times a week and is almost never actionable.
> A runbook tells responders to "check ZooKeeper" on a system that no longer uses it. The same incident recurs because the
> postmortem actions sit open for weeks. Everyone knows, and nothing changes, because nobody has the data and nobody owns the follow-up.

**Need help while building?** See [`docs/build-plan.md`](docs/build-plan.md): tasks with a goal and a "done when" check, hints hidden in levels (nudge → concept → docs), and a diagnosis table. It never gives you the full solution.

Responsibility this project answers: *"Call out weak ownership, missed SLAs, poor alerts and ineffective runbooks,
and drive the owning teams to fix them."*

This is the most **human** project: the code produces evidence, but the outcome is other teams changing what they do,
without you being their manager.

## Decisions this project proves you can make

1. **Which metrics:** what to measure so teams improve the system instead of gaming the number (Goodhart's law).
2. **Visibility:** public scorecard vs private feedback to each team.
3. **Escalation:** when an ignored finding goes up, to whom, and what SRE may do on its own.
4. **Bad alerts:** delete, downgrade, rewrite or reassign, and who decides.
5. **Forum and cadence:** weekly ops review, monthly, or per-incident, and who attends.

## Success criteria

- [ ] Metrics for ownership, alert quality, runbook quality, action follow-through and SLO misses, each with a written definition and tests.
- [ ] Each metric finds the problems planted in the sample data (and in the landscape) that you found by hand first.
- [ ] At least 3 weekly ops reviews (`review/`), with findings written using the finding template.
- [ ] At least one finding taken **all the way to fixed**: evidence → conversation → change → metric improves. Ideally with a real second person playing the owning team.
- [ ] One case where a metric was gamed or misleading, and how you changed it (a superseding ADR).

## Prerequisites and cost

- Free: Python 3.12. Works standalone on generated sample data. Switches to real data from projects 12, 14, 15 and 16.

## Starter layout

```
sample-data/generate.py     # 4 weeks of alerts, feedback and incidents with patterns planted (run it first)
governance/sources.py       # loaders: sample data by default, real data via env vars (TRIAGE_DIR, INCIDENTS_DIR, CATALOG)
governance/metrics.py       # ownership_gaps implemented as the example; the rest are STUBS
governance/scorecard.py     # runs every metric, groups findings by owner
review/ops-review-template.md   review/finding-template.md   review/escalation-policy.md (prompts)
tests/test_metrics.py
```

## Run

```bash
pip install -r requirements-dev.txt
python sample-data/generate.py
python -m pytest
python -m governance.scorecard
```

## How this project connects

| Direction | Project | What flows |
|-----------|---------|------------|
| Uses | [14 Triage](../14-alert-triage-pipeline/) | `triage-log.jsonl` + `feedback.jsonl`: alert volume, routing, actionability |
| Uses | [12 Incident response](../12-incident-response/) | Incident records: action items, runbooks used (and whether they helped), repeat root causes; the runbook standard |
| Uses | [15 Coverage audit](../15-monitoring-coverage-audit/) | Gap backlog with owners and due dates: overdue gaps become findings |
| Uses | [16 Reliability reporting](../16-reliability-reporting/) | Missed SLOs and budget burn per owner |
| Uses | Landscape | Catalog ownership and runbook dates; the runbooks themselves |
| Uses | [13 Toil](../13-toil-automation/) | Optional: toil hours and automation audit logs as a team-health metric |

This project is where the reliability-operations track (12 → 14 → 15 → 16 → 17) comes together: each one before it produces data, and this one turns that data into change.

**Not in this project:** collecting the data (12, 14, 15, 16 do that). Here you **judge it, communicate it, and follow through**.

## ADRs

| # | Decision | Status |
|---|----------|--------|
| [0001](docs/adr/0001-which-metrics.md) | What to measure (and what gets gamed) | Proposed |
| [0002](docs/adr/0002-visibility.md) | Public scorecard vs private feedback | Proposed |
| [0003](docs/adr/0003-escalation.md) | Escalation path and SRE's own authority | Proposed |
| [0004](docs/adr/0004-bad-alert-policy.md) | What happens to bad alerts | Proposed |
| [0005](docs/adr/0005-review-forum.md) | Review forum and cadence | Proposed |

## Interview story

> "One alert paged ___ times a week and was actionable ___% of the time, a tier-1 service had no owner, and the same price-feed incident happened twice
> because actions sat open. I built a scorecard from triage, incident and SLO data, ran a weekly review, and wrote findings as ___.
> The ___ team fixed ___ within ___. One metric got gamed (___), so I changed it to ___. Without authority, what worked was ___."
