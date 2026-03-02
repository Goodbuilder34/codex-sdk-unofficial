from __future__ import annotations

import json
import math
import os
import queue
import re
import shutil
import subprocess
import threading
from dataclasses import dataclass
from typing import Iterator, Mapping, TextIO

from .codex_options import CodexConfigObject, CodexConfigValue
from .thread_options import ApprovalMode, ModelReasoningEffort, SandboxMode, WebSearchMode
from .turn_options import CancelSignal, is_cancelled

INTERNAL_ORIGINATOR_ENV = "CODEX_INTERNAL_ORIGINATOR_OVERRIDE"
PYTHON_SDK_ORIGINATOR = "codex_sdk_py"


@dataclass(slots=True)
class CodexExecArgs:
    input: str
    base_url: str | None = None
    api_key: str | None = None
    thread_id: str | None = None
    images: list[str] | None = None
    model: str | None = None
    sandbox_mode: SandboxMode | None = None
    working_directory: str | None = None
    additional_directories: list[str] | None = None
    skip_git_repo_check: bool | None = None
    output_schema_file: str | None = None
    model_reasoning_effort: ModelReasoningEffort | None = None
    signal: CancelSignal | None = None
    network_access_enabled: bool | None = None
    web_search_mode: WebSearchMode | None = None
    web_search_enabled: bool | None = None
    approval_policy: ApprovalMode | None = None


class CodexExec:
    def __init__(
        self,
        executable_path: str | None = None,
        env: Mapping[str, str] | None = None,
        config_overrides: CodexConfigObject | None = None,
    ) -> None:
        self._executable_path = executable_path or find_codex_path()
        self._env_override = dict(env) if env is not None else None
        self._config_overrides = config_overrides

    def run(self, args: CodexExecArgs) -> Iterator[str]:
        command_args = self._build_command_args(args)
        env = self._build_env(args)

        if is_cancelled(args.signal):
            raise RuntimeError("Codex execution aborted before start")

        try:
            child = subprocess.Popen(
                [self._executable_path, *command_args],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env,
            )
        except OSError as exc:
            raise RuntimeError(f"Failed to spawn Codex CLI: {exc}") from exc

        if child.stdin is None:
            child.kill()
            raise RuntimeError("Child process has no stdin")
        if child.stdout is None:
            child.kill()
            raise RuntimeError("Child process has no stdout")
        if child.stderr is None:
            child.kill()
            raise RuntimeError("Child process has no stderr")

        try:
            child.stdin.write(args.input)
            child.stdin.close()

            stdout_queue: queue.Queue[object] = queue.Queue()
            stderr_chunks: list[str] = []

            stdout_thread = threading.Thread(
                target=_read_stdout_lines, args=(child.stdout, stdout_queue), daemon=True
            )
            stderr_thread = threading.Thread(
                target=_read_stream_text, args=(child.stderr, stderr_chunks), daemon=True
            )
            stdout_thread.start()
            stderr_thread.start()

            while True:
                if is_cancelled(args.signal):
                    _terminate(child)
                    raise RuntimeError("Codex execution aborted")

                try:
                    entry = stdout_queue.get(timeout=0.05)
                except queue.Empty:
                    if child.poll() is not None and not stdout_thread.is_alive():
                        break
                    continue

                if entry is _STREAM_EOF:
                    break
                if isinstance(entry, Exception):
                    raise RuntimeError("Failed reading Codex stdout") from entry

                yield str(entry)

            code = child.wait()
            stderr_thread.join(timeout=0.2)
            stderr_text = "".join(stderr_chunks)
            if code != 0:
                raise RuntimeError(f"Codex Exec exited with code {code}: {stderr_text}")
        finally:
            _terminate(child)

    def _build_command_args(self, args: CodexExecArgs) -> list[str]:
        command_args = ["exec", "--experimental-json"]

        if self._config_overrides:
            for override in serialize_config_overrides(self._config_overrides):
                command_args.extend(["--config", override])

        if args.model:
            command_args.extend(["--model", args.model])
        if args.sandbox_mode:
            command_args.extend(["--sandbox", args.sandbox_mode])
        if args.working_directory:
            command_args.extend(["--cd", args.working_directory])
        if args.additional_directories:
            for directory in args.additional_directories:
                command_args.extend(["--add-dir", directory])
        if args.skip_git_repo_check:
            command_args.append("--skip-git-repo-check")
        if args.output_schema_file:
            command_args.extend(["--output-schema", args.output_schema_file])
        if args.model_reasoning_effort:
            command_args.extend(
                ["--config", f'model_reasoning_effort="{args.model_reasoning_effort}"']
            )
        if args.network_access_enabled is not None:
            network_access = "true" if args.network_access_enabled else "false"
            command_args.extend(
                ["--config", f"sandbox_workspace_write.network_access={network_access}"]
            )
        if args.web_search_mode:
            command_args.extend(["--config", f'web_search="{args.web_search_mode}"'])
        elif args.web_search_enabled is True:
            command_args.extend(["--config", 'web_search="live"'])
        elif args.web_search_enabled is False:
            command_args.extend(["--config", 'web_search="disabled"'])
        if args.approval_policy:
            command_args.extend(["--config", f'approval_policy="{args.approval_policy}"'])
        if args.thread_id:
            command_args.extend(["resume", args.thread_id])
        if args.images:
            for image in args.images:
                command_args.extend(["--image", image])

        return command_args

    def _build_env(self, args: CodexExecArgs) -> dict[str, str]:
        env = dict(self._env_override) if self._env_override is not None else dict(os.environ)
        if INTERNAL_ORIGINATOR_ENV not in env:
            env[INTERNAL_ORIGINATOR_ENV] = PYTHON_SDK_ORIGINATOR
        if args.base_url:
            env["OPENAI_BASE_URL"] = args.base_url
        if args.api_key:
            env["CODEX_API_KEY"] = args.api_key
        return env


