# Expand / contract: renaming `items.name` to `items.title` with zero downtime

During a rolling deploy, **old and new code run at the same time** against the **same database**.
So every schema change must be compatible with both versions alive at that moment.

| Step | Migration | App version deployed | Old code works? | New code works? |
|------|-----------|----------------------|-----------------|-----------------|
| 1. Expand | `002_expand_add_title.sql`: add nullable `title`, trigger to keep both in sync | v1 still running | ✅ writes `name`, trigger copies | n/a |
| 2. Migrate code | none | v2: reads `title`, writes **both** | ✅ | ✅ |
| 3. Backfill | `003_backfill_title.sql` | v2 | ✅ | ✅ |
| 4. Switch | none | v3: reads/writes `title` only | ❌ v2 must be fully gone first | ✅ |
| 5. Contract | `004_contract_drop_name.sql` | v3 | n/a | ✅ |

The **wrong** way, which break-it experiment 1 asks you to try: one migration that renames the column
plus one deploy. Old pods throw `column "name" does not exist` until the rollout finishes.

Copy each file into `app/migrations/` **one step at a time**. Each step is a separate deploy.
