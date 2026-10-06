# CI metrics: your evidence

Measure **before** you optimize, or the "25 → 6 minutes" story isn't credible.
Take 5 runs per configuration and report the median (one run is noise).

## Per-stage breakdown

| Configuration | Checkout+setup | Install deps | Lint | Test | Build | Scan | Total (median of 5) |
|---------------|----------------|--------------|------|------|-------|------|---------------------|
| Naive (no cache, everything) | | | | | | | |
| + pip cache | | | | | | | |
| + parallel lint/test | | | | | | | |
| + docker layer cache | | | | | | | |
| + path filters (docs-only PR) | | | | | | | |

## Cost of the speed

| Change | Time saved | New risk introduced | Mitigation |
|--------|-----------|---------------------|------------|
| Layer cache | | Stale or poisoned layers | Weekly no-cache build |
| Path filters | | A change outside the filter breaks the app | `ci-ok` aggregator + full nightly run |
