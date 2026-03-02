from __future__ import annotations

from typing import Mapping

from .codex_options import CodexOptions, coerce_codex_options
from .exec import CodexExec
from .thread import Thread
from .thread_options import ThreadOptions, coerce_thread_options


class Codex:
    def __init__(self, options: CodexOptions | Mapping[str, object] | None = None) -> None:
        parsed_options = coerce_codex_options(options)
        self._exec = CodexExec(
            executable_path=parsed_options.codex_path_override,
            env=parsed_options.env,
            config_overrides=parsed_options.config,
        )
        self._options = parsed_options

    def start_thread(self, options: ThreadOptions | Mapping[str, object] | None = None) -> Thread:
        return Thread(self._exec, self._options, coerce_thread_options(options))

    def startThread(self, options: ThreadOptions | Mapping[str, object] | None = None) -> Thread:
        return self.start_thread(options)

    def resume_thread(
        self, thread_id: str, options: ThreadOptions | Mapping[str, object] | None = None
    ) -> Thread:
        return Thread(self._exec, self._options, coerce_thread_options(options), thread_id)

    def resumeThread(
        self, thread_id: str, options: ThreadOptions | Mapping[str, object] | None = None
    ) -> Thread:
        return self.resume_thread(thread_id, options)
