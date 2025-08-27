Product shape (MVP → V1)

User stories
	•	As a customer, I connect sources (RBI circulars, blogs, docs, PDFs, RSS, sitemaps).
	•	I set my topic profile (include/exclude keywords, entities, geographies, sources).
	•	I get a Daily Digest at 9:00 IST with concise bullets + source links.
	•	I can ask ad-hoc questions any time and see an At-the-Moment Trendline.
	•	I can upvote/downvote individual summary bullets to tune future results.

Key choices
	•	LangChain for RAG pipelines & tasks.
	•	ChromaDB for vector store (per-tenant isolation via collections/metadata).
	•	FastAPI backend + Celery/Arq for jobs (daily digest; periodic indexing).
	•	Postgres for multi-tenant core data (users, orgs, votes, trend metrics).
	•	Redis for queues & short-lived trend counters.
	•	Playwright/Firecrawl/RSS connectors for ingestion (start with RSS/sitemaps; add crawlers later).
	•	Optional: add a small cross-encoder reranker (e.g., bge-reranker) after Chroma retrieval to boost quality.

UI: two simple views
	•	daily digest - 5–7 bullets, each shows favicon, title, date, source link, ↑/↓.small “why this” popover: tags, recency, similarity score, preference boost.
	•	at-the-moment - tag leaderboard + sparkline; click a tag → show example docs & ask follow-ups.

### Project Structure

```
discovery-bot/
  ├─ app/
  │  ├─ main.py
  │  ├─ api/
  │  │  ├─ auth.py
  │  │  ├─ sources.py
  │  │  ├─ query.py
  │  │  ├─ digest.py
  │  │  ├─ vote.py
  │  │  └─ trends.py
  │  ├─ core/
  │  │  ├─ config.py
  │  │  ├─ scheduler.py
  │  │  └─ security.py
  │  ├─ db/
  │  │  ├─ models.py
  │  │  ├─ session.py
  │  │  └─ crud.py
  │  ├─ ingestion/
  │  │  ├─ fetchers.py
  │  │  ├─ pipeline.py
  │  │  └─ text_clean.py
  │  ├─ rag/
  │  │  ├─ chroma_store.py
  │  │  ├─ retrieval.py
  │  │  └─ summarize.py
  │  └─ services/
  │     ├─ digest.py
  │     ├─ trends.py
  │     └─ feedback.py
  ├─ scripts/
  │  └─ init_db.py
  ├─ docs/
  │  ├─ index.md
  │  ├─ architecture/overview.md
  │  ├─ api/design.md
  │  ├─ data-model/overview.md
  │  ├─ ingestion/pipelines.md
  │  ├─ rag/chroma.md
  │  ├─ product/feedback-loop.md
  │  ├─ ops/migrations.md
  │  ├─ ops/taskfile.md
  │  └─ dev/
  ├─ pyproject.toml
  ├─ docker-compose.yml
  ├─ .env.example
  └─ README.md
```

### Quickstart

## Prereqs
- Python 3.11+
- Docker (for Postgres & Redis)
- Task runner: go-task (`task`). Install:
  - macOS: `brew install go-task`
  - Linux: `curl -sL https://taskfile.dev/install.sh | sh`
  - Note: If you have Taskwarrior (`task`) installed, use `go-task` or alias `task=go-task`.

## Run services
### One-time setup (env, Docker, deps, DB init)
task setup

### Run the API (dev server)
task run

### Add an RSS source
curl -X POST http://localhost:8000/sources -H 'Content-Type: application/json' \
  -d '{"type":"rss","url":"https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=RSS"}'

### Get a digest (builds one on the fly)
curl http://localhost:8000/digest/today

### Ask a query
curl -X POST http://localhost:8000/query -H 'Content-Type: application/json' -d '{"q":"AA-based lending updates"}'

### Development

- Install dev tools: `task install:dev`
- Run tests: `task test`
- Override tests: `uv run pytest -k "pattern"` (e.g., a module or test name)
- Lint: `task lint`
- Format: `task format`
- Type check: `task typecheck`
- Pre-commit install: `task precommit:install`
- Pre-commit run: `task precommit:run`
- Start/stop infra: `task up` / `task down`
- Generate lockfile: `task lock`

### Tooling

- pip-audit: dependency vulnerability scan via pre-commit (see `.pre-commit/.pre-commit-config.yaml`).
- structlog: structured JSON logs for production readiness.
- OpenTelemetry: tracing hooks (install `--extra observability`) for OTLP/Jaeger exporters.
- APScheduler: cron-style jobs for 09:00 IST digest and periodic crawls.

### Docs

- Browse docs: open `docs/index.md` or serve with `uvx mkdocs serve -f docs/mkdocs.yml -a 127.0.0.1:8001`
- Architecture: `docs/architecture/overview.md`
- API design: `docs/api/design.md`
- Data model: `docs/data-model/overview.md`
- Pipelines: `docs/ingestion/pipelines.md`
- Chroma design: `docs/rag/chroma.md`
- Feedback loop: `docs/product/feedback-loop.md`
- Ops: `docs/ops/taskfile.md`, `docs/ops/migrations.md`

### Migrations (Alembic)

- Create revision: `task db:revision MSG="create users table"` (add `AUTOGEN=true` to autogenerate if you later enable it)
- Upgrade to head: `task db:upgrade`
- Downgrade one step: `task db:downgrade` (or `task db:downgrade TARGET=-2`)
- Current revision: `task db:current`
- Heads/history: `task db:heads` / `task db:history`
- Stamp revision: `task db:stamp REV=head`

### Troubleshooting

- Postgres port in use: set `POSTGRES_PORT=5433` in `.env`, update `DATABASE_URL` to use `:5433`, then `task down && task up`.
- Redis port in use: set `REDIS_PORT=6380` in `.env`, update `REDIS_URL` to use `:6380`.
- Auth failed for user: ensure the password in `DATABASE_URL` matches `POSTGRES_PASSWORD` used to create the DB. Our `.env.example` uses `app`/`app` for both to avoid mismatches.
- If the DB was initialized with a different password, either:
  - Reset dev DB (destructive): `go-task db:reset` then `go-task up && go-task db:wait && go-task db:init`.
  - Or update the password in-place: `docker-compose exec db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "ALTER USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';"`
