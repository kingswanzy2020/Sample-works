import json
import pathlib

from fastapi.testclient import TestClient

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "kafka-storm.json"


def client(tmp_path, monkeypatch):
    monkeypatch.setenv("TRIAGE_DATA", str(tmp_path))
    import importlib

    import triage.app
    importlib.reload(triage.app)
    return TestClient(triage.app.app)


def test_every_alert_is_recorded(tmp_path, monkeypatch):
    c = client(tmp_path, monkeypatch)
    r = c.post("/alerts", json=json.loads(FIXTURE.read_text()))
    assert r.status_code == 200
    lines = (tmp_path / "triage-log.jsonl").read_text().splitlines()
    assert len(lines) == 4
    services = {json.loads(line)["service"] for line in lines}
    assert services == {"kafka", "price-feed", "order-gateway", "positions-api"}


def test_feedback_is_stored(tmp_path, monkeypatch):
    c = client(tmp_path, monkeypatch)
    c.post("/feedback", json={"fingerprint": "a4", "actionable": False})
    assert "a4" in (tmp_path / "feedback.jsonl").read_text()

# TODO (you): tests for YOUR stages, e.g.
#   - the four alerts in kafka-storm.json end up in ONE group with kafka as the probable cause
#   - an alert for an unowned service is routed according to your ADR
#   - enrichment still records the alert when the catalog lookup fails
