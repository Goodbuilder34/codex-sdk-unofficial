from __future__ import annotations

import json
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .turn_options import UNSET


@dataclass(slots=True)
class OutputSchemaFile:
    schema_path: str | None
    cleanup: Callable[[], None]


def create_output_schema_file(schema: object) -> OutputSchemaFile:
    if schema is UNSET:
        return OutputSchemaFile(schema_path=None, cleanup=lambda: None)
    if not _is_json_object(schema):
        raise ValueError("output_schema must be a plain JSON object")

    schema_dir = Path(tempfile.mkdtemp(prefix="codex-output-schema-"))
    schema_path = schema_dir / "schema.json"

    def cleanup() -> None:
        try:
            shutil.rmtree(schema_dir, ignore_errors=True)
        except Exception:
            pass

    try:
        schema_path.write_text(json.dumps(schema), encoding="utf-8")
        return OutputSchemaFile(schema_path=str(schema_path), cleanup=cleanup)
    except Exception:
        cleanup()
        raise


def _is_json_object(value: object) -> bool:
    return isinstance(value, dict)
