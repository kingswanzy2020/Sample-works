"""Sample service used by every project in this repo.

Deliberately small: a JSON API backed by Postgres, with the endpoints that
deployment, observability and scaling work all need (health, readiness,
metrics, a slow endpoint, and a version stamp).
"""
import asyncio
import os
import random
import time
from contextlib import asynccontextmanager

import psycopg
from fastapi import FastAPI, HTTPException, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from pydantic import BaseModel

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://app:app@localhost:5432/app")
# If set, the URL is re-read from this file on every connection, so rotated
# credentials (e.g. rendered by Vault Agent) are picked up without a restart.
DATABASE_URL_FILE = os.getenv("DATABASE_URL_FILE")
APP_VERSION = os.getenv("APP_VERSION", "dev")
# Failure injection knobs for the "break it" exercises.
INJECT_LATENCY_MS = int(os.getenv("INJECT_LATENCY_MS", "0"))
INJECT_ERROR_RATE = float(os.getenv("INJECT_ERROR_RATE", "0"))

REQUESTS = Counter("http_requests_total", "HTTP requests", ["route", "method", "status"])
LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["route", "method"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5),
)

state = {"ready": False}


@asynccontextmanager
async def lifespan(_app: FastAPI):
    state["ready"] = True
    yield
    # Fail readiness first so the load balancer drains us before we exit.
    state["ready"] = False


app = FastAPI(title="sample-service", version=APP_VERSION, lifespan=lifespan)


class ItemIn(BaseModel):
    name: str


def database_url() -> str:
    if DATABASE_URL_FILE:
        with open(DATABASE_URL_FILE) as f:
            return f.read().strip()
    return DATABASE_URL


def db():
    return psycopg.connect(database_url(), connect_timeout=2)


@app.middleware("http")
async def instrument(request, call_next):
    path = request.url.path
    start = time.perf_counter()
    status = 500
    try:
        if INJECT_LATENCY_MS and path.startswith("/items"):
            await asyncio.sleep(INJECT_LATENCY_MS / 1000)
        if INJECT_ERROR_RATE and path.startswith("/items") and random.random() < INJECT_ERROR_RATE:
            status = 503
            return Response(status_code=503, content="injected failure")
        response = await call_next(request)
        status = response.status_code
        return response
    finally:
        # Use the route template, not the raw path, to keep label cardinality bounded.
        route = request.scope.get("route")
        path = route.path if route else "unmatched"
        REQUESTS.labels(path, request.method, str(status)).inc()
        LATENCY.labels(path, request.method).observe(time.perf_counter() - start)


@app.get("/healthz")
def healthz():
    """Liveness: the process is up. Never checks dependencies."""
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    """Readiness: can this instance serve traffic right now?"""
    if not state["ready"]:
        raise HTTPException(503, "shutting down")
    try:
        with db() as conn:
            conn.execute("SELECT 1")
    except (psycopg.Error, OSError) as exc:
        raise HTTPException(503, f"database unavailable: {exc.__class__.__name__}") from exc
    return {"status": "ready"}


@app.get("/version")
def version():
    return {"version": APP_VERSION}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/items")
def list_items():
    with db() as conn:
        rows = conn.execute("SELECT id, name FROM items ORDER BY id LIMIT 100").fetchall()
    return [{"id": r[0], "name": r[1]} for r in rows]


@app.post("/items", status_code=201)
def create_item(item: ItemIn):
    with db() as conn:
        row = conn.execute(
            "INSERT INTO items (name) VALUES (%s) RETURNING id", (item.name,)
        ).fetchone()
    return {"id": row[0], "name": item.name}


@app.get("/work")
def work(ms: int = 100):
    """CPU-bound endpoint for load and autoscaling tests."""
    deadline = time.perf_counter() + min(ms, 5000) / 1000
    n = 0
    while time.perf_counter() < deadline:
        n += 1
    return {"iterations": n}
