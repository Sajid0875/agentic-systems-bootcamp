"""Small logging facade used by decorators, mixins, and sessions."""

from __future__ import annotations

from datetime import datetime, timezone
import sys


class FrameworkLogger:
    """A tiny stderr logger with a stable format for CLI applications."""

    __slots__ = ()

    @staticmethod
    def _write(level: str, message: str) -> None:
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        print(f"[{timestamp}] {level.upper():<7} {message}", file=sys.stderr)

    @classmethod
    def info(cls, message: str) -> None:
        """Write an informational log event."""

        cls._write("info", message)

    @classmethod
    def warning(cls, message: str) -> None:
        """Write a warning log event."""

        cls._write("warning", message)

    @classmethod
    def error(cls, message: str) -> None:
        """Write an error log event."""

        cls._write("error", message)

