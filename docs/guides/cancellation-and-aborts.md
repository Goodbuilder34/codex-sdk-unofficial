# Cancellation and Aborts

Prerequisites:
- Familiarity with thread synchronization primitives

What you'll learn:
- How `signal` cancellation works
- Safe cancel patterns for CLI-driven work

## TurnOptions Signal Contract

`TurnOptions.signal` accepts an object exposing:
- `is_set() -> bool`

The SDK checks cancellation:
- Before spawn
- During stream consumption loop

## Example With `threading.Event`

```python
import threading
from codex_sdk import Codex

stop = threading.Event()
thread = Codex().start_thread()

# stop.set() can be called by another thread
try:
    result = thread.run("Perform deep analysis", {"signal": stop})
    print(result.final_response)
except RuntimeError as exc:
    print("Cancelled or failed:", exc)
```

## Streaming Cancellation Pattern

```python
streamed = thread.run_streamed("Long task", {"signal": stop})
for event in streamed.events:
    if should_cancel(event):
        stop.set()
```

## Failure Modes

- Passing a signal-like object without `is_set()`
- Assuming cancellation returns partial turn summary like normal completion
