from __future__ import annotations

import json

import pytest

from codex_sdk.codex_options import CodexOptions
from codex_sdk.thread import Thread, normalize_input
from codex_sdk.thread_options import ThreadOptions


class FakeExec:
    def __init__(self, lines: list[str]) -> None:
        self.lines = lines
        self.calls = []

    def run(self, args):  # noqa: ANN001
        self.calls.append(args)
        for line in self.lines:
            yield line


def test_run_returns_items_usage_and_final_response() -> None:
    fake_exec = FakeExec(
        [
            json.dumps({"type": "thread.started", "thread_id": "thread_123"}),
            json.dumps({"type": "turn.started"}),
            json.dumps(
                {
                    "type": "item.completed",
                    "item": {"id": "item_1", "type": "agent_message", "text": "Hi!"},
                }
            ),
            json.dumps(
                {
                    "type": "turn.completed",
                    "usage": {
                        "cached_input_tokens": 12,
                        "input_tokens": 42,
                        "output_tokens": 5,
                    },
                }
            ),
        ]
    )
    thread = Thread(fake_exec, CodexOptions(base_url="http://base"), ThreadOptions(model="gpt-5"))

    result = thread.run("Hello")

    assert thread.id == "thread_123"
    assert result.final_response == "Hi!"
    assert result.items == [{"id": "item_1", "type": "agent_message", "text": "Hi!"}]
    assert result.usage == {
        "cached_input_tokens": 12,
        "input_tokens": 42,
        "output_tokens": 5,
    }
    assert fake_exec.calls[0].model == "gpt-5"
    assert fake_exec.calls[0].base_url == "http://base"


def test_run_raises_on_turn_failure() -> None:
    fake_exec = FakeExec(
        [
            json.dumps({"type": "thread.started", "thread_id": "thread_123"}),
            json.dumps({"type": "turn.failed", "error": {"message": "rate limit exceeded"}}),
        ]
    )
    thread = Thread(fake_exec, CodexOptions(), ThreadOptions())

    with pytest.raises(RuntimeError, match="rate limit exceeded"):
        thread.run("fail")


def test_run_streamed_uses_existing_thread_id() -> None:
    fake_exec = FakeExec(
        [
            json.dumps({"type": "turn.started"}),
            json.dumps(
                {
                    "type": "turn.completed",
                    "usage": {
                        "cached_input_tokens": 0,
                        "input_tokens": 1,
                        "output_tokens": 1,
                    },
                }
            ),
        ]
    )
    thread = Thread(fake_exec, CodexOptions(), ThreadOptions(), thread_id="thread_saved")

    streamed = thread.run_streamed("continue")
    list(streamed.events)

    assert fake_exec.calls[0].thread_id == "thread_saved"


def test_run_stream_true_streams_agent_message_text_without_duplicates(
    capsys: pytest.CaptureFixture[str],
) -> None:
    fake_exec = FakeExec(
        [
            json.dumps({"type": "thread.started", "thread_id": "thread_123"}),
            json.dumps(
                {
                    "type": "item.updated",
                    "item": {"id": "item_1", "type": "agent_message", "text": "Hel"},
                }
            ),
            json.dumps(
                {
                    "type": "item.updated",
                    "item": {"id": "item_1", "type": "agent_message", "text": "Hello"},
                }
            ),
            json.dumps(
                {
                    "type": "item.updated",
                    "item": {"id": "item_1", "type": "agent_message", "text": "Hello"},
                }
            ),
            json.dumps(
                {
                    "type": "item.completed",
                    "item": {"id": "item_1", "type": "agent_message", "text": "Hello!"},
                }
            ),
            json.dumps(
                {
                    "type": "turn.completed",
                    "usage": {
                        "cached_input_tokens": 1,
                        "input_tokens": 2,
                        "output_tokens": 3,
                    },
                }
            ),
        ]
    )
    thread = Thread(fake_exec, CodexOptions(), ThreadOptions())

    result = thread.run("Hello", stream=True)

    captured = capsys.readouterr()
    assert captured.out == "Hello!\n"
    assert result.final_response == "Hello!"
    assert result.items == [{"id": "item_1", "type": "agent_message", "text": "Hello!"}]
    assert result.usage == {
        "cached_input_tokens": 1,
        "input_tokens": 2,
        "output_tokens": 3,
    }


