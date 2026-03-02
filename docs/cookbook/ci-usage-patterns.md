# CI Usage Patterns

Prerequisites:
- Familiarity with CI pipelines

What you'll learn:
- How to integrate SDK calls in CI scripts with UV

## Minimal CI step

```bash
uv run python scripts/codex_check.py
```

## Build-and-check pipeline sketch

```bash
uv run pytest -q
uv run python scripts/codex_review.py
```

## Practical recommendations

- keep prompts deterministic for CI checks
- parse and store outputs as artifacts
- fail pipeline on explicit policy conditions only

## Failure modes

- using non-deterministic prompts as hard quality gates
- missing retries for transient infrastructure failures
