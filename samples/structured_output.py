from codex_sdk import Codex

schema = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "status": {"type": "string", "enum": ["ok", "action_required"]},
    },
    "required": ["summary", "status"],
    "additionalProperties": False,
}


def main() -> None:
    codex = Codex()
    thread = codex.start_thread()
    turn = thread.run("Summarize repository status", {"output_schema": schema})
    print(turn.final_response)


if __name__ == "__main__":
    main()
