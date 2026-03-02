# Options (Codex, Thread, Turn)

Prerequisites:
- Basic Python dict usage

What you'll learn:
- Which options belong at each layer
- How options are merged and applied

## CodexOptions (client-wide)

Set once on `Codex(...)`:
- `codex_path_override`
- `base_url`
- `api_key`
- `config`
- `env`

## ThreadOptions (conversation-wide)

Set on `start_thread(...)` or `resume_thread(...)`:
- `model`, `sandbox_mode`, `working_directory`
- `skip_git_repo_check`, `additional_directories`
- `model_reasoning_effort`, `network_access_enabled`
- `web_search_mode`, `web_search_enabled`
- `approval_policy`

## TurnOptions (request-specific)

Set per `run(...)` call:
- `output_schema`
- `signal`

## Full Example

```python
from codex_sdk import Codex

codex = Codex(
    {
        "base_url": "https://example.endpoint",
        "api_key": "token",
        "config": {"approval_policy": "never"},
    }
)

thread = codex.start_thread(
    {
        "model": "gpt-5",
        "sandbox_mode": "workspace-write",
        "working_directory": "/path/to/repo",
        "skip_git_repo_check": True,
    }
)

turn = thread.run("Summarize changes", {"output_schema": {"type": "object"}})
print(turn.final_response)
```

## Failure Modes

- Passing wrong types in mapping options
- Setting conflicting web search values without clear intent
