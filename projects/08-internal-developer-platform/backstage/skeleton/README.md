# ${{ values.name }}

${{ values.description }}

Owned by **${{ values.owner }}**. Created from the paved-road template, so CI, image signing,
deploy manifests, probes and metrics are already wired. See `docs/adr/` for decisions.

| You get for free | Where |
|------------------|-------|
| CI (lint, test, build, scan, SBOM, sign) | `.github/workflows/ci.yml` → org reusable workflow |
| Kubernetes manifests with probes, requests, PDB | `k8s/` |
| `/healthz`, `/readyz`, `/metrics` | `src/main.py` |
| Catalog entry and ownership | `catalog-info.yaml` |
