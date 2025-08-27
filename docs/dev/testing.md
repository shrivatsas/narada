# Testing & Tooling

Pytest
- Default config in `pyproject.toml` under `[tool.pytest.ini_options]`.
- Run: `task test` or `uv run pytest -k "pattern"`.

Type checking
- `task typecheck` (mypy), config in `.pre-commit/mypy.ini`.

Lint/format
- `task lint` / `task format` (ruff), config in `.pre-commit/ruff.toml`.

Pre-commit
- Install: `task precommit:install`
- Run: `task precommit:run`

Security audit
- pip-audit runs as a pre-commit hook to flag vulnerable dependencies.
