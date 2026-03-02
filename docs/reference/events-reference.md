# Events Reference

`ThreadEvent` includes these event types:

- `thread.started`
  - fields: `thread_id`
- `turn.started`
- `item.started`
  - fields: `item`
- `item.updated`
  - fields: `item`
- `item.completed`
  - fields: `item`
- `turn.completed`
  - fields: `usage` (`input_tokens`, `cached_input_tokens`, `output_tokens`)
- `turn.failed`
  - fields: `error.message`
- `error`
  - fields: `message`

## Usage Type

```python
{
  "input_tokens": int,
  "cached_input_tokens": int,
  "output_tokens": int,
}
```

## Notes

- Always guard with `event.get("type")`
- Do not assume every event appears in every turn
