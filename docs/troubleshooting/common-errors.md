# Common Errors

## `Unable to locate \`codex\` executable`

Cause:
- CLI not installed or not on `PATH`

Fix:
- Install Codex CLI
- Verify path:

```bash
uv run python -c "import shutil; print(shutil.which('codex'))"
```

- Or set `codex_path_override`

## `Codex Exec exited with code ...`

Cause:
- CLI runtime failure

Fix:
- Inspect stderr in exception message
- Validate auth and CLI config
- Retry with minimal prompt

## `options must be ... mapping or None`

Cause:
- Incorrect options type

Fix:
- Pass dict or dataclass instances

## `signal must expose is_set()`

Cause:
- Invalid cancellation object

Fix:
- Use `threading.Event` or compatible object

## UV-specific: Wrong interpreter in `uv run`

Cause:
- Unexpected environment selection

Fix:
- Pin interpreter:

```bash
uv run --python 3.12 python -c "import sys; print(sys.version)"
```
