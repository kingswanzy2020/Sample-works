"""SLI/SLO arithmetic. The 24/7 case is implemented; the rest is yours."""
from __future__ import annotations

from dataclasses import dataclass

from reliability_report import sources


@dataclass
class SloResult:
    service: str
    name: str
    objective: float
    actual: float | None          # None = no data (that is NOT 100%)
    budget_remaining: float | None  # fraction of error budget left, can go negative

    @property
    def met(self) -> bool | None:
        return None if self.actual is None else self.actual >= self.objective


def budget_remaining(objective: float, actual: float) -> float:
    allowed = 1 - objective
    spent = 1 - actual
    return 1 - spent / allowed if allowed else 0.0


def evaluate(slo: dict) -> SloResult:
    if slo.get("trading_hours_only"):
        return evaluate_trading_hours(slo)
    good = sources.prom_scalar(slo["sli"]["good"].replace("{{window}}", slo["window"]))
    total = sources.prom_scalar(slo["sli"]["total"].replace("{{window}}", slo["window"]))
    actual = (good / total) if good is not None and total else None
    remaining = budget_remaining(slo["objective"], actual) if actual is not None else None
    return SloResult(slo["service"], slo["name"], slo["objective"], actual, remaining)


def evaluate_trading_hours(slo: dict) -> SloResult:
    """TODO (you, ADR-0003): count only requests made while markets are open.

    The catalog has trading_hours (timezone, open, close, days). An instant query over a window can't
    exclude nights and weekends. Think about range queries with a step, or recording rules that
    multiply by a "market open" series, and about daylight-saving changes.
    """
    raise NotImplementedError("trading-hours SLOs: see the docstring")


def composite_availability(availabilities: list[float]) -> float:
    """TODO (you): the availability ceiling of a service that needs ALL of these dependencies.

    Write tests first: what should two 99.9% dependencies give? What assumptions does that formula make?
    """
    raise NotImplementedError


def attribute(incidents: list[dict], catalog: dict[str, dict]) -> dict[str, dict]:
    """TODO (you, ADR-0004): for each service, how much impact came from its own faults vs its dependencies?

    Inputs: project 12 incident records (services_impacted, root_cause_service, timeline)
    and the catalog's depends_on.
    Output shape is your choice; the report needs it per service.
    """
    raise NotImplementedError
