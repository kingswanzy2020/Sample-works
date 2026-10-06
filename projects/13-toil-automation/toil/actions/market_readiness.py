"""TODO (you): the pre-market-open readiness check.

Decide what "ready to trade" means (ADR-0001 / your toil inventory), for example:
tier-1 services up, error rates normal, Kafka lag near zero, certificates valid,
no open Sev1/Sev2, yesterday's batch jobs finished.
Sources: the landscape simulator/Prometheus, project 09's lag,
project 12's incidents.

Read-only. Output must be readable by a human at 08:45 in under 30 seconds.
"""
from toil.framework import Action


class MarketReadiness(Action):
    name = "market-readiness"
    help = "pre-open checklist for the trading platform (read-only) [NOT WRITTEN YET]"

    def plan(self, args):
        raise SystemExit("market-readiness: not implemented yet (see the docstring in this file)")