_STREAM_EOF = object()


def _read_stdout_lines(stream: TextIO, out_queue: queue.Queue[object]) -> None:
    try:
        while True:
            line = stream.readline()
            if line == "":
                break
            out_queue.put(line.rstrip("\r\n"))
    except Exception as exc:  # pragma: no cover - defensive
        out_queue.put(exc)
    finally:
        out_queue.put(_STREAM_EOF)


def _read_stream_text(stream: TextIO, chunks: list[str]) -> None:
    try:
        while True:
            chunk = stream.read(4096)
            if chunk == "":
                break
            chunks.append(chunk)
    except Exception:
        pass


def _terminate(child: subprocess.Popen[str]) -> None:
    if child.poll() is not None:
        return
    try:
        child.terminate()
    except Exception:
        return
    try:
        child.wait(timeout=0.2)
    except Exception:
        try:
            child.kill()
        except Exception:
            pass


def serialize_config_overrides(config_overrides: CodexConfigObject) -> list[str]:
    overrides: list[str] = []
    _flatten_config_overrides(config_overrides, "", overrides)
    return overrides


def _flatten_config_overrides(
    value: CodexConfigValue | CodexConfigObject,
    prefix: str,
    overrides: list[str],
) -> None:
    if not _is_plain_object(value):
        if prefix:
            overrides.append(f"{prefix}={_to_toml_value(value, prefix)}")
            return
        raise ValueError("Codex config overrides must be a plain object")

    entries = list(value.items())
    if not prefix and len(entries) == 0:
        return
    if prefix and len(entries) == 0:
        overrides.append(f"{prefix}={{}}")
        return

    for key, child in entries:
        if not key:
            raise ValueError("Codex config override keys must be non-empty strings")
        path = f"{prefix}.{key}" if prefix else key
        if _is_plain_object(child):
            _flatten_config_overrides(child, path, overrides)
        else:
            overrides.append(f"{path}={_to_toml_value(child, path)}")


def _to_toml_value(value: CodexConfigValue, path: str) -> str:
    if isinstance(value, str):
        return json.dumps(value)
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"Codex config override at {path} must be a finite number")
        return str(value)
    if isinstance(value, list):
        rendered = [_to_toml_value(item, f"{path}[{index}]") for index, item in enumerate(value)]
        return f"[{', '.join(rendered)}]"
    if _is_plain_object(value):
        parts: list[str] = []
        for key, child in value.items():
            if not key:
                raise ValueError("Codex config override keys must be non-empty strings")
            parts.append(f"{_format_toml_key(key)} = {_to_toml_value(child, f'{path}.{key}')}")
        return "{" + ", ".join(parts) + "}"
    raise ValueError(f"Unsupported Codex config override value at {path}: {type(value).__name__}")


_TOML_BARE_KEY = re.compile(r"^[A-Za-z0-9_-]+$")


def _format_toml_key(key: str) -> str:
    if _TOML_BARE_KEY.match(key):
        return key
    return json.dumps(key)


def _is_plain_object(value: object) -> bool:
    return isinstance(value, dict)


def find_codex_path() -> str:
    codex_binary = shutil.which("codex")
    if codex_binary:
        return codex_binary
    raise RuntimeError(
        "Unable to locate `codex` executable. Install @openai/codex and ensure `codex` is on PATH, "
        "or pass `codex_path_override`."
    )
