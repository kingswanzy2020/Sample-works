# Project 02: A CI/CD pipeline that is fast *and* safe

> **Problem:** CI takes 25 minutes, so developers batch changes and merge less often.
> Flaky tests get re-run until green. Nobody knows what is inside the images we ship.

**Need help while building?** See [`docs/build-plan.md`](docs/build-plan.md): tasks with a goal and a "done when" check, hints hidden in levels (nudge → concept → docs), and a diagnosis table. It never gives you the full solution.

## Decisions this project proves you can make

1. **What runs on each change:** everything, or only what changed?
2. **Caching:** what to cache, and how you know the cache isn't giving wrong builds.
3. **Security gates:** which findings block a merge and which only warn.
4. **Flaky tests:** retry, quarantine, or fix, and who owns them.
5. **Build once, promote by digest** vs rebuild per environment.
6. **Runners:** GitHub-hosted vs self-hosted.

## Success criteria

- [ ] A **baseline** CI time is recorded *before* any optimization (see `docs/ci-metrics.md`).
- [ ] PR feedback (lint and tests) arrives in under 5 minutes, and you can say what it costs.
- [ ] Every image pushed from `main` has an SBOM, a vulnerability scan result and a signature.
- [ ] The same image digest that passed tests is the one deployed. No rebuilds.
- [ ] A written flaky-test policy that you actually applied once.

## Prerequisites and cost

- A GitHub repo (Actions minutes are free for public repos), Docker, Python 3.12.
- Uses GHCR for images, which is free for public images.
- Starts from `app/` (the shared sample service).

## Starter layout

```
.github/workflows/
  ci.yml         # change detection → lint → test → build → scan → SBOM → sign
  promote.yml    # promote an existing digest to an environment tag (no rebuild)
.github/dependabot.yml
pyproject.toml   # ruff + pytest config
docs/ci-metrics.md   # baseline vs after numbers: your evidence
docs/adr/  docs/break-it.md  docs/scale.md  docs/postmortems/
```

## Milestones

### Build
- [ ] **Before optimizing:** write the naive pipeline (no cache, everything every time) and record its duration ×5 runs in `docs/ci-metrics.md`.
- [ ] Switch to the starter `ci.yml`. Fill in ADR-0001 (what runs) and ADR-0002 (caching).
- [ ] Push to `main`, then verify the signature: `cosign verify ghcr.io/<you>/sample-service@<digest> --certificate-identity-regexp ... --certificate-oidc-issuer https://token.actions.githubusercontent.com`.

### Test
- [ ] Record the new timings. Where did the time go (setup, install, test, build, scan)?
- [ ] Prove change detection works: a docs-only PR should skip build and scan.

### Break
- [ ] Run [`docs/break-it.md`](docs/break-it.md): cache poisoning, CVE gate, flaky test, a "docs-only" change that isn't.

### Decide
- [ ] ADR-0003 (security gate policy), ADR-0004 (flaky tests), ADR-0005 (promotion), ADR-0006 (runners).

### Improve
- [ ] Add required status checks and branch protection on `main`.
- [ ] Add a weekly job that rebuilds without cache, so cache bugs surface on a schedule rather than in an incident.

### Document
- [ ] A before/after chart of CI duration.
- [ ] Interview story below.

## ADRs

| # | Decision | Status |
|---|----------|--------|
| [0001](docs/adr/0001-what-runs-on-each-change.md) | Path-filtered vs full pipeline | Proposed |
| [0002](docs/adr/0002-caching-strategy.md) | What to cache and how to trust it | Proposed |
| [0003](docs/adr/0003-security-gates.md) | Block vs warn on scan findings | Proposed |
| [0004](docs/adr/0004-flaky-test-policy.md) | Retry, quarantine or fix | Proposed |
| [0005](docs/adr/0005-build-once-promote-by-digest.md) | Promote digests vs rebuild per env | Proposed |
| [0006](docs/adr/0006-runners.md) | Hosted vs self-hosted runners | Proposed |

## Interview story

> "CI took ___ minutes. I measured where the time went: ___. I changed ___ and got it to ___,
> but that introduced ___ risk, so I added ___. A flaky test taught me ___."
