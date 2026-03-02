# Image Inputs

Prerequisites:
- Local image files available

What you'll learn:
- How to submit mixed text + image turns
- How image paths are forwarded

## Example

```python
from codex_sdk import Codex

thread = Codex().start_thread()
result = thread.run(
    [
        {"type": "text", "text": "Describe these screenshots"},
        {"type": "local_image", "path": "./ui.png"},
        {"type": "local_image", "path": "./diagram.jpg"},
    ]
)

print(result.final_response)
```

## Behavior Notes

- Text inputs are combined into a single prompt body
- Images are passed as repeated `--image` flags
- Thread continuity works exactly the same as text-only turns

## Failure Modes

- Relative path mismatch due to working directory
- Non-existent files
