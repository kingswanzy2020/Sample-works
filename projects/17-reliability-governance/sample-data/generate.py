"""Generate 4 weeks of realistic governance input data.

This lets project 17 start before projects 12/14/16 have produced real data.

    python sample-data/generate.py            # writes sample-data/out/

The data has patterns planted in it (like a real organisation would). Finding them is the project.
Swap to real data by pointing the loaders at projects 12/14/15/16 (see governance/sources.py).
"""

import datetime as dt
import json
import pathlib
import random

import yaml

random.seed(17)
OUT = pathlib.Path(__file__).parent / "out"
START = dt.datetime(2026, 9, 7, 7, 0, tzinfo=dt.UTC)

ALERTS = [
    # (alertname, service, severity, weekly_volume, actionable_probability)
    ("HighErrorRate", "order-gateway", "page", 3, 0.9),
    ("HighErrorRate", "price-feed", "page", 4, 0.6),
    ("HighErrorRate", "risk-engine", "page", 2, 0.8),
    ("AnyErrors", "positions-api", "page", 40, 0.05),
    ("KafkaDegraded", "kafka", "page", 1, 1.0),
    ("ServiceDown", "reporting-batch", "page", 6, 0.1),
]


def main():
    (OUT / "incidents").mkdir(parents=True, exist_ok=True)
    triage, feedback = [], []
    for week in range(4):
        for name, svc, sev, volume, p_actionable in ALERTS:
            for i in range(random.randint(int(volume * 0.7), int(volume * 1.3) + 1)):
                t = START + dt.timedelta(days=week * 7 + random.uniform(0, 7))
                fp = f"{svc}-{name}-{week}-{i}"
                owner = {"risk-engine": None}.get(svc, "owned")
                triage.append(
                    {
                        "received_at": t.isoformat(),
                        "fingerprint": fp,
                        "alertname": name,
                        "status": "firing",
                        "service": svc,
                        "severity": sev,
                        "starts_at": t.isoformat(),
                        "routed_to": "unrouted" if owner is None else f"{svc}-oncall",
                    }
                )
                if random.random() < 0.7:  # not every alert gets feedback: a finding in itself
                    feedback.append(
                        {
                            "received_at": (t + dt.timedelta(minutes=20)).isoformat(),
                            "fingerprint": fp,
                            "actionable": random.random() < p_actionable,
                        }
                    )
    (OUT / "triage-log.jsonl").write_text("\n".join(json.dumps(r) for r in triage) + "\n")
    (OUT / "feedback.jsonl").write_text("\n".join(json.dumps(r) for r in feedback) + "\n")

    incidents = [
        (
            "2026-09-09-kafka-isr",
            "kafka",
            ["price-feed", "order-gateway"],
            2,
            "runbooks/kafka.md",
            True,
            [("team-platform", "2026-09-23", "done"), ("team-platform", "2026-09-30", "open")],
        ),
        (
            "2026-09-15-price-feed-stale",
            "price-feed",
            ["price-feed"],
            2,
            "runbooks/price-feed.md",
            False,
            [("team-marketdata", "2026-09-22", "open"), ("team-marketdata", "2026-09-29", "open")],
        ),
        (
            "2026-09-22-risk-engine-down",
            "risk-engine",
            ["risk-engine", "order-gateway"],
            1,
            "runbooks/risk-engine.md",
            False,
            [("", "2026-10-06", "open")],
        ),
        (
            "2026-09-29-price-feed-stale",
            "price-feed",
            ["price-feed"],
            2,
            "runbooks/price-feed.md",
            False,
            [("team-marketdata", "2026-10-13", "open")],
        ),
    ]
    for iid, cause, impacted, sev, runbook, helped, actions in incidents:
        day = dt.datetime.fromisoformat(iid[:10] + "T09:05:00+00:00")
        record = {
            "id": iid,
            "title": iid[11:].replace("-", " "),
            "severity": sev,
            "game_day": False,
            "services_impacted": impacted,
            "root_cause_service": cause,
            "timeline": {
                "started": day.isoformat(),
                "detected": (day + dt.timedelta(minutes=6)).isoformat(),
                "mitigated": (day + dt.timedelta(minutes=41)).isoformat(),
                "resolved": (day + dt.timedelta(minutes=70)).isoformat(),
            },
            "detection": "alert",
            "alerts_fired": [],
            "runbooks_used": [{"runbook": runbook, "helped": helped, "notes": ""}],
            "actions": [
                {"id": f"A{i + 1}", "description": "", "owner": o, "due": d, "status": s}
                for i, (o, d, s) in enumerate(actions)
            ],
        }
        (OUT / "incidents" / f"{iid}.yaml").write_text(yaml.safe_dump(record, sort_keys=False))
    print(f"wrote {len(triage)} alerts, {len(feedback)} feedback, {len(incidents)} incidents to {OUT}")


if __name__ == "__main__":
    main()
