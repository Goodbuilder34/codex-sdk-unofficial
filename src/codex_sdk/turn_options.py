from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol

UNSET = object()


class CancelSignal(Protocol):
    def is_set(self) -> bool:  # pragma: no cover - Protocol signature
        ...


@dataclass(slots=True)
class TurnOptions:
    output_schema: object = UNSET
    signal: CancelSignal | None = None


def coerce_turn_options(options: TurnOptions | Mapping[str, object] | None) -> TurnOptions:
    if options is None:
        return TurnOptions()
    if isinstance(options, TurnOptions):
        return options
    if isinstance(options, Mapping):
        if "output_schema" in options:
            schema = options["output_schema"]
        else:
            schema = options.get("outputSchema", UNSET)
        signal = options.get("signal")
        if signal is not None and not _is_signal_like(signal):
            raise TypeError("signal must expose is_set()")
        return TurnOptions(output_schema=schema, signal=signal)  # type: ignore[arg-type]
    raise TypeError("options must be TurnOptions, a mapping, or None")


def is_cancelled(signal: CancelSignal | None) -> bool:
    if signal is None:
        return False
    try:
        return bool(signal.is_set())
    except Exception:
        return False


def _is_signal_like(signal: object) -> bool:
    return hasattr(signal, "is_set") and callable(getattr(signal, "is_set"))
