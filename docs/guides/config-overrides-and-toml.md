# Config Overrides and TOML Serialization

Prerequisites:
- Familiarity with nested dict configuration

What you'll learn:
- How `CodexOptions.config` is transformed
- How nested config becomes `--config key=value`

## Example Input

```python
config = {
    "approval_policy": "never",
    "sandbox_workspace_write": {"network_access": True},
    "retry_budget": 3,
    "tool_rules": {"allow": ["git status", "git diff"]},
}
```

## Effective CLI Overrides

- `approval_policy="never"`
- `sandbox_workspace_write.network_access=true`
- `retry_budget=3`
- `tool_rules.allow=["git status", "git diff"]`

## Rules

- Top-level must be an object
- Keys must be non-empty strings
- Numbers must be finite
- Booleans map to `true` / `false`
- Lists and objects serialize recursively

## Failure Modes

- Null/unsupported value types
- Empty keys
- Non-finite floats
