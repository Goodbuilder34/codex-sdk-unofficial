# Prerequisites and Codex CLI

Prerequisites:
- Basic terminal usage
- Existing UV-managed Python project
- `codex` CLI installed

What you'll learn:
- Why this SDK depends on the Codex CLI
- What environment variables matter
- When to use path overrides

## How The SDK Works At Runtime

The SDK launches `codex exec --experimental-json` as a subprocess and streams JSONL events over stdout.

Because of that:
- Python import success is not enough
- `codex` CLI must also be installed and reachable

## Required Runtime Pieces

- `codex-sdk-unofficial`
- `codex` executable
- Valid auth/config recognized by Codex CLI

## Useful Constructor Options

```python
from codex_sdk import Codex

codex = Codex(
    {
        "codex_path_override": "/absolute/path/to/codex",
        "base_url": "https://your-endpoint.example",
        "api_key": "your-api-key",
    }
)
```

## Environment Behavior

By default:
- SDK inherits your current process environment

If you pass `env`:
- SDK uses only provided keys (plus required injected keys like originator/base url/api key)

## Failure Modes

- CLI not on `PATH`
- CLI installed but wrong binary
- Auth misconfiguration in environment
- Running in restricted environment where subprocess spawn is blocked