def test_run_default_stream_false_prints_nothing(
    capsys: pytest.CaptureFixture[str],
) -> None:
    fake_exec = FakeExec(
        [
            json.dumps({"type": "thread.started", "thread_id": "thread_123"}),
            json.dumps(
                {
                    "type": "item.updated",
                    "item": {"id": "item_1", "type": "agent_message", "text": "Hi"},
                }
            ),
            json.dumps(
                {
                    "type": "item.completed",
                    "item": {"id": "item_1", "type": "agent_message", "text": "Hi there"},
                }
            ),
            json.dumps(
                {
                    "type": "turn.completed",
                    "usage": {
                        "cached_input_tokens": 0,
                        "input_tokens": 2,
                        "output_tokens": 2,
                    },
                }
            ),
        ]
    )
    thread = Thread(fake_exec, CodexOptions(), ThreadOptions())

    result = thread.run("Hello")

    captured = capsys.readouterr()
    assert captured.out == ""
    assert result.final_response == "Hi there"
    assert result.items == [{"id": "item_1", "type": "agent_message", "text": "Hi there"}]


def test_run_stream_true_raises_on_turn_failure_and_appends_newline(
    capsys: pytest.CaptureFixture[str],
) -> None:
    fake_exec = FakeExec(
        [
            json.dumps({"type": "thread.started", "thread_id": "thread_123"}),
            json.dumps(
                {
                    "type": "item.updated",
                    "item": {"id": "item_1", "type": "agent_message", "text": "Working..."},
                }
            ),
            json.dumps({"type": "turn.failed", "error": {"message": "rate limit exceeded"}}),
        ]
    )
    thread = Thread(fake_exec, CodexOptions(), ThreadOptions())

    with pytest.raises(RuntimeError, match="rate limit exceeded"):
        thread.run("fail", stream=True)

    captured = capsys.readouterr()
    assert captured.out == "Working...\n"


def test_run_stream_true_does_not_append_extra_newline(
    capsys: pytest.CaptureFixture[str],
) -> None:
    fake_exec = FakeExec(
        [
            json.dumps({"type": "thread.started", "thread_id": "thread_123"}),
            json.dumps(
                {
                    "type": "item.updated",
                    "item": {"id": "item_1", "type": "agent_message", "text": "Done\n"},
                }
            ),
            json.dumps(
                {
                    "type": "item.completed",
                    "item": {"id": "item_1", "type": "agent_message", "text": "Done\n"},
                }
            ),
            json.dumps(
                {
                    "type": "turn.completed",
                    "usage": {
                        "cached_input_tokens": 0,
                        "input_tokens": 1,
                        "output_tokens": 1,
                    },
                }
            ),
        ]
    )
    thread = Thread(fake_exec, CodexOptions(), ThreadOptions())

    result = thread.run("finish", stream=True)

    captured = capsys.readouterr()
    assert captured.out == "Done\n"
    assert result.final_response == "Done\n"


def test_normalize_input_combines_text_and_extracts_images() -> None:
    prompt, images = normalize_input(
        [
            {"type": "text", "text": "Describe file changes"},
            {"type": "text", "text": "Focus on impacted tests"},
            {"type": "local_image", "path": "/tmp/a.png"},
            {"type": "local_image", "path": "/tmp/b.jpg"},
        ]
    )

    assert prompt == "Describe file changes\n\nFocus on impacted tests"
    assert images == ["/tmp/a.png", "/tmp/b.jpg"]
