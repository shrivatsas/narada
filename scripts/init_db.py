from __future__ import annotations

import os
from typing import Any

from alembic import command  # type: ignore[attr-defined]
from alembic.config import Config
from sqlalchemy import text

from app.core.config import settings
from app.core.security import hash_password
from app.db.session import engine


def run_migrations() -> None:
    cfg_path = os.path.join(os.path.dirname(__file__), "..", "alembic", "alembic.ini")
    script_location = os.path.join(os.path.dirname(__file__), "..", "alembic")
    cfg = Config(cfg_path)
    cfg.set_main_option("script_location", script_location)
    cfg.set_main_option("sqlalchemy.url", settings.database_url)
    command.upgrade(cfg, "head")


def seed_demo_user() -> None:
    email = "demo@example.com"
    password = "demo"  # nosec B105: demo-only seed credential
    hpw = hash_password(password)
    with engine.begin() as conn:
        res: Any | None = conn.execute(
            text("SELECT id FROM users WHERE email = :email"), {"email": email}
        ).fetchone()
        if res is None:
            conn.execute(
                text(
                    "INSERT INTO users (email, password_hash, plan) VALUES (:email, :hpw, 'free')"
                ),
                {"email": email, "hpw": hpw},
            )
            print(f"Seeded demo user: {email} / {password}")
        else:
            print("Demo user already exists; skipping seed.")


def main() -> None:
    print("Running Alembic migrations...")
    run_migrations()
    print("Migrations complete.")
    print("Seeding demo data...")
    seed_demo_user()
    print("Done.")


if __name__ == "__main__":
    main()
