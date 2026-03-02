# Installation (UV Project Already Set Up)

Prerequisites:
- Existing UV-managed Python project
- A working `codex` CLI installation

What you'll learn:
- How to add the SDK dependency with `uv`
- How to verify import and CLI availability
- How to avoid the most common setup mistakes

## 1) Add The SDK

```bash
uv add codex-sdk-unofficial
```

## 2) Verify Python Import

```bash
uv run python -c "from codex_sdk import Codex, __version__; print(__version__)"
```

Expected output:
- Prints a version like `0.1.2`

## 3) Verify `codex` CLI Is Reachable

```bash
uv run python -c "import shutil; print(shutil.which('codex'))"
```

Expected output:
- A non-empty path to the executable

If you get `None`:
- Install Codex CLI
- Ensure it is on `PATH`
- Or pass `codex_path_override` in `CodexOptions`

If you are not already in a UV project, follow the official UV setup docs first:
- [UV Getting Started](https://docs.astral.sh/uv/getting-started/)

## First Run Sanity Check

```python
from codex_sdk import Codex

thread = Codex().start_thread()
result = thread.run("Say hello and explain what you can do.")
print(result.final_response)
```

Run:

```bash
uv run python sanity_check.py
```

Failure modes:
- `Unable to locate codex executable`: CLI not found
- Non-zero subprocess exit with stderr: CLI/runtime configuration issue
