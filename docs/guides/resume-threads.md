# Resume Threads

Prerequisites:
- A previously created thread ID

What you'll learn:
- How to continue an existing session
- How to structure resumable workflows

## Basic Resume

```python
from codex_sdk import Codex

saved_id = "thread_abc123"
thread = Codex().resume_thread(saved_id)
result = thread.run("Continue from where we left off")
print(result.final_response)
```

## Persisting Thread IDs

Recommended:
- Save `thread.id` after each successful turn
- Store alongside your task/job metadata

## Safety Pattern

```python
if thread.id is not None:
    save_id(thread.id)
```

## Failure Modes

- Using stale IDs that no longer map to valid underlying session state
- Creating a new thread by mistake instead of resuming
