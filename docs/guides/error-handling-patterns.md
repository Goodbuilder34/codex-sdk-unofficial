# Error Handling Patterns

Prerequisites:
- Basic Python exception handling

What you'll learn:
- How to distinguish subprocess errors vs turn failures
- How to wrap calls for resilient callers

## Recommended Wrapper

```python
from codex_sdk import Codex

def safe_run(prompt: str) -> tuple[bool, str]:
    thread = Codex().start_thread()
    try:
        result = thread.run(prompt)
        return True, result.final_response
    except RuntimeError as exc:
        return False, str(exc)
```

## Error Categories

- Spawn errors: CLI not executable
- Process exit errors: non-zero code with stderr
- Turn failure errors: `turn.failed` with message
- Parse errors: malformed/non-JSON event line

## Streaming Resilience

- Always guard event field access
- Keep fallback branch for unknown payloads
- Log raw event for diagnostics

## Failure Modes

- Catching broad exceptions without recording context
- Treating all runtime errors as equivalent remediation paths
