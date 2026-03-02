# Streaming Events

Prerequisites:
- [Your First Streaming Turn](../getting-started/your-first-streaming-turn.md)

What you'll learn:
- Building robust streaming handlers
- Mapping event types to actions

## Production-Safe Loop Pattern

```python
from codex_sdk import Codex

thread = Codex().start_thread()
streamed = thread.run_streamed("Audit this code and propose fixes")

for event in streamed.events:
    t = event.get("type")

    if t == "thread.started":
        print("Thread:", event.get("thread_id"))

    elif t == "item.completed":
        item = event.get("item", {})
        if isinstance(item, dict) and item.get("type") == "agent_message":
            print(item.get("text", ""))

    elif t == "turn.completed":
        print("Usage:", event.get("usage"))

    elif t == "turn.failed":
        err = event.get("error", {})
        print("Failure:", err.get("message"))
```

## Event Handling Strategy

- Handle known types explicitly
- Ignore unknown types gracefully for forward compatibility
- Log raw event payloads during integration testing

Reference sample:
- [`samples/basic_streaming.py`](https://github.com/Goodbuilder34/codex-sdk-unofficial/blob/main/samples/basic_streaming.py)

## Failure Modes

- Treating all item payloads as the same shape
- Assuming streamed order implies business completion without checking `turn.completed`
