# Migrations (Alembic)

Tasks
- Create revision: `task db:revision MSG="create users table"` (add `AUTOGEN=true` if enabled)
- Upgrade to head: `task db:upgrade`
- Downgrade one step: `task db:downgrade` (or `TARGET=-2`)
- Current revision: `task db:current`
- Heads/history: `task db:heads` / `task db:history`
- Stamp revision: `task db:stamp REV=head`

Config
- Alembic config lives at `alembic/alembic.ini`.
- Runtime DB URL comes from app settings or `DATABASE_URL`.
