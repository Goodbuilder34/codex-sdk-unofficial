# Changelog

## v0.1.3 - 2026-03-02

- Add simple streaming mode to `Thread.run(...)` via `stream=True` for live assistant text output.
- Stream `agent_message` text from `item.updated` and `item.completed` events while preventing duplicate output by emitting only suffix deltas.
- Preserve buffered `Turn` behavior (`items`, `final_response`, and `usage`) while adding stdout streaming support.
- Add newline cleanup behavior for streamed output on completion/failure and keep `turn.failed` error raising semantics.
- Add test coverage for streaming deltas, default non-stream behavior, failure newline handling, and newline non-duplication.
- Update docs and README to document `run(..., stream=True)` as the simple streaming path and position `run_streamed()` as the advanced raw-event API.

## v0.1.2 - 2026-03-02

- Launch a full MkDocs + Material documentation site with beginner-first, UV-first guides.
- Add complete docs structure: getting started, concepts, guides, cookbook, reference, troubleshooting, FAQ, contributing, releasing, and pip fallback appendix.
- Add strict docs navigation/build config via `mkdocs.yml`.
- Add GitHub Pages docs workflow with automatic deploy from `main`.
- Update CI to enforce strict docs build.
- Convert README into a concise UV-first entrypoint that links to full documentation.
- Add docs dependency group in `pyproject.toml`.

## v0.1.1 - 2026-03-02

- Fix Python 3.12 import/runtime compatibility for recursive config type aliases.
- Confirm test suite passes on Python 3.12.

## v0.1.0 - 2026-03-02

- Initial public release of the unofficial Python Codex SDK.
- Added `Codex` and `Thread` APIs with streamed and buffered turn execution.
- Added structured output schema support and image input forwarding.
- Added tests for execution args, thread behavior, and schema temp-file lifecycle.
- Added packaging metadata and release instructions for GitHub + PyPI.
