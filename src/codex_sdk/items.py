from __future__ import annotations

from typing import Any, Literal, NotRequired, TypedDict, TypeAlias

CommandExecutionStatus: TypeAlias = Literal["in_progress", "completed", "failed"]
PatchChangeKind: TypeAlias = Literal["add", "delete", "update"]
PatchApplyStatus: TypeAlias = Literal["completed", "failed"]
McpToolCallStatus: TypeAlias = Literal["in_progress", "completed", "failed"]


class CommandExecutionItem(TypedDict):
    id: str
    type: Literal["command_execution"]
    command: str
    aggregated_output: str
    status: CommandExecutionStatus
    exit_code: NotRequired[int]


class FileUpdateChange(TypedDict):
    path: str
    kind: PatchChangeKind


class FileChangeItem(TypedDict):
    id: str
    type: Literal["file_change"]
    changes: list[FileUpdateChange]
    status: PatchApplyStatus


class McpToolCallResult(TypedDict):
    content: list[Any]
    structured_content: Any


class McpToolCallError(TypedDict):
    message: str


class McpToolCallItem(TypedDict):
    id: str
    type: Literal["mcp_tool_call"]
    server: str
    tool: str
    arguments: Any
    status: McpToolCallStatus
    result: NotRequired[McpToolCallResult]
    error: NotRequired[McpToolCallError]


class AgentMessageItem(TypedDict):
    id: str
    type: Literal["agent_message"]
    text: str


class ReasoningItem(TypedDict):
    id: str
    type: Literal["reasoning"]
    text: str


class WebSearchItem(TypedDict):
    id: str
    type: Literal["web_search"]
    query: str


class ErrorItem(TypedDict):
    id: str
    type: Literal["error"]
    message: str


class TodoItem(TypedDict):
    text: str
    completed: bool


class TodoListItem(TypedDict):
    id: str
    type: Literal["todo_list"]
    items: list[TodoItem]


ThreadItem: TypeAlias = (
    AgentMessageItem
    | ReasoningItem
    | CommandExecutionItem
    | FileChangeItem
    | McpToolCallItem
    | WebSearchItem
    | TodoListItem
    | ErrorItem
)
