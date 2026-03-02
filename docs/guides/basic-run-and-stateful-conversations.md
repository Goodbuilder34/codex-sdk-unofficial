# Basic Run and Stateful Conversations

Prerequisites:
- [Your First Script](../getting-started/your-first-script.md)

What you'll learn:
- Reusing a thread across multiple turns
- Interpreting run results safely

## Single Turn

```python
from codex_sdk import Codex

thread = Codex().start_thread()
result = thread.run("Summarize this repository")
print(result.final_response)
```

## Multi-Turn Conversation

```python
first = thread.run("Identify the top risk in this codebase")
second = thread.run("Propose a minimal patch for that risk")
third = thread.run("Write a rollout checklist")
```

Use one thread for one evolving conversation.

## Reading Result Data

```python
print(result.final_response)
for item in result.items:
    print(item.get("type"), item)
print(result.usage)
```

## Failure Modes

- Creating new threads for each follow-up and losing context
- Assuming `usage` is always present
