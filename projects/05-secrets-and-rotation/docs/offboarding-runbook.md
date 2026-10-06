# Offboarding runbook (draft: fill in and time it)

When an engineer with production access leaves:

| Step | System | Action | Owner | Time taken |
|------|--------|--------|-------|------------|
| 1 | Identity provider | Disable account (cascades to SSO apps) | | |
| 2 | GitHub | Remove from org; review deploy keys and PATs they created | | |
| 3 | Cloud | Confirm no IAM users/keys belong to them | | |
| 4 | Vault | Revoke their tokens and leases (`vault token revoke -accessor ...`) | | |
| 5 | SOPS | Remove their age key from `.sops.yaml`, `sops updatekeys`, **and rotate every secret they could decrypt** | | |
| 6 | Static secrets | Rotate any shared secret they ever saw | | |

**Total time:** ___. What would make it faster?
