# Type Aliases and Compatibility

## Runtime/Python Compatibility

- Supported Python: `>=3.10`
- Tested workflow baseline: Python 3.12

## Core Type Aliases

- `Input`
- `UserInput`
- `RunResult`
- `RunStreamedResult`
- `ThreadEvent`
- `ThreadItem`
- `CodexConfigValue`

## API Compatibility Notes

- Snake_case methods are primary Python interface
- CamelCase aliases are available for compatibility:
  - `startThread`, `resumeThread`, `runStreamed`
- `Turn.finalResponse` property mirrors `final_response`

## Guidance

Prefer snake_case in new Python code for consistency with ecosystem norms.
