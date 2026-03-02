# Structured JSON Workflows

Prerequisites:
- JSON Schema basics

What you'll learn:
- Schema-first automation patterns

## Pattern: enforce contract for downstream parser

```python
schema = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "severity": {"type": "string", "enum": ["low", "medium", "high"]},
    },
    "required": ["summary", "severity"],
    "additionalProperties": False,
}

result = Codex().start_thread().run("Assess this patch", {"output_schema": schema})
print(result.final_response)
```

## Pattern: queue fan-out by status

- Parse `result.final_response` JSON
- Route tasks based on status/severity
- Persist raw text for auditability

## Failure modes

- weak schema that allows unusable outputs
- missing validation downstream
