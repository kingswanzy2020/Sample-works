import json

import pytest
from toil.framework import Action, Result, Runner, Step


class Fake(Action):
    name = "fake"

    def __init__(self, n):
        self.n, self.applied = n, []

    def plan(self, args):
        return [Step(f"host-{i}", "restart") for i in range(self.n)]

    def apply(self, step, args):
        self.applied.append(step.target)
        return Result(step.target, True, "restarted")


def test_dry_run_never_applies(tmp_path):
    action = Fake(2)
    results = Runner(tmp_path / "a.jsonl").run(action, None)
    assert action.applied == []
    assert all("DRY-RUN" in r.detail for r in results)


def test_execute_applies(tmp_path):
    action = Fake(2)
    Runner(tmp_path / "a.jsonl", execute=True).run(action, None)
    assert action.applied == ["host-0", "host-1"]


def test_blast_radius_refuses_before_any_change(tmp_path):
    action = Fake(6)
    with pytest.raises(SystemExit):
        Runner(tmp_path / "a.jsonl", execute=True, max_targets=5).run(action, None)
    assert action.applied == []


def test_audit_log_records_plan_and_result(tmp_path):
    log = tmp_path / "a.jsonl"
    Runner(log, execute=True).run(Fake(1), None)
    events = [json.loads(line)["event"] for line in log.read_text().splitlines()]
    assert events == ["plan", "result"]
