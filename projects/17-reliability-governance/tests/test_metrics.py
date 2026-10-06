from governance import metrics


def test_ownership_gaps_flags_missing_owner_and_oncall():
    catalog = {
        "ok": {"owner": "team-a", "oncall": "a-primary", "tier": 1},
        "orphan": {"owner": "", "oncall": "", "tier": 1},
        "no-oncall": {"owner": "team-b", "oncall": "", "tier": 3},
    }
    findings = {f["service"]: f for f in metrics.ownership_gaps(catalog)}
    assert set(findings) == {"orphan", "no-oncall"}
    assert findings["orphan"]["value"] == 2


# TODO (you): tests for every metric you define, using small hand-written inputs
# where you know the right answer.
