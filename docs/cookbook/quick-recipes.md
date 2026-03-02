# Quick Recipes

Prerequisites:
- Basic usage familiarity

What you'll learn:
- Common copy-paste patterns you can adapt quickly

## Recipe: One-shot summary

```python
from codex_sdk import Codex
print(Codex().start_thread().run("Summarize this repo").final_response)
```

## Recipe: Continue conversation

```python
thread = Codex().start_thread()
thread.run("Inspect tests")
print(thread.run("Now propose fixes").final_response)
```

## Recipe: Streaming progress

```python
streamed = Codex().start_thread().run_streamed("Analyze architecture")
for event in streamed.events:
    if event.get("type") == "turn.completed":
        print("done")
```

## Recipe: Structured result

```python
schema = {"type": "object", "properties": {"answer": {"type": "string"}}}
result = Codex().start_thread().run("Answer in JSON", {"output_schema": schema})
print(result.final_response)
```

## Recipe: Image + text prompt

```python
payload = [{"type": "text", "text": "Describe image"}, {"type": "local_image", "path": "./a.png"}]
print(Codex().start_thread().run(payload).final_response)
```

## Recipe: Resume thread

```python
codex = Codex()
thread = codex.resume_thread("thread_id_here")
print(thread.run("Continue").final_response)
```

## Recipe: Override env

```python
codex = Codex({"env": {"PATH": "/usr/local/bin"}})
print(codex.start_thread().run("hello").final_response)
```

## Recipe: Set model and sandbox

```python
thread = Codex().start_thread({"model": "gpt-5", "sandbox_mode": "workspace-write"})
print(thread.run("Audit code").final_response)
```

## Recipe: Add extra directories

```python
thread = Codex().start_thread({"additional_directories": ["../shared", "/tmp/common"]})
print(thread.run("Use these dirs").final_response)
```

## Recipe: Fail-safe wrapper

```python
def run_safe(thread, prompt):
    try:
        return thread.run(prompt).final_response
    except RuntimeError as exc:
        return f"error: {exc}"
```
