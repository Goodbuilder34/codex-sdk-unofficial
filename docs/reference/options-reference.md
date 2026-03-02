# Options Reference

## `CodexOptions`

- `codex_path_override`: override binary path
- `base_url`: sets `OPENAI_BASE_URL`
- `api_key`: sets `CODEX_API_KEY`
- `config`: flattened to `--config key=value`
- `env`: replaces inherited environment when supplied

## `ThreadOptions`

- `model`
- `sandbox_mode`: `read-only` | `workspace-write` | `danger-full-access`
- `working_directory`
- `skip_git_repo_check`
- `model_reasoning_effort`: `minimal` | `low` | `medium` | `high` | `xhigh`
- `network_access_enabled`
- `web_search_mode`: `disabled` | `cached` | `live`
- `web_search_enabled`
- `approval_policy`: `never` | `on-request` | `on-failure` | `untrusted`
- `additional_directories: list[str]`

## `TurnOptions`

- `output_schema`
- `signal` (must expose `is_set()`)

## Mapping Compatibility

All options objects may be passed as dataclass instances or mapping objects.

Both snake_case and legacy camelCase keys are coerced for key option fields.
