from fastapi.testclient import TestClient

from src.main import app


def test_healthz_does_not_need_database():
    with TestClient(app) as client:
        assert client.get("/healthz").json() == {"status": "ok"}


def test_version_endpoint():
    with TestClient(app) as client:
        assert "version" in client.get("/version").json()


def test_metrics_exposed():
    with TestClient(app) as client:
        client.get("/healthz")
        body = client.get("/metrics").text
        assert "http_requests_total" in body


def test_database_url_file_is_reread(tmp_path, monkeypatch):
    from src import main

    secret = tmp_path / "database_url"
    secret.write_text("postgresql://a:1@db/app\n")
    monkeypatch.setattr(main, "DATABASE_URL_FILE", str(secret))
    assert main.database_url() == "postgresql://a:1@db/app"
    secret.write_text("postgresql://b:2@db/app\n")
    assert main.database_url() == "postgresql://b:2@db/app"
