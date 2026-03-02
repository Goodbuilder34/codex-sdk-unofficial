# Docs Contribution Guide

Thanks for helping improve this documentation.

## Goals

- Keep docs beginner-first
- Keep commands UV-first
- Keep examples copy-pasteable

## Page Template

Each page should include:
- prerequisites
- what you'll learn
- examples
- expected behavior
- failure modes

## Style Rules

- Use exact import snippets:

```python
from codex_sdk import Codex
```

- Prefer concise, explicit steps
- Avoid hidden assumptions
- Keep unofficial disclaimer visible where relevant

## Validation Checklist

Before opening a PR:

```bash
uv run --group docs mkdocs build --strict
PYTHONPATH=src uv run pytest -q
```
