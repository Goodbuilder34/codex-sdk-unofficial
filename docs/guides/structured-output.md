# Structured Output

Prerequisites:
- JSON Schema familiarity

What you'll learn:
- How to request schema-constrained output
- How `output_schema` flows to CLI

## Example

```python
from codex_sdk import Codex

schema = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "status": {"type": "string", "enum": ["ok", "action_required"]},
    },
    "required": ["summary", "status"],
    "additionalProperties": False,
}

thread = Codex().start_thread()
result = thread.run("Summarize repo status", {"output_schema": schema})
print(result.final_response)
```

Run:

```bash
uv run python structured_output.py
```

## What Happens Internally

- SDK writes schema JSON to a temp file
- Passes `--output-schema <tempfile>` to Codex CLI
- Cleans up temp directory after turn

Reference sample:
- [`samples/structured_output.py`](https://github.com/Goodbuilder34/codex-sdk-unofficial/blob/main/samples/structured_output.py)

## Failure Modes

- Passing non-object schema value
- Assuming output text is always plain prose when schema is requested
