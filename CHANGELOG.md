# Changelog

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
