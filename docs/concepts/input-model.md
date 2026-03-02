# Input Model

Prerequisites:
- Familiarity with Python dict/list literals

What you'll learn:
- Supported input shapes
- How text and image inputs are normalized

## Supported Input Types

`Input` accepts:
- `str`
- `list[UserInput]`

`UserInput` variants:
- `{"type": "text", "text": "..."}`
- `{"type": "local_image", "path": "..."}`

## Normalization Rules

When input is a list:
- Text parts are joined with two newlines
- Local image paths are forwarded as repeated `--image` args

Example:

```python
payload = [
    {"type": "text", "text": "Describe file changes"},
    {"type": "text", "text": "Focus on tests"},
    {"type": "local_image", "path": "./ui.png"},
]
```

Effective behavior:
- Prompt becomes: `Describe file changes\n\nFocus on tests`
- Images list includes: `./ui.png`

## Best Practices

- Keep text segments intentional and readable
- Validate local image paths before calling `run`
- Prefer one conceptual task per turn
