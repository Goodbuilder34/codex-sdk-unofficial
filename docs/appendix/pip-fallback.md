# pip Fallback (Non-Primary)

This project is UV-first. Use this page only when UV is not available.

## Install with pip

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install codex-sdk-unofficial
python -c "from codex_sdk import Codex; print('import-ok')"
```

## Run scripts

```bash
python your_script.py
```

## Important

- Keep all main guides UV-first
- Treat this page as fallback compatibility documentation only
