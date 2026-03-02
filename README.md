# Unofficial Codex SDK (Python)

Unofficial, community-maintained Python SDK for the Codex CLI.

This project is **not an official OpenAI SDK**. It wraps the `codex` CLI from `@openai/codex`, spawning the CLI and exchanging JSONL events over stdin/stdout.

## Installation

```bash
pip install codex-sdk-unofficial
```

Requires Python 3.10+ and a `codex` executable on your `PATH` (or pass `codex_path_override`).

## Status

- Package name: `codex-sdk-unofficial`
- Import name: `codex_sdk`
- Current version: `0.1.0`
- Stability: alpha

## Quickstart

```python
from codex_sdk import Codex, __version__

print("codex_sdk version:", __version__)

codex = Codex()
thread = codex.start_thread()
turn = thread.run("Diagnose the test failure and propose a fix")

print(turn.final_response)
print(turn.items)
```

Call `run()` repeatedly on the same `Thread` to continue a conversation.

```python
next_turn = thread.run("Implement the fix")
```

## Streaming responses

`run()` buffers events until completion. To react to intermediate progress, use `run_streamed()`.

```python
streamed = thread.run_streamed("Diagnose the test failure and propose a fix")
for event in streamed.events:
    if event["type"] == "item.completed":
        print("item", event["item"])
    elif event["type"] == "turn.completed":
        print("usage", event["usage"])
```

## Structured output

```python
schema = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "status": {"type": "string", "enum": ["ok", "action_required"]},
    },
    "required": ["summary", "status"],
    "additionalProperties": False,
}

turn = thread.run("Summarize repository status", {"output_schema": schema})
print(turn.final_response)
```

## Attaching images

```python
thread.run(
    [
        {"type": "text", "text": "Describe these screenshots"},
        {"type": "local_image", "path": "./ui.png"},
        {"type": "local_image", "path": "./diagram.jpg"},
    ]
)
```

## Resuming an existing thread

```python
thread = codex.resume_thread("thread_id_here")
thread.run("Implement the fix")
```

## Working directory and execution options

```python
thread = codex.start_thread(
    {
        "working_directory": "/path/to/project",
        "skip_git_repo_check": True,
        "sandbox_mode": "workspace-write",
    }
)
```

## Overriding CLI environment

```python
codex = Codex(
    {
        "env": {"PATH": "/usr/local/bin"},
    }
)
```

## Global `--config` overrides

```python
codex = Codex(
    {
        "config": {
            "show_raw_agent_reasoning": True,
            "sandbox_workspace_write": {"network_access": True},
        }
    }
)
```

## Publish Checklist

1. Update `pyproject.toml` version and `src/codex_sdk/__init__.py` `__version__`.
2. Run tests:
   ```bash
   PYTHONPATH=src uv run pytest -q
   ```
3. Build artifacts:
   ```bash
   uv run --with build python -m build
   ```
4. Commit and create a version tag:
   ```bash
   git add .
   git commit -m "release: v0.1.0"
   git tag -a v0.1.0 -m "v0.1.0"
   ```
5. Push GitHub branch + tags:
   ```bash
   git push origin main --tags
   ```
6. Publish to PyPI (after creating a trusted publisher or API token):
   ```bash
   uv run --with twine twine upload dist/*
   ```
