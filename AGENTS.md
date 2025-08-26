# Repository Guidelines

## Project Structure & Module Organization
- Source: `app/` (FastAPI app). Submodules: `api/` (endpoints), `core/` (config, security, scheduler), `db/` (session, models, CRUD), `ingestion/` (fetchers, cleaning, pipeline), `rag/` (vector store, retrieval, summarize), `services/` (domain logic). Entry: `app/main.py`.
- Scripts: `scripts/` (e.g., `init_db.py`).
- Config: `.env.example` for env vars; `docker-compose.yml` for Postgres and Redis.
- Docs: `docs/index.md` (serve with `uvx mkdocs serve -f docs/mkdocs.yml -a 127.0.0.1:8001`). Key pages:
  - Architecture: `docs/architecture/overview.md`
  - API: `docs/api/design.md`
  - Data model: `docs/data-model/overview.md`
  - Pipelines: `docs/ingestion/pipelines.md`
  - Chroma: `docs/rag/chroma.md`
  - Feedback: `docs/product/feedback-loop.md`

## Build, Test, and Development Commands
- Setup: `task setup` — env, infra, deps, DB init.
- Run API: `task run` — dev server at `:8000`.
- Infra: `task up` / `task down` — start/stop services.
- Install: `task install` (or `task install:dev` for dev tools).
- Tests: `task test` (optionally with `-k` via `uv run pytest -k ...`).
- Lint/Format: `task lint` / `task format`.
- Type check: `task typecheck`.
- Pre-commit: `task precommit:install` then `task precommit:run`.
 - Alembic: `task db:revision MSG="..."`, `task db:upgrade`, `task db:downgrade TARGET=-1`, `task db:current`.
- Smoke test: `curl http://localhost:8000/` — expect `{ "ok": true }`.

## Coding Style & Naming Conventions
- Python: PEP 8, 4-space indents, type hints required on public functions.
- Modules: group by concern (`api`, `services`, `rag`, `ingestion`, `db`, `core`).
- Files: endpoint modules in `app/api/*.py` mirror route domain (e.g., `sources.py`, `digest.py`).
- Imports: absolute from `app.*`; avoid circular deps by keeping logic in `services/`.

## Testing Guidelines
- Framework: pytest (add `pytest` as a dev dependency). Place tests under `tests/` mirroring `app/` structure.
- Naming: files `test_*.py`; functions `test_*`.
- Running: `pytest -q` (optionally with `-k` to filter). Target high-value services and `core` utilities first.

## Commit & Pull Request Guidelines
- Commits: imperative mood, concise subject (≤72 chars), optional scope: `core: add JWT helpers`.
- PRs: clear description of intent, linked issues, steps to validate (curl/HTTPX examples), and notes on migrations/config changes. Add screenshots for user-visible API examples when applicable.

## Security & Configuration Tips
- Secrets: never commit `.env`; use `.env.example` for new keys. Rotate `JWT_SECRET` in production.
- Data: default URLs point to local Docker services; parameterize via env for other environments.
