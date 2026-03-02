from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, TypeAlias, TypeGuard

CodexConfigValue: TypeAlias = (
    str | int | float | bool | list["CodexConfigValue"] | "CodexConfigObject"
)
CodexConfigObject: TypeAlias = dict[str, CodexConfigValue]


@dataclass(slots=True)
class CodexOptions:
    codex_path_override: str | None = None
    base_url: str | None = None
    api_key: str | None = None
    config: CodexConfigObject | None = None
    env: dict[str, str] | None = None


def coerce_codex_options(options: CodexOptions | Mapping[str, object] | None) -> CodexOptions:
    if options is None:
        return CodexOptions()
    if isinstance(options, CodexOptions):
        return options
    if isinstance(options, Mapping):
        env = options.get("env")
        config = options.get("config")
        return CodexOptions(
            codex_path_override=_as_optional_str(
                options.get("codex_path_override", options.get("codexPathOverride"))
            ),
            base_url=_as_optional_str(options.get("base_url", options.get("baseUrl"))),
            api_key=_as_optional_str(options.get("api_key", options.get("apiKey"))),
            config=dict(config) if isinstance(config, Mapping) else None,
            env=dict(env) if isinstance(env, Mapping) else None,
        )
    raise TypeError("options must be CodexOptions, a mapping, or None")


def is_plain_mapping(value: object) -> TypeGuard[Mapping[str, object]]:
    return isinstance(value, Mapping)


def _as_optional_str(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    raise TypeError(f"Expected string or None, got {type(value).__name__}")
