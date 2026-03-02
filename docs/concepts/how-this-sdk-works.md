# How This SDK Works

Prerequisites:
- Familiarity with Python subprocess basics

What you'll learn:
- Runtime architecture
- Why event streaming exists
- Where errors originate

## Architecture Summary

`codex-sdk-unofficial` is a thin Python wrapper around the Codex CLI.

At runtime the SDK:
1. Builds CLI args (`codex exec --experimental-json ...`)
2. Spawns a subprocess
3. Sends user prompt to stdin
4. Reads JSONL events from stdout
5. Aggregates or streams those events to your code

## Components

- `Codex`: top-level client and options holder
- `Thread`: conversation lifecycle and turn execution
- `CodexExec`: subprocess execution, argument construction, env wiring

## Why Event-Driven

The CLI emits event records. The SDK keeps this model intact so you can:
- Consume every state transition (`item.started`, `item.updated`, `item.completed`)
- Keep full observability in advanced integrations

## Error Surfaces

There are three major classes:
- Subprocess spawn errors
- Non-zero subprocess exits (with stderr)
- Turn-level failures from event stream (`turn.failed`)

## Compatibility Notes

- Python 3.10+
- UV is recommended for all workflows
- SDK is community-maintained and unofficial
