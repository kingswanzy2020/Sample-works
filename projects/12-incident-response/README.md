# Project 12: Incident response and on-call

> **Problem:** Incidents are chaotic. Three people debug the same thing while nobody updates the trading desk.
> Nobody is sure who's in charge. The same incident happens again a month later because the follow-up actions were never done.

**Need help while building?** See [`docs/build-plan.md`](docs/build-plan.md): tasks with a goal and a "done when" check, hints hidden in levels (nudge → concept → docs), and a diagnosis table. It never gives you the full solution.

This project is about **people and process during and right after an incident**. You design the process,
then test it in game days against the landscape, with someone else injecting faults you can't see.

## Decisions this project proves you can make

1. **Severity model:** what Sev1/2/3 mean in business terms, and whether market hours change them.
2. **Roles:** incident commander, operations, communications and scribe, and how that works with two people.
3. **On-call design:** rotation, escalation, handoff, and what to do when a service has **no owner**.
4. **Runbook vs automation:** which response steps stay human, and which go to project 14.
5. **Postmortem policy:** which incidents get one, blameless format, and how actions are tracked.

## Success criteria

- [ ] A written process (`process/`) that someone new could follow under stress.
- [ ] At least **3 game days**, each with an incident record (`incidents/*.yaml`) and a postmortem.
- [ ] Measured detection and mitigation times per game day, compared with the hidden injection log.
- [ ] At least one process change made *because* a game day exposed a gap, recorded as a superseding ADR.
- [ ] Every action item has an owner and a due date, and you track whether it's done.

## Prerequisites and cost

- Free: Docker, Python 3. Uses the shared **landscape** (simulated trading platform).
- Ideally a second person as game master. Solo works with the randomized delay.

## Starter layout

```
gameday/scenarios.yaml      # hidden fault scenarios (the game master reads this, responders don't)
gameday/game_master.py      # injects a scenario at a random time; logs ground truth; reveal afterwards
process/                    # PROMPTS for your process docs: severity, roles, comms, on-call, runbook standard
incidents/SCHEMA.md         # the structured incident record (read by projects 16 and 17)
incidents/TEMPLATE.yaml
../../landscape/            # the platform you respond to (catalog, simulator, alerts, runbooks)
```

## Run a game day

```bash
cd ../../landscape && docker compose up -d --build      # in an extracted repo: cd landscape
cd - && pip install pyyaml
python gameday/game_master.py run          # game master's terminal
# responders: watch http://localhost:9093 (alerts) and http://localhost:9090 (metrics)
python gameday/game_master.py clear && python gameday/game_master.py reveal
```

## How this project connects

| Direction | Project | What flows |
|-----------|---------|------------|
| Uses | Landscape | The platform, alerts and (deliberately uneven) runbooks you respond with |
| Uses | Break-it experiments from [03](../03-zero-downtime-deploys/), [04](../04-observability-slos/), [06](../06-backup-and-dr/), [09](../09-kafka-streaming-reliability/) | Good sources of extra game-day scenarios |
| Feeds | [14 Triage pipeline](../14-alert-triage-pipeline/) | The triage steps you repeat in every game day are what 14 automates |
| Feeds | [16 Reliability reporting](../16-reliability-reporting/) | `incidents/*.yaml`: impact per service, root-cause dependency, detection times |
| Feeds | [17 Governance](../17-reliability-governance/) | Action items (done or not), runbook usefulness, and the runbook standard you define here |

**Not in this project:** designing alerts and SLOs (04), automating triage (14), and cross-incident trends and accountability (16, 17).
Here you handle **one incident at a time**, and the process around it.

## ADRs

| # | Decision | Status |
|---|----------|--------|
| [0001](docs/adr/0001-severity-model.md) | Severity levels and market hours | Proposed |
| [0002](docs/adr/0002-incident-roles.md) | Roles and when to declare an incident | Proposed |
| [0003](docs/adr/0003-on-call-design.md) | Rotation, escalation, unowned services | Proposed |
| [0004](docs/adr/0004-runbook-vs-automation.md) | What stays human, what gets automated | Proposed |
| [0005](docs/adr/0005-postmortem-policy.md) | Which incidents get postmortems; action tracking | Proposed |

## Interview story

> "Our first game day took ___ minutes to detect and ___ to mitigate, and nobody updated the desk for ___ minutes.
> I introduced ___ (roles / severity / comms). By the third game day it was ___ and ___. The stale runbook for ___ cost us ___,
> which is why I ___."
