# API Overview

Prerequisites:
- Familiarity with Python classes and dictionaries

What you'll learn:
- The complete API surface at a glance

## Import

```python
from codex_sdk import Codex
```

## Primary Classes

- `Codex`
- `Thread`
- `Turn`
- `StreamedTurn`

## Method Summary

- `Codex.start_thread(options=None) -> Thread`
- `Codex.resume_thread(thread_id, options=None) -> Thread`
- `Thread.run(input, turn_options=None) -> Turn`
- `Thread.run_streamed(input, turn_options=None) -> StreamedTurn`

Compatibility aliases are also available:
- `startThread`
- `resumeThread`
- `runStreamed`

## Core Data Shapes

- `Input = str | list[UserInput]`
- `UserInput = TextUserInput | LocalImageUserInput`
- `ThreadEvent` union of event payloads
- `ThreadItem` union of item payloads
