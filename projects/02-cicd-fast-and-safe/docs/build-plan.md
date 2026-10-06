# Build plan: Project 02, fast and safe CI/CD

A **guide for when you're stuck**, not a walkthrough. Each task says *what* to achieve and how
you'll know it's done, never *how*. Open hints one level at a time, only after a real attempt (20–30 min):
**Hint 1** a nudge, **Hint 2** the concept or tool, **Hint 3** the docs.

**Decisions:** tasks work with any option you choose. **"Depends on your ADR"** notes say what to think about, not what to type.

**Rough time:** 12–20 hours. **Cost:** free on a public repo.

---

## Phase 0: Setup

### Task 0.1: Repo and tools
**Goal:** this project in its own **public** GitHub repo, with Docker (with buildx) and Python 3.12 locally.
**Done when:** the repo is pushed and you can build `app/` locally.

<details><summary>Hint 1</summary>Why does public vs private matter for this project? Think about Actions minutes and image visibility.</details>

---

## Phase 1: Measure the "before"

### Task 1.1: A deliberately naive pipeline
**Goal:** a workflow that does everything, every time, with no caching, no filters and no parallelism: lint, test, build, scan.
**Done when:** it runs green, and you have **5 timed runs** in `docs/ci-metrics.md`, broken down by stage.

<details><summary>Hint 1</summary>Temporarily move the starter <code>ci.yml</code> out of <code>.github/workflows/</code> so it doesn't run alongside yours.</details>
<details><summary>Hint 2</summary>You can re-run a workflow without pushing a new commit. Each job's step timings are shown in the run UI.</details>
<details><summary>Hint 3</summary>For exact numbers, the GitHub REST API lists jobs and their start/finish times for a run: https://docs.github.com/rest/actions/workflow-jobs</details>

### Task 1.2: Where does the time go?
**Goal:** a sentence per stage on *why* it takes as long as it does.
**Done when:** you can name the single biggest time cost, and say whether it's waiting, downloading or computing.

---

## Phase 2: Decide

### Task 2.1: ADR-0001 (what runs per change) and ADR-0002 (caching)
**Goal:** both accepted, using your Phase 1 numbers as context.
**Done when:** each ADR cites at least one number from `ci-metrics.md`.

<details><summary>Hint 1</summary>For caching: what is the cache <em>key</em>, and which change <em>should</em> invalidate it but might not?</details>

---

## Phase 3: Build

### Task 3.1: Switch to the starter pipeline and make it yours
**Goal:** the starter `ci.yml` runs, adjusted to your ADR-0001 and ADR-0002.
**Done when:** a PR touching `app/` runs lint → test → build → scan, and a PR touching only docs skips the expensive jobs.

> **Depends on your ADR-0001:** "run everything" means removing something from the starter. "Path filters" means checking the filter covers every file that can break the app. "Build-graph tooling" is a large detour, so scope it honestly in the ADR.
>
> **Depends on your ADR-0002:** the GitHub Actions cache, a registry-backed cache and no cache each change one line of the build step. Find out what the alternatives are called in the build-push action's docs.

<details><summary>Hint 1</summary>Read the <code>ci-ok</code> job. Why does it exist, and what goes wrong without it when jobs are skipped?</details>
<details><summary>Hint 3</summary>https://docs.docker.com/build/ci/github-actions/cache/</details>

### Task 3.2: Branch protection
**Goal:** `main` can't be merged into unless CI passes.
**Done when:** a PR with a failing test is blocked, and a docs-only PR can still merge.

<details><summary>Hint 1</summary>Which single check should be "required" so that skipped jobs don't block merges forever?</details>
<details><summary>Hint 2</summary>Settings → Branches (or Rulesets) → required status checks.</details>

### Task 3.3: Signed images on `main`
**Goal:** a push to `main` publishes an image to GHCR, signed with keyless cosign.
**Done when:** you verify the signature **from your laptop**, and can explain what identity the signature proves.

<details><summary>Hint 1</summary>Verification needs two things besides the image: <em>who</em> signed it (an identity) and <em>who vouched for that identity</em> (an issuer).</details>
<details><summary>Hint 2</summary>The identity of a keyless GitHub signature is the workflow file path plus the ref. Look at the certificate with <code>cosign verify ... | jq</code> once it works with a loose regexp, then tighten the regexp.</details>
<details><summary>Hint 3</summary>https://docs.sigstore.dev/cosign/verifying/verify/</details>

