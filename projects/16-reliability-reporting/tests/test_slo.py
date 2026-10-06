import pytest
from reliability_report import slo


def test_budget_remaining_full_partial_and_overspent():
    assert slo.budget_remaining(0.99, 1.0) == pytest.approx(1.0)
    assert slo.budget_remaining(0.99, 0.995) == pytest.approx(0.5)
    assert slo.budget_remaining(0.99, 0.98) == pytest.approx(-1.0)


def test_no_data_is_not_success(monkeypatch):
    monkeypatch.setattr(slo.sources, "prom_scalar", lambda expr: None)
    r = slo.evaluate({"service": "s", "name": "a", "objective": 0.99, "window": "1h",
                      "sli": {"good": "g", "total": "t"}})
    assert r.actual is None and r.met is None


def test_window_is_substituted(monkeypatch):
    seen = []
    monkeypatch.setattr(slo.sources, "prom_scalar", lambda expr: seen.append(expr) or 1.0)
    slo.evaluate({"service": "s", "name": "a", "objective": 0.99, "window": "7d",
                  "sli": {"good": "x[{{window}}]", "total": "y[{{window}}]"}})
    assert seen == ["x[7d]", "y[7d]"]

# TODO (you): tests for composite_availability, attribute and trading-hours evaluation,
# written BEFORE the code.
