# Your First Streaming Turn

Prerequisites:
- Completed [Your First Script](your-first-script.md)

What you'll learn:
- How to stream events during execution
- How to handle event types safely
- When to choose streaming over buffered runs

## Streaming Example

```python
from codex_sdk import Codex

codex = Codex()
thread = codex.start_thread()

turn = thread.run(
    "Inspect this repository and propose a refactor plan",
    stream=True,
)
print("Final response:", turn.final_response)
print("Usage:", turn.usage)
```

Run:

```bash
uv run python first_stream.py
```

## When To Use Streaming

Use `run_streamed()` when you need:
- Progress visibility
- Near-real-time UI updates
- Fine-grained event handling
- Direct access to raw event payloads (`item.updated`, `item.completed`, etc.)

Use `run()` when you need:
- Simpler control flow
- Final results only
- Optional simple live text streaming via `stream=True`

## Failure Modes

- Unhandled event shape assumptions (`dict` checks are important)
- Consuming stream partially and expecting complete summary data
