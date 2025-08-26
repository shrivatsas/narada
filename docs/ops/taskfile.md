# Taskfile Reference

Install
- macOS: `brew install go-task`
- Linux: `curl -sL https://taskfile.dev/install.sh | sh`
- If `task` runs Taskwarrior, use `go-task` or alias `task=go-task`.

Common tasks
- Setup: `task setup` — env, infra, deps, DB init
- Run API: `task run` — dev server at `:8000`
- Infra: `task up` / `task down`
- Deps: `task install` / `task install:dev`
- Tests/Lint/Format/Types: `task test`, `task lint`, `task format`, `task typecheck`
- Pre-commit: `task precommit:install`, `task precommit:run`
- Lockfile: `task lock`
- Smoke test: `task smoke`

Docs
- Serve: `uvx mkdocs serve -f docs/mkdocs.yml -a 127.0.0.1:8001`
- Build: `uvx mkdocs build -f docs/mkdocs.yml -d site`
