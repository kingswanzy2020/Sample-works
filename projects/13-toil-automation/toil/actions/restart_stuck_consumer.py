"""TODO (you): restart a Kafka consumer that has stopped making progress (project 09).

Questions this action must answer before it's allowed to change anything:
- How do you know a consumer is STUCK, not just slow?
  (Lag growing AND committed offset not moving for N minutes?)
- What's the blast radius? One consumer instance, never the whole group at once.
- What must be true before restarting (market hours? an open incident?), and who is told afterwards?

plan() returns the restarts it WOULD do; apply() does one. The framework handles dry-run, limits and audit.
"""
from toil.framework import Action


class RestartStuckConsumer(Action):
    name = "restart-stuck-consumer"
    help = "restart consumers whose offsets stopped moving [NOT WRITTEN YET]"

    def plan(self, args):
        raise SystemExit("restart-stuck-consumer: not implemented yet (see the docstring in this file)")
