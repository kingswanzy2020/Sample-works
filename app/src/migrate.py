"""Minimal forward-only migration runner.

Applies migrations/NNN_*.sql in order and records them in schema_migrations.
Kept tiny on purpose so the expand/contract exercise in project 03 is visible.
"""
import os
import pathlib
import sys

import psycopg

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://app:app@localhost:5432/app")
MIGRATIONS_DIR = pathlib.Path(
    os.getenv("MIGRATIONS_DIR", pathlib.Path(__file__).parent.parent / "migrations")
)


def main() -> int:
    with psycopg.connect(DATABASE_URL, autocommit=True) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS schema_migrations "
            "(version text PRIMARY KEY, applied_at timestamptz DEFAULT now())"
        )
        applied = {r[0] for r in conn.execute("SELECT version FROM schema_migrations")}
        for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
            if path.stem in applied:
                continue
            print(f"applying {path.name}")
            with conn.transaction():
                conn.execute(path.read_text())
                conn.execute("INSERT INTO schema_migrations (version) VALUES (%s)", (path.stem,))
    return 0


if __name__ == "__main__":
    sys.exit(main())
