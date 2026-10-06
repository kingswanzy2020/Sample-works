// Quiet → sudden spike → quiet. Measures how fast you scale up, what users feel meanwhile,
// and how long you keep paying for capacity after the spike (scale-down lag).
import http from "k6/http";

export const options = {
  scenarios: {
    spike: {
      executor: "ramping-arrival-rate",
      startRate: 5,
      timeUnit: "1s",
      preAllocatedVUs: 200,
      stages: [
        { target: 5, duration: "2m" },
        { target: 150, duration: "20s" },
        { target: 150, duration: "4m" },
        { target: 5, duration: "20s" },
        { target: 5, duration: "8m" },
      ],
    },
  },
  thresholds: { http_req_failed: ["rate<0.01"], http_req_duration: ["p(95)<500"] },
};
const BASE = __ENV.BASE_URL || "http://localhost:8080";
export default function () {
  http.get(`${BASE}/work?ms=${__ENV.WORK_MS || 20}`);
}
