# `Thread` Class Reference

## Properties

### `id: str | None`
Thread identifier. Usually populated after first `thread.started` event.

## Methods

### `run(input, turn_options=None, *, stream=False) -> Turn`
Runs a buffered turn and returns:
- `items: list[ThreadItem]`
- `final_response: str`
- `usage: Usage | None`

If `stream=True`, assistant message text is written to stdout as it arrives.

### `run_streamed(input, turn_options=None) -> StreamedTurn`
Returns `StreamedTurn(events=Iterator[ThreadEvent])`.

### Compatibility alias

- `runStreamed(...)`

## Input Types

- `str`
- `list[{"type": "text"|"local_image", ...}]`

## Example

```python
thread = Codex().start_thread()
turn = thread.run("Hello")
for event in thread.run_streamed("Follow up").events:
    print(event)
```