### Task 3.4: SBOM you can actually find
**Goal:** every `main` build leaves an SBOM someone can download or query later.
**Done when:** you can get the SBOM for a given image digest *without* re-running the build.

<details><summary>Hint 1</summary>The starter generates an SBOM file, then does nothing with it. Where should it go?</details>
<details><summary>Hint 2</summary>Two common answers: a workflow artifact, or an attestation attached to the image in the registry. They have different lifetimes. Which one do you need?</details>

### Task 3.5: Promote by digest
**Goal:** a tested digest is promoted to `staging`, then `prod` (with approval), with no rebuild.
**Done when:** the `prod` tag points at the **same digest** that passed CI, and promoting an unsigned image fails.

<details><summary>Hint 1</summary>Where will you find the digest of a build? Could CI make it easier to find?</details>
<details><summary>Hint 2</summary>The job summary (<code>$GITHUB_STEP_SUMMARY</code>) is a handy place to print it. GitHub environments can require a reviewer.</details>

### Task 3.6: Dependency updates
**Goal:** Dependabot opens update PRs, grouped sensibly.
**Done when:** at least one Dependabot PR has gone through your CI.

---

## Phase 4: Verify and measure the "after"

**Goal:** `docs/ci-metrics.md` filled in for every configuration, plus the "cost of the speed" table.
**Done when:** you have a before/after chart, and each speed-up has a stated new risk next to it.

<details><summary>Hint 1</summary>Use the median of 5 runs. Cold-cache and warm-cache runs differ a lot, so measure and label both.</details>

---

## Phase 5: Break

**Goal:** every experiment in `docs/break-it.md`, each with a postmortem.

<details><summary>Exp 1: stale cache</summary>Think about which Dockerfile layer is reused, and what that layer contains. The cache key is about inputs to the step, not about what your code imports.</details>
<details><summary>Exp 2: CVE gate</summary>Search an advisory database (e.g. OSV, GitHub Advisory) for an old version of a common library with a <em>fixed</em> critical issue.</details>
<details><summary>Exp 3: flaky test</summary>Same commit, different results. How would you detect that automatically rather than by noticing?</details>
<details><summary>Exp 4: escaped path filter</summary>Which files outside <code>app/</code> does the app or its build depend on?</details>

---

## Phase 6: Decide again, then improve

### Task 6.1: ADR-0003 to ADR-0006
**Goal:** all accepted, each citing a break-it result or a measurement.

> **Depends on your ADR-0004 (flaky tests):** retries, quarantine and fix-forward each need a mechanism *and* an owner. Write down who notices, and how.
>
> **Depends on your ADR-0006 (runners):** if you consider self-hosted, explain how a PR from a fork is kept away from your machine.

### Task 6.2: Safety nets for your speed-ups
**Goal:** something catches what your caching and filters might miss.
**Done when:** a scheduled job exists that would have caught experiments 1 and 4.

<details><summary>Hint 1</summary>A build that ignores the cache, and a run that ignores the filters, on a schedule.</details>

---

## Phase 7: Document

**Done when:**
- [ ] The interview story is filled in, with real numbers.
- [ ] `docs/scale.md` is in your words.
- [ ] You can answer: "How do you know the cache isn't lying?", "What does your signature prove, and what doesn't it prove?", "Why build once?"

---

## Stuck? Diagnose before you search

| Symptom | Ask yourself | Where to look |
|---------|--------------|---------------|
| Tests can't import `src` | Which directory does pytest run from, and what's on its path? | `pyproject.toml` `[tool.pytest.ini_options]` |
| Ruff fails on import order | Is this a real problem or formatting? | `ruff check --help` (there's a fix flag) |
| GHCR push `denied` | Does the job have permission to write packages? Is the package linked to this repo? | Job `permissions:`; package settings |
| Build fails only on PRs, mentioning attestations or exporters | What's different about a build that isn't pushed? | `build-push-action` `load` vs `push` |
| Trivy fails downloading its database | Rate limiting on the vulnerability DB? | Trivy docs on DB repository/caching |
| `cosign verify`: no matching signatures | Does your identity regexp match the actual certificate identity? | Loosen it, inspect the output, tighten it again |
| Required check "expected, waiting" forever | Is the required check one that can be skipped? | Branch protection settings vs `ci-ok` |
| Path filter never matches on `main` | What does the filter compare against on push vs PR? | `dorny/paths-filter` README |

**Still stuck?** Write down what you expected, what happened, and the exact error, then ask.
