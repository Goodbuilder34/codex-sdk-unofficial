# Security and Sandboxing

Prerequisites:
- Understanding of local execution risk boundaries

What you'll learn:
- How sandbox-related options are passed
- How to shape safer defaults

## Relevant Thread Options

- `sandbox_mode`
- `approval_policy`
- `working_directory`
- `additional_directories`
- `network_access_enabled`

## Safer Baseline Example

```python
from codex_sdk import Codex

thread = Codex().start_thread(
    {
        "sandbox_mode": "workspace-write",
        "approval_policy": "on-request",
        "working_directory": "/safe/project",
        "additional_directories": ["/safe/shared"],
        "network_access_enabled": False,
    }
)
```

## Operational Guidance

- Use least privilege for directories
- Prefer explicit working directory
- Keep approval policy strict in untrusted contexts
- Disable network unless required

## Failure Modes

- Granting broad directory access by default
- Running with unsafe approval policy in automation without review
