// k6 run load/during-deploy.js   (https://k6.io)
// Constant arrival rate, so a slow pod can't hide errors by lowering throughput.
import http from "k6/http";
import { check } from "k6";
import { Counter } from "k6/metrics";

const versions = new Counter("served_by_version");

export const options = {
  scenarios: {
    steady: {
      executor: "constant-arrival-rate",
      rate: 50,
      timeUnit: "1s",
      duration: __ENV.DURATION || "3m",
      preAllocatedVUs: 50,
    },
  },
  thresholds: {
    // Define "zero downtime" precisely. Write your definition in ADR-0003.
    http_req_failed: ["rate==0"],
    http_req_duration: ["p(99)<500"],
  },
};

const BASE = __ENV.BASE_URL || "http://localhost:8080";

export default function () {
  const res = http.get(`${BASE}/items`);
  check(res, { "status is 200": (r) => r.status === 200 });
  const v = http.get(`${BASE}/version`);
  if (v.status === 200) versions.add(1, { version: v.json("version") });
}
