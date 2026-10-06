// k6 run load/steady.js  : background traffic so SLIs have data.
import http from "k6/http";
import { sleep } from "k6";

export const options = { vus: 10, duration: __ENV.DURATION || "30m" };
const BASE = __ENV.BASE_URL || "http://localhost:8000";

export default function () {
  http.get(`${BASE}/items`);
  if (Math.random() < 0.1) {
    http.post(`${BASE}/items`, JSON.stringify({ name: "k6" }), { headers: { "content-type": "application/json" } });
  }
  sleep(0.2);
}
