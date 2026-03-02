from __future__ import annotations

import io
import os
import subprocess
from typing import Any

import pytest

from codex_sdk.exec import (
    CodexExec,
    CodexExecArgs,
    PYTHON_SDK_ORIGINATOR,
    serialize_config_overrides,
)


class FakePopen:
    def __init__(
        self,
        command: list[str],
        env: dict[str, str],
        stdout_text: str = "",
        stderr_text: str = "",
        returncode: int = 0,
    ) -> None:
        self.command = command
        self.env = env
        self.stdin = io.StringIO()
        self.stdout = io.StringIO(stdout_text)
        self.stderr = io.StringIO(stderr_text)
        self._returncode = returncode

    def poll(self) -> int | None:
        return self._returncode

    def wait(self, timeout: float | None = None) -> int:
        _ = timeout
        return self._returncode

    def terminate(self) -> None:
        self._returncode = self._returncode if self._returncode is not None else -15

    def kill(self) -> None:
        self._returncode = self._returncode if self._returncode is not None else -9


def test_places_resume_args_before_image_args(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    def fake_popen(*args: Any, **kwargs: Any) -> FakePopen:
        captured["args"] = args
        captured["kwargs"] = kwargs
        return FakePopen(command=args[0], env=kwargs["env"], returncode=0)

    monkeypatch.setattr(subprocess, "Popen", fake_popen)

    exec_client = CodexExec(executable_path="codex")
    list(exec_client.run(CodexExecArgs(input="hi", images=["img.png"], thread_id="thread-id")))

    command_args = captured["args"][0][1:]
    resume_index = command_args.index("resume")
    image_index = command_args.index("--image")
    assert resume_index < image_index


def test_rejects_nonzero_exit(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_popen(*args: Any, **kwargs: Any) -> FakePopen:
        return FakePopen(
            command=args[0],
            env=kwargs["env"],
            stdout_text="",
            stderr_text="boom",
            returncode=2,
        )

    monkeypatch.setattr(subprocess, "Popen", fake_popen)
    exec_client = CodexExec(executable_path="codex")

    with pytest.raises(RuntimeError, match=r"Codex Exec exited with code 2: boom"):
        list(exec_client.run(CodexExecArgs(input="hi")))


def test_env_override_includes_required_and_does_not_leak(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}
    os.environ["CODEX_ENV_SHOULD_NOT_LEAK"] = "leak"

    def fake_popen(*args: Any, **kwargs: Any) -> FakePopen:
        captured["env"] = kwargs["env"]
        return FakePopen(command=args[0], env=kwargs["env"], returncode=0)

    monkeypatch.setattr(subprocess, "Popen", fake_popen)

    try:
        exec_client = CodexExec(executable_path="codex", env={"CUSTOM_ENV": "custom"})
        list(
            exec_client.run(
                CodexExecArgs(input="hi", base_url="https://example.test", api_key="secret-key")
            )
        )

        spawn_env = captured["env"]
        assert spawn_env["CUSTOM_ENV"] == "custom"
        assert "CODEX_ENV_SHOULD_NOT_LEAK" not in spawn_env
        assert spawn_env["OPENAI_BASE_URL"] == "https://example.test"
        assert spawn_env["CODEX_API_KEY"] == "secret-key"
        assert spawn_env["CODEX_INTERNAL_ORIGINATOR_OVERRIDE"] == PYTHON_SDK_ORIGINATOR
    finally:
        del os.environ["CODEX_ENV_SHOULD_NOT_LEAK"]


def test_serialize_config_overrides_as_toml_literals() -> None:
    overrides = serialize_config_overrides(
        {
            "approval_policy": "never",
            "sandbox_workspace_write": {"network_access": True},
            "retry_budget": 3,
            "tool_rules": {"allow": ["git status", "git diff"]},
        }
    )
    assert overrides == [
        'approval_policy="never"',
        "sandbox_workspace_write.network_access=true",
        "retry_budget=3",
        'tool_rules.allow=["git status", "git diff"]',
    ]
