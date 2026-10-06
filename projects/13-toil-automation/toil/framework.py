"""The safety rails every toil action runs inside.

An action describes WHAT to do; the runner decides WHETHER it may do it:
  - dry-run unless --execute is given (ADR-0002)
  - refuses to act on more than --max-targets at once (blast radius)
  - writes every planned and executed step to an append-only audit log
"""
from __future__ import annotations

import getpass
import json
import pathlib
import time
from dataclasses import dataclass, field


@dataclass
class Step:
    target: str
    description: str
    changes_something: bool = True


@dataclass
class Result:
    target: str
    ok: bool
    detail: str = ""


class Action:
    """Base class. Subclasses implement plan() and, for changing actions, apply()."""

    name = "unnamed"
    help = ""

    def add_arguments(self, parser) -> None:  # optional per-action CLI args
        pass

    def plan(self, args) -> list[Step]:
        raise NotImplementedError

    def apply(self, step: Step, args) -> Result:
        raise NotImplementedError(f"{self.name} is read-only or apply() isn't written yet")


@dataclass
class Runner:
    audit_log: pathlib.Path
    execute: bool = False
    max_targets: int = 5
    actor: str = field(default_factory=getpass.getuser)

    def _audit(self, action: str, event: str, **data) -> None:
        self.audit_log.parent.mkdir(parents=True, exist_ok=True)
        with self.audit_log.open("a") as f:
            f.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "actor": self.actor,
                                "action": action, "event": event, "execute": self.execute, **data}) + "\n")

    def run(self, action: Action, args) -> list[Result]:
        steps = action.plan(args)
        changing = [s for s in steps if s.changes_something]
        self._audit(action.name, "plan", steps=[s.__dict__ for s in steps])

        if len({s.target for s in changing}) > self.max_targets:
            self._audit(action.name, "refused", reason="blast radius", targets=len(changing))
            raise SystemExit(f"refusing: {len(changing)} targets would change, limit is {self.max_targets} "
                             f"(raise --max-targets deliberately if this is intended)")

        results = []
        for step in steps:
            if not step.changes_something:
                results.append(Result(step.target, True, step.description))
            elif not self.execute:
                results.append(Result(step.target, True, f"DRY-RUN would: {step.description}"))
            else:
                try:
                    results.append(action.apply(step, args))
                except Exception as exc:  # one failing target must not hide the others
                    results.append(Result(step.target, False, f"error: {exc}"))
        self._audit(action.name, "result", results=[r.__dict__ for r in results])
        return results
