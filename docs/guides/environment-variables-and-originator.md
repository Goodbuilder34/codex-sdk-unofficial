# Environment Variables and Originator

Prerequisites:
- Familiarity with process environments

What you'll learn:
- How env inheritance works
- How to isolate env for subprocess execution

## Default Behavior

If `env` is omitted:
- SDK inherits your current process environment

If `env` is provided:
- SDK uses only provided values plus required injections

## Injected Variables

SDK sets when needed:
- `CODEX_INTERNAL_ORIGINATOR_OVERRIDE` (defaults to `codex_sdk_py`)
- `OPENAI_BASE_URL` if provided
- `CODEX_API_KEY` if provided

## Example Isolated Env

```python
from codex_sdk import Codex

codex = Codex(
    {
        "env": {
            "PATH": "/usr/local/bin",
            "CUSTOM_ENV": "value",
        }
    }
)
```

## Failure Modes

- Providing too minimal `PATH` so CLI cannot resolve dependencies
- Assuming host env variables will be present when `env` override is used
