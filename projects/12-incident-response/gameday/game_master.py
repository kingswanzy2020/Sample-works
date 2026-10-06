"""Runs a game-day scenario against the landscape simulator, without telling responders what it is.

  python game_master.py list                 # ids only (safe to show responders)
  python game_master.py run [--id ID] [--delay-max 300]
  python game_master.py clear                # end the exercise
  python game_master.py reveal               # after the exercise: what was injected, and when

The injection log (gameday/.injections.jsonl) is the ground truth to compare against
the responders' incident timeline: time to detect, time to diagnose, wrong turns.
"""
import argparse
import json
import pathlib
import random
import sys
import time
import urllib.request

import yaml

HERE = pathlib.Path(__file__).parent
LOG = HERE / ".injections.jsonl"
SIM = "http://localhost:9200"


def call(path, body=None):
    req = urllib.request.Request(SIM + path, data=json.dumps(body or {}).encode(), method="POST",
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as r:
        return json.load(r)


def record(event):
    event["ts"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with LOG.open("a") as f:
        f.write(json.dumps(event) + "\n")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["list", "run", "clear", "reveal"])
    p.add_argument("--id")
    p.add_argument("--delay-max", type=int, default=300, help="random wait before the first fault (seconds)")
    a = p.parse_args()
    scenarios = {s["id"]: s for s in yaml.safe_load((HERE / "scenarios.yaml").read_text())["scenarios"]}

    if a.cmd == "list":
        print("\n".join(scenarios))
    elif a.cmd == "clear":
        call("/clear")
        record({"event": "clear"})
        print("cleared")
    elif a.cmd == "reveal":
        print(LOG.read_text() if LOG.exists() else "no injections recorded")
    else:
        s = scenarios[a.id] if a.id else random.choice(list(scenarios.values()))
        wait = random.randint(0, a.delay_max)
        print(f"scenario chosen; first fault in ≤ {a.delay_max}s. Responders: watch your alerts.", flush=True)
        time.sleep(wait)
        start = time.time()
        for step in s["steps"]:
            time.sleep(max(0, step["after_s"] - (time.time() - start)))
            if step.get("clear"):
                call("/clear")
            else:
                call("/fault", step["fault"])
            record({"event": "inject", "scenario": s["id"], "step": step})
        print("all steps injected; run `clear` when the exercise ends", flush=True)


if __name__ == "__main__":
    sys.exit(main())
