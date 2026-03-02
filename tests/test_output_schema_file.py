from __future__ import annotations

import json
from pathlib import Path

from codex_sdk.output_schema_file import create_output_schema_file
from codex_sdk.turn_options import UNSET


def test_create_output_schema_file_writes_then_cleans() -> None:
    schema = {"type": "object", "properties": {"answer": {"type": "string"}}}
    output_schema_file = create_output_schema_file(schema)

    assert output_schema_file.schema_path is not None
    schema_path = Path(output_schema_file.schema_path)
    assert schema_path.exists()
    assert json.loads(schema_path.read_text(encoding="utf-8")) == schema

    output_schema_file.cleanup()
    assert not schema_path.exists()
    assert not schema_path.parent.exists()


def test_create_output_schema_file_unset_schema_is_noop() -> None:
    output_schema_file = create_output_schema_file(UNSET)
    assert output_schema_file.schema_path is None
    output_schema_file.cleanup()
