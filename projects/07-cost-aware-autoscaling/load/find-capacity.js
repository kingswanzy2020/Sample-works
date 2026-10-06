// Step load against ONE pod (scale to 1 replica, HPA off) to find req/s per pod before latency degrades.
// That number is your scaling target (KEDA threshold) and the basis of the cost model.
import http from "k6/http";

export const options = {
  scenarios: {
    steps: {
      executor: "ramping-arrival-rate",
      startRate: 5,
      timeUnit: "1s",
      preAllocatedVUs: 100,
      stages: [
        { target: 10, duration: "1m" },
        { target: 20, duration: "1m" },
        { target: 40, duration: "1m" },
        { target: 80, duration: "1m" },
        { target: 160, duration: "1m" },
      ],
    },
  },
};
const BASE = __ENV.BASE_URL || "http://localhost:8080";
export default function () {
  http.get(`${BASE}/work?ms=${__ENV.WORK_MS || 20}`);
}
