# Long-Running Stream Consumers

Prerequisites:
- Streaming basics

What you'll learn:
- Robust event consumer patterns for long sessions

## Pattern: typed dispatch map

```python
handlers = {
    "thread.started": handle_thread_started,
    "item.completed": handle_item_completed,
    "turn.completed": handle_turn_completed,
    "turn.failed": handle_turn_failed,
}

for event in streamed.events:
    fn = handlers.get(event.get("type"), handle_unknown)
    fn(event)
```

## Pattern: checkpointing

- write event snapshots to local log
- record last complete turn markers
- recover gracefully after process interruption

## Pattern: cancellation watchdog

- monitor time budget
- set signal when threshold exceeded

Failure modes:
- memory growth from storing all raw events indefinitely
- no timeout or cancellation path in long-running service
