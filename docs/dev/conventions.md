# Coding Conventions

- Python 3.11+, PEP 8, 4-space indents.
- Type hints required on public functions.
- Modules grouped by concern: `api`, `services`, `rag`, `ingestion`, `db`, `core`.
- Avoid circular deps; keep domain logic in `services/`.
- Absolute imports from `app.*`.
