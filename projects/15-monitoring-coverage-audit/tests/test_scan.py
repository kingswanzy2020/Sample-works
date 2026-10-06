from coverage_audit import scan as scan_mod
from coverage_audit import sources

CATALOG = {
    "a": {"name": "a", "tier": 1},
    "b": {"name": "b", "tier": 3},
    "k": {"name": "k", "tier": 1, "kind": "platform"},
}


def test_required_checks_follow_tier_and_platform():
    standard = {"required_by_tier": {1: ["has_owner"], 3: []}, "required_for_platform": ["has_metrics"]}
    assert scan_mod.required_checks(CATALOG["a"], standard) == ["has_owner"]
    assert scan_mod.required_checks(CATALOG["b"], standard) == []
    assert scan_mod.required_checks(CATALOG["k"], standard) == ["has_metrics"]


def test_unimplemented_checks_report_todo_not_pass(monkeypatch):
    monkeypatch.setattr(sources, "catalog", lambda: CATALOG)
    rows = scan_mod.scan({"required_by_tier": {1: ["has_owner"]}})
    assert {r["result"] for r in rows} == {"TODO"}


def test_a_crashing_check_is_reported_as_fail(monkeypatch):
    monkeypatch.setattr(sources, "catalog", lambda: {"a": CATALOG["a"]})
    monkeypatch.setitem(scan_mod.REGISTRY, "boom", lambda *a: 1 / 0)
    rows = scan_mod.scan({"required_by_tier": {1: ["boom"]}})
    assert rows[0]["result"] == "FAIL" and "check error" in rows[0]["detail"]

# TODO (you): a test per check you implement, using fake catalog entries and fake Prometheus data.
