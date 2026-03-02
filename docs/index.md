# codex-sdk-unofficial Documentation

> `codex-sdk-unofficial` is a community-maintained project and is **not an official OpenAI SDK**.

This site is a full, ground-up guide for installing, understanding, and using the SDK with an **UV-first workflow**.

## Start Here In 5 Minutes

Prerequisites:
- Existing UV-managed Python project
- `codex` CLI available on your machine

What you'll do:
- Add the SDK dependency
- Install the package
- Run your first turn

```bash
uv add codex-sdk-unofficial
uv run python -c "from codex_sdk import Codex; print('import-ok')"
```

## The Exact Import

```python
from codex_sdk import Codex
```

## Quick First Script

```python
from codex_sdk import Codex

codex = Codex()
thread = codex.start_thread()
turn = thread.run("Diagnose the test failure and propose a fix")

print(turn.final_response)
print(turn.items)
print(turn.usage)
```

Run it:

```bash
uv run python your_script.py
```

Expected outcome:
- `turn.final_response` contains the latest assistant message text
- `turn.items` contains completed items emitted during the turn
- `turn.usage` contains token counts when available

## Documentation Roadmap

- [Installation](getting-started/installation.md)
- [Your First Script](getting-started/your-first-script.md)
- [Your First Streaming Turn](getting-started/your-first-streaming-turn.md)
- [Guides](guides/basic-run-and-stateful-conversations.md)
- [Cookbook](cookbook/quick-recipes.md)
- [Reference](reference/api-overview.md)
- [Troubleshooting](troubleshooting/common-errors.md)

## Project Pointers

- Repository: [Goodbuilder34/codex-sdk-unofficial](https://github.com/Goodbuilder34/codex-sdk-unofficial)
- Sample scripts:
  - [samples/basic_streaming.py](https://github.com/Goodbuilder34/codex-sdk-unofficial/blob/main/samples/basic_streaming.py)
  - [samples/structured_output.py](https://github.com/Goodbuilder34/codex-sdk-unofficial/blob/main/samples/structured_output.py)
