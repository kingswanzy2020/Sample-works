# Break-it experiments

Write the hypothesis first. Afterwards, add a postmortem in [`postmortems/`](postmortems/).

### Experiment 1: Cache poisoning / stale cache
- **Hypothesis:** If a cached layer contains a dependency that is no longer in `requirements.txt`, CI still passes because ___.
- **Procedure:**
  1. Add a `RUN pip install requests` line to the Dockerfile, push, and let it cache.
  2. Remove it from the Dockerfile but import `requests` in `app/src/main.py`. Does CI catch it? (Hint: think about which layer is reused.)
  3. Separately, change only a comment in `requirements.txt`. Does the pip cache bust? Should it?
- **Measure:** whether CI caught the missing dependency; whether the weekly no-cache build would have.
- **Result:**

### Experiment 2: Ship a known CVE
- **Hypothesis:** Pinning an old vulnerable package (e.g. an old `jinja2` or `urllib3`) makes the blocking scan fail.
- **Procedure:** Pin a version with a published CRITICAL CVE that has a fix. Then try a HIGH with no fix. Compare behaviour.
- **Measure:** which gate fired; what message a developer sees; how they'd fix it.
- **Result:**

### Experiment 3: A flaky test
- **Procedure:** Add `app/tests/test_flaky.py`:
  ```python
  import random
  def test_sometimes():
      assert random.random() > 0.2
  ```
  Run CI 10 times on the same commit. Then apply your ADR-0004 policy end to end.
- **Measure:** failure rate; how long until someone would notice in a real team.
- **Result:**

### Experiment 4: The "docs-only" change that isn't
- **Hypothesis:** A change to a file outside the path filter can break the app without CI noticing.
- **Procedure:** Move a config value the app reads into a root-level file not in the filter, then break it.
- **Measure:** did `ci-ok` pass? What safety net would catch it?
- **Result:**

### Experiment 5: Unsigned image promotion
- **Procedure:** Push an image manually (not from CI) and try to promote it with `promote.yml`.
- **Expected:** `cosign verify` refuses it. Confirm, and capture the error.
- **Result:**
