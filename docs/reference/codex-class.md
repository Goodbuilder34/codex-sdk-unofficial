# `Codex` Class Reference

## Constructor

```python
Codex(options: CodexOptions | Mapping[str, object] | None = None)
```

### `options` fields

- `codex_path_override: str | None`
- `base_url: str | None`
- `api_key: str | None`
- `config: dict[str, CodexConfigValue] | None`
- `env: dict[str, str] | None`

## Methods

### `start_thread(options=None) -> Thread`
Starts a new thread.

### `resume_thread(thread_id, options=None) -> Thread`
Resumes a thread by id.

### Compatibility aliases

- `startThread(...)`
- `resumeThread(...)`

## Example

```python
from codex_sdk import Codex

codex = Codex({"base_url": "https://example", "api_key": "token"})
thread = codex.start_thread({"model": "gpt-5"})
```
