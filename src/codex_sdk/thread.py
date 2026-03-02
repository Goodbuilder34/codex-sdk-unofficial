from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Iterator, Literal, Mapping, TypedDict, TypeAlias

from .codex_options import CodexOptions
from .events import ThreadEvent, ThreadError, Usage
from .exec import CodexExec, CodexExecArgs
from .items import ThreadItem
from .output_schema_file import create_output_schema_file
from .thread_options import ThreadOptions
from .turn_options import TurnOptions, coerce_turn_options


@dataclass(slots=True)
class Turn:
    items: list[ThreadItem]
    final_response: str
    usage: Usage | None

    @property
    def finalResponse(self) -> str:
        return self.final_response


RunResult: TypeAlias = Turn


@dataclass(slots=True)
class StreamedTurn:
    events: Iterator[ThreadEvent]


RunStreamedResult: TypeAlias = StreamedTurn


class TextUserInput(TypedDict):
    type: Literal["text"]
    text: str


class LocalImageUserInput(TypedDict):
    type: Literal["local_image"]
    path: str


UserInput: TypeAlias = TextUserInput | LocalImageUserInput
Input: TypeAlias = str | list[UserInput]


class Thread:
    def __init__(
        self,
        exec_client: CodexExec,
        codex_options: CodexOptions,
        thread_options: ThreadOptions,
        thread_id: str | None = None,
    ) -> None:
        self._exec = exec_client
        self._options = codex_options
        self._id = thread_id
        self._thread_options = thread_options

    @property
    def id(self) -> str | None:
        return self._id

    def run_streamed(self, input: Input, turn_options: TurnOptions | Mapping[str, object] | None = None) -> StreamedTurn:
        return StreamedTurn(events=self._run_streamed_internal(input, turn_options))

    def runStreamed(self, input: Input, turn_options: TurnOptions | Mapping[str, object] | None = None) -> StreamedTurn:
        return self.run_streamed(input, turn_options)

    def _run_streamed_internal(
        self, input: Input, turn_options: TurnOptions | Mapping[str, object] | None = None
    ) -> Iterator[ThreadEvent]:
        parsed_turn_options = coerce_turn_options(turn_options)
        schema_file = create_output_schema_file(parsed_turn_options.output_schema)
        prompt, images = normalize_input(input)

        options = self._thread_options
        generator = self._exec.run(
            CodexExecArgs(
                input=prompt,
                base_url=self._options.base_url,
                api_key=self._options.api_key,
                thread_id=self._id,
                images=images,
                model=options.model,
                sandbox_mode=options.sandbox_mode,
                working_directory=options.working_directory,
                skip_git_repo_check=options.skip_git_repo_check,
                output_schema_file=schema_file.schema_path,
                model_reasoning_effort=options.model_reasoning_effort,
                signal=parsed_turn_options.signal,
                network_access_enabled=options.network_access_enabled,
                web_search_mode=options.web_search_mode,
                web_search_enabled=options.web_search_enabled,
                approval_policy=options.approval_policy,
                additional_directories=options.additional_directories,
            )
        )

        try:
            for line in generator:
                try:
                    parsed = json.loads(line)
                except Exception as exc:
                    raise RuntimeError(f"Failed to parse item: {line}") from exc
                if not isinstance(parsed, dict):
                    raise RuntimeError(f"Unexpected event payload: {parsed!r}")
                if parsed.get("type") == "thread.started":
                    thread_id = parsed.get("thread_id")
                    if isinstance(thread_id, str):
                        self._id = thread_id
                yield parsed  # type: ignore[misc]
        finally:
            schema_file.cleanup()

    def run(self, input: Input, turn_options: TurnOptions | Mapping[str, object] | None = None) -> Turn:
        generator = self._run_streamed_internal(input, turn_options)
        items: list[ThreadItem] = []
        final_response = ""
        usage: Usage | None = None
        turn_failure: ThreadError | None = None

        for event in generator:
            event_type = event.get("type")
            if event_type == "item.completed":
                item = event.get("item")
                if isinstance(item, dict):
                    if item.get("type") == "agent_message":
                        text = item.get("text")
                        if isinstance(text, str):
                            final_response = text
                    items.append(item)  # type: ignore[arg-type]
            elif event_type == "turn.completed":
                event_usage = event.get("usage")
                if isinstance(event_usage, dict):
                    usage = event_usage  # type: ignore[assignment]
            elif event_type == "turn.failed":
                event_error = event.get("error")
                if isinstance(event_error, dict):
                    turn_failure = event_error  # type: ignore[assignment]
                break

        if turn_failure is not None:
            message = turn_failure.get("message")
            raise RuntimeError(message if isinstance(message, str) else "Turn failed")

        return Turn(items=items, final_response=final_response, usage=usage)


def normalize_input(input: Input) -> tuple[str, list[str]]:
    if isinstance(input, str):
        return input, []

    prompt_parts: list[str] = []
    images: list[str] = []
    for item in input:
        kind = item.get("type")
        if kind == "text":
            text = item.get("text")
            if isinstance(text, str):
                prompt_parts.append(text)
        elif kind == "local_image":
            path = item.get("path")
            if isinstance(path, str):
                images.append(path)
    return "\n\n".join(prompt_parts), images
