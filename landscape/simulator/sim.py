"""Fake fleet: emits Prometheus metrics for every service in catalog.yaml.

Each service serves synthetic traffic. Failures propagate along `depends_on`:
if kafka degrades, price-feed, order-gateway and positions-api degrade too.
That's what makes correlation (project 14) and attribution (project 16) real problems.

Control it at runtime:
  curl -XPOST localhost:9200/fault -d '{"service":"kafka","error_rate":0.3,"latency_ms":200}'
  curl -XPOST localhost:9200/clear
  curl localhost:9200/state
  curl localhost:9200/probe/order-gateway   # black-box check of one service (200/500/503)
"""
import json
import os
import random
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import yaml
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest

CATALOG = os.getenv("CATALOG", "/catalog.yaml")
RPS = float(os.getenv("RPS_PER_SERVICE", "20"))
BASE_ERROR_RATE = float(os.getenv("BASE_ERROR_RATE", "0.001"))
PROPAGATION = float(os.getenv("PROPAGATION", "0.7"))  # share of a dependency's errors that leak upstream

REQUESTS = Counter("svc_requests_total", "Requests handled", ["service", "code"])
LATENCY = Histogram(
    "svc_request_duration_seconds", "Request latency", ["service"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5),
)
UP = Gauge("svc_up", "1 if the service process is up", ["service"])

with open(CATALOG) as f:
    services = {s["name"]: s for s in yaml.safe_load(f)["services"]}

faults: dict[str, dict] = {}
lock = threading.Lock()


def effective(service: str, seen=None) -> tuple[float, float]:
    """Error rate and added latency for a service, including what leaks from dependencies."""
    seen = seen or set()
    if service in seen:
        return 0.0, 0.0
    seen.add(service)
    f = faults.get(service, {})
    if f.get("down"):
        return 1.0, 0.0  # a dead dependency fails every call that reaches it
    err, lat = BASE_ERROR_RATE + f.get("error_rate", 0.0), f.get("latency_ms", 0.0)
    for dep in services[service].get("depends_on", []):
        d_err, d_lat = effective(dep, seen)
        err += d_err * PROPAGATION
        lat += d_lat
    return min(err, 1.0), lat


def traffic_loop():
    tick = 0.1
    while True:
        with lock:
            for name in services:
                down = faults.get(name, {}).get("down", False)
                UP.labels(name).set(0 if down else 1)
                if down:
                    continue
                err, extra_ms = effective(name)
                for _ in range(max(1, int(random.gauss(RPS * tick, 1)))):
                    code = "500" if random.random() < err else "200"
                    REQUESTS.labels(name, code).inc()
                    LATENCY.labels(name).observe(max(0.001, random.gauss(0.02, 0.005) + extra_ms / 1000))
        time.sleep(tick)


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/metrics":
            self._send(200, generate_latest(), CONTENT_TYPE_LATEST)
        elif self.path.startswith("/probe/"):
            # A black-box view of one service: what a synthetic check (project 15) would see.
            name = self.path.removeprefix("/probe/")
            if name not in services:
                return self._send(404, {"error": "unknown service"})
            with lock:
                down = faults.get(name, {}).get("down", False)
                err, extra_ms = effective(name)
            if down:
                return self._send(503, {"service": name, "ok": False})
            time.sleep(min(extra_ms, 5000) / 1000)
            ok = random.random() >= err
            self._send(200 if ok else 500, {"service": name, "ok": ok})
        elif self.path == "/state":
            with lock:
                self._send(200, {s: {"fault": faults.get(s, {}), "effective_error_rate": round(effective(s)[0], 4)}
                                 for s in services})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0)) or 0) or b"{}")
        with lock:
            if self.path == "/fault":
                if body.get("service") not in services:
                    return self._send(400, {"error": f"unknown service, choose from {sorted(services)}"})
                faults[body["service"]] = {k: v for k, v in body.items() if k != "service"}
            elif self.path == "/clear":
                faults.clear()
            else:
                return self._send(404, {"error": "not found"})
        self._send(200, {"faults": faults})

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    threading.Thread(target=traffic_loop, daemon=True).start()
    ThreadingHTTPServer(("0.0.0.0", 9200), Handler).serve_forever()
