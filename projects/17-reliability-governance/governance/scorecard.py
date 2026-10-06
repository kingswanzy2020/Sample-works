"""Run every metric and print findings grouped by owner. The format of the real scorecard is ADR-0002.

python -m governance.scorecard
"""

from __future__ import annotations

import datetime as dt
import sys
from collections import defaultdict

from governance import metrics, sources


def main() -> int:
    catalog = sources.catalog()
    runs = {
        "ownership_gaps": lambda: metrics.ownership_gaps(catalog),
        "alert_quality": lambda: metrics.alert_quality(sources.triage_log(), sources.feedback(), catalog),
        "runbook_quality": lambda: metrics.runbook_quality(sources.incidents(), catalog),
        "action_followthrough": lambda: metrics.action_followthrough(
            sources.incidents(), dt.date.today().isoformat()
        ),
    }
    by_owner: dict[str, list[dict]] = defaultdict(list)
    for name, run in runs.items():
        try:
            for f in run():
                by_owner[f["owner"]].append(f)
        except NotImplementedError:
            print(f"(metric {name} not implemented yet)")
    for owner, findings in sorted(by_owner.items()):
        print(f"\n## {owner}")
        for f in findings:
            print(f"- [{f['metric']}] {f['service']}: {f['detail']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
