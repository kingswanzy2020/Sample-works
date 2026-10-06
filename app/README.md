# sample-service

The shared workload for every project. It is intentionally boring so the
interesting part is the infrastructure around it.

| Endpoint        | Purpose                                                       |
|-----------------|---------------------------------------------------------------|
| `GET /healthz`  | Liveness. Process is up. Never checks dependencies.           |
| `GET /readyz`   | Readiness. Checks the database; fails during shutdown.        |
| `GET /metrics`  | Prometheus metrics (request count, latency histogram).        |
| `GET /version`  | Returns `APP_VERSION`, so you can see which version served you. |
| `GET/POST /items` | Postgres-backed CRUD.                                       |
| `GET /work?ms=N` | Burns CPU for N ms. Used for load and autoscaling tests.    |

## Failure injection

| Env var             | Effect                                         |
|---------------------|------------------------------------------------|
| `INJECT_LATENCY_MS` | Adds latency to `/items*`                      |
| `INJECT_ERROR_RATE` | Fraction (0–1) of `/items*` requests that 503  |
| `DATABASE_URL_FILE` | Read the DB URL from this file on every connection (rotation without restart) |

## Run locally

```bash
docker compose up --build
curl localhost:8000/readyz
curl -X POST localhost:8000/items -H 'content-type: application/json' -d '{"name":"first"}'
```

## Test

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements-dev.txt
pytest
```
