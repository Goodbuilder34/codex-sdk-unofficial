# codex-sdk-unofficial

Unofficial, community-maintained Python SDK for the Codex CLI.

> This is **not an official OpenAI SDK**.

## Documentation

Full docs site (UV-first, beginner-first):
- https://goodbuilder34.github.io/codex-sdk-unofficial/

Local docs preview:

```bash
uv run --group docs mkdocs serve
```

## Quickstart (UV-First)

```bash
uv init codex-sdk-app
cd codex-sdk-app
uv venv
source .venv/bin/activate
uv add codex-sdk-unofficial
uv run python -c "from codex_sdk import Codex; print('import-ok')"
```

```python
from codex_sdk import Codex

codex = Codex()
thread = codex.start_thread()
turn = thread.run("Diagnose the test failure and propose a fix")

print(turn.final_response)
print(turn.items)
```

Run:

```bash
uv run python your_script.py
```

## Package Info

- Package name: `codex-sdk-unofficial`
- Import name: `codex_sdk`
- Current version: `0.1.2`

## Dev Commands

```bash
PYTHONPATH=src uv run pytest -q
uv run --group docs mkdocs build --strict
uv run --with build python -m build
```

## Publishing

Tag pushes (`v*`) trigger `.github/workflows/publish.yml`.

Manual upload fallback:

```bash
uv run --with twine twine upload dist/*
```
