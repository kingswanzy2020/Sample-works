# ADR-0001: What runs on each change

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Every PR currently runs lint, test, image build and scans, even for a README typo.
Feedback is slow, so people stop waiting for it.

## Options considered

### Option 1: Run everything, always
- **Pros:** Nothing slips through. Simple to reason about.
- **Cons:** Slowest. Wastes minutes on docs-only changes.

### Option 2: Path filters (starter default) with an always-reporting aggregator job (`ci-ok`)
- **Pros:** Docs-only PRs finish in seconds. `ci-ok` keeps branch protection working when jobs are skipped.
- **Cons:** If the filter is wrong (a shared config outside `app/`), a breaking change skips tests.

### Option 3: Build-graph aware tooling (Nx, Bazel, Pants, Turborepo)
- **Pros:** Precise: only affected targets, with a remote cache.
- **Cons:** Heavy adoption cost; overkill for one service.

## Questions to answer before deciding

- Which files outside `app/` can break the app? Are they in the filter?
- Is there a safety net (nightly full run) for what filters miss?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence

docs/ci-metrics.md: docs-only PR timing; break-it experiment 4
