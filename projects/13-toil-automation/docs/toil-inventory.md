# Toil inventory: measure before you automate

Toil = manual, repetitive, automatable, reactive work that scales with the size of the system and has no lasting value.
List every candidate for **two weeks** (or from your game days and break-it experiments), with honest numbers.

| Task | Trigger | Frequency / week | Minutes each | Hours / month | Risk if done wrong | Automatable? | Better fix elsewhere? (project) | Decision |
|------|---------|------------------|--------------|---------------|--------------------|--------------|----------------------------------|----------|
| Pre-market readiness check | Every trading day 08:30 | 5 | | | | | | |
| Restart stuck consumer | Lag alert | | | | | | | |
| Check cert expiry | Monthly | | | | | | | |
| Disk cleanup | Disk alert | | | | | | 11 (log rotation)? | |
| | | | | | | | | |

**Rank by hours/month × risk.** Automate from the top. Delete rows where the right answer is fixing the cause.
