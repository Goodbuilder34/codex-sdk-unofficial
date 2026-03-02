# Threads, Turns, Events, and Items

Prerequisites:
- Basic familiarity with request/response workflows

What you'll learn:
- The core vocabulary of this SDK
- How thread continuity works
- How to reason about event and item payloads

## Thread

A `Thread` represents a conversation session.

- Start new: `codex.start_thread()`
- Resume existing: `codex.resume_thread(thread_id)`

`thread.id` is populated when `thread.started` event arrives.

## Turn

A turn is one prompt submission plus all resulting events until completion or failure.

- Buffered mode: `thread.run(...)` returns `Turn`
- Streaming mode: `thread.run_streamed(...)` returns iterator of events

## Events

Top-level stream records, e.g.:
- `thread.started`
- `turn.started`
- `item.started` / `item.updated` / `item.completed`
- `turn.completed`
- `turn.failed`

## Items

Items are typed payloads inside item events, e.g.:
- `agent_message`
- `reasoning`
- `command_execution`
- `file_change`
- `todo_list`

## Lifecycle Example

1. Prompt sent
2. `thread.started` (new thread only)
3. `turn.started`
4. one or more item events
5. `turn.completed` with usage or `turn.failed` with error

Failure modes:
- assuming `thread.id` exists before first turn starts
- assuming every stream includes all item categories
