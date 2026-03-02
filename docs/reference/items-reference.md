# Items Reference

`ThreadItem` can be one of:

- `agent_message` (`id`, `text`)
- `reasoning` (`id`, `text`)
- `command_execution` (`command`, `aggregated_output`, `status`, optional `exit_code`)
- `file_change` (`changes`, `status`)
- `mcp_tool_call` (`server`, `tool`, `arguments`, optional `result`/`error`)
- `web_search` (`query`)
- `todo_list` (`items[]`)
- `error` (`message`)

## Example Handler

```python
def handle_item(item: dict):
    t = item.get("type")
    if t == "agent_message":
        print(item.get("text"))
    elif t == "command_execution":
        print(item.get("command"), item.get("status"))
```
