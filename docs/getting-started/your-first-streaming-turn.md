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

streamed = thread.run_streamed("Inspect this repository and propose a refactor plan")

for event in streamed.events:
    t = event.get("type")
    if t == "item.completed":
        item = event.get("item", {})
        if isinstance(item, dict) and item.get("type") == "agent_message":
            print("Assistant:", item.get("text", ""))
    elif t == "turn.completed":
        print("Usage:", event.get("usage"))
    elif t == "turn.failed":
        print("Turn failed:", event.get("error"))
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

Use `run()` when you need:
- Simpler control flow
- Final results only

## Failure Modes

- Unhandled event shape assumptions (`dict` checks are important)
- Consuming stream partially and expecting complete summary data
