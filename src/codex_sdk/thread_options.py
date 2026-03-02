from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Mapping, TypeAlias

ApprovalMode: TypeAlias = Literal["never", "on-request", "on-failure", "untrusted"]
SandboxMode: TypeAlias = Literal["read-only", "workspace-write", "danger-full-access"]
ModelReasoningEffort: TypeAlias = Literal["minimal", "low", "medium", "high", "xhigh"]
WebSearchMode: TypeAlias = Literal["disabled", "cached", "live"]


@dataclass(slots=True)
class ThreadOptions:
    model: str | None = None
    sandbox_mode: SandboxMode | None = None
    working_directory: str | None = None
    skip_git_repo_check: bool | None = None
    model_reasoning_effort: ModelReasoningEffort | None = None
    network_access_enabled: bool | None = None
    web_search_mode: WebSearchMode | None = None
    web_search_enabled: bool | None = None
    approval_policy: ApprovalMode | None = None
    additional_directories: list[str] | None = None


def coerce_thread_options(options: ThreadOptions | Mapping[str, object] | None) -> ThreadOptions:
    if options is None:
        return ThreadOptions()
    if isinstance(options, ThreadOptions):
        return options
    if isinstance(options, Mapping):
        dirs = options.get("additional_directories", options.get("additionalDirectories"))
        return ThreadOptions(
            model=_as_optional_str(options.get("model")),
            sandbox_mode=_as_optional_str(options.get("sandbox_mode", options.get("sandboxMode"))),  # type: ignore[arg-type]
            working_directory=_as_optional_str(
                options.get("working_directory", options.get("workingDirectory"))
            ),
            skip_git_repo_check=_as_optional_bool(
                options.get("skip_git_repo_check", options.get("skipGitRepoCheck"))
            ),
            model_reasoning_effort=_as_optional_str(
                options.get("model_reasoning_effort", options.get("modelReasoningEffort"))
            ),  # type: ignore[arg-type]
            network_access_enabled=_as_optional_bool(
                options.get("network_access_enabled", options.get("networkAccessEnabled"))
            ),
            web_search_mode=_as_optional_str(
                options.get("web_search_mode", options.get("webSearchMode"))
            ),  # type: ignore[arg-type]
            web_search_enabled=_as_optional_bool(
                options.get("web_search_enabled", options.get("webSearchEnabled"))
            ),
            approval_policy=_as_optional_str(
                options.get("approval_policy", options.get("approvalPolicy"))
            ),  # type: ignore[arg-type]
            additional_directories=_as_optional_str_list(dirs),
        )
    raise TypeError("options must be ThreadOptions, a mapping, or None")


def _as_optional_str(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    raise TypeError(f"Expected string or None, got {type(value).__name__}")


def _as_optional_bool(value: object) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    raise TypeError(f"Expected bool or None, got {type(value).__name__}")


def _as_optional_str_list(value: object) -> list[str] | None:
    if value is None:
        return None
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    raise TypeError("Expected list[str] or None")
