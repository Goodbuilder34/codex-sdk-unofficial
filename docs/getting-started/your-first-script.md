# Your First Script

Prerequisites:
- Completed [Installation](installation.md)

What you'll learn:
- The canonical import line
- How to start a thread and run one turn
- How to read `final_response`, `items`, and `usage`

## Exact Import (Use This)

```python
from codex_sdk import Codex
```

## Script

```python
from codex_sdk import Codex

codex = Codex()
thread = codex.start_thread()

turn = thread.run("Diagnose the test failure and propose a fix")

print("Thread ID:", thread.id)
print("Final response:\n", turn.final_response)
print("Items count:", len(turn.items))
print("Usage:", turn.usage)
```

Run:

```bash
uv run python first_script.py
```

Expected behavior:
- `thread.id` is `None` before first turn starts
- `thread.id` is populated once `thread.started` arrives
- `turn.final_response` is the final assistant text from completed items

## Continue The Same Conversation

```python
follow_up = thread.run("Now summarize the fix in 3 bullets")
print(follow_up.final_response)
```

## Failure Modes

- Runtime error from turn failure event
- JSON parse failure if subprocess output is malformed
- Non-zero subprocess exit from CLI issues
