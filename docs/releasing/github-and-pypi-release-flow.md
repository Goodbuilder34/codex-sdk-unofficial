# GitHub and PyPI Release Flow

Prerequisites:
- Maintainer access to repository and tags
- PyPI Trusted Publisher configured

What you'll learn:
- How to cut a release using UV-first commands
- How publish automation is triggered

## 1) Update version

- `pyproject.toml` project version
- `src/codex_sdk/__init__.py` `__version__`
- changelog

## 2) Run validation

```bash
PYTHONPATH=src uv run pytest -q
uv run --group docs mkdocs build --strict
```

## 3) Build artifacts

```bash
uv run --with build python -m build
```

## 4) Commit and tag

```bash
git add .
git commit -m "release: vX.Y.Z"
git tag -a vX.Y.Z -m "vX.Y.Z"
```

## 5) Push

```bash
git push origin main --tags
```

Tag pushes trigger `.github/workflows/publish.yml`.

## 6) Trusted Publisher Flow

Workflow `publish.yml` publishes to PyPI via OIDC using environment `pypi`.

## Optional manual upload

```bash
uv run --with twine twine upload dist/*
```
