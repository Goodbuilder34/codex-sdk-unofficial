# Automation Scripts

Prerequisites:
- Familiarity with cron/CI style automation

What you'll learn:
- How to use the SDK in unattended scripts

## Nightly repository summary

```python
from datetime import datetime
from codex_sdk import Codex

thread = Codex().start_thread({"working_directory": "/srv/repo", "skip_git_repo_check": True})
result = thread.run("Summarize new changes and risks from today")
print(datetime.utcnow().isoformat(), result.final_response)
```

Run:

```bash
uv run python nightly_summary.py
```

## Persisting thread IDs between runs

```python
# save thread.id at end of successful run
# load and call resume_thread on next run
```

## Safety checklist

- enforce explicit working directory
- use strict approval policy for unattended jobs
- capture logs and stderr-backed runtime errors
