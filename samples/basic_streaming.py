from codex_sdk import Codex


def main() -> None:
    codex = Codex()
    thread = codex.start_thread()

    while True:
        prompt = input("> ").strip()
        if not prompt:
            continue

        streamed = thread.run_streamed(prompt)
        for event in streamed.events:
            event_type = event.get("type")
            if event_type == "item.completed":
                item = event.get("item", {})
                if isinstance(item, dict) and item.get("type") == "agent_message":
                    print(f"Assistant: {item.get('text', '')}")
            elif event_type == "turn.completed":
                usage = event.get("usage", {})
                print(
                    "Usage:",
                    usage.get("input_tokens"),
                    "input,",
                    usage.get("cached_input_tokens"),
                    "cached,",
                    usage.get("output_tokens"),
                    "output",
                )
            elif event_type == "turn.failed":
                error = event.get("error", {})
                print("Turn failed:", error.get("message"))


if __name__ == "__main__":
    main()
