# FAQ

## Is this an official OpenAI SDK?

No. `codex-sdk-unofficial` is community-maintained and unofficial.

## What import should I use?

```python
from codex_sdk import Codex
```

## Should I use UV or other tooling?

Use UV as the primary workflow in this project.

## Why does this require the Codex CLI?

This SDK wraps the CLI by launching it as a subprocess and consuming event output.

## Should I use `run()` or `run_streamed()`?

- `run()` for simple final-result use cases
- `run_streamed()` for live progress and fine-grained event handling

## Can I pass options as plain dicts?

Yes. Dict mappings are supported and coerced.

## How do I continue the same conversation?

Reuse the same `Thread` object or resume with `resume_thread(thread_id)`.
