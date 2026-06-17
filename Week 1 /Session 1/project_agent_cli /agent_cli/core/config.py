"""Validated configuration objects for tools."""

from __future__ import annotations

from typing import Any

from agent_cli.descriptors import BooleanField, FloatRange, IdentifierField, IntegerRange


class ToolConfig:
    """Runtime configuration for a tool instance.

    Descriptors enforce invariants at assignment time. The object is slotted so
    config state stays compact and accidental attributes fail loudly.
    """

    __slots__ = ("_retries", "_streaming_enabled", "_timeout", "_tool_name")

    tool_name: str = IdentifierField()
    retries: int = IntegerRange(0, 5, default=1)
    timeout: float = FloatRange(0.1, 120.0, default=10.0)
    streaming_enabled: bool = BooleanField(default=True)

    def __init__(
        self,
        *,
        tool_name: str,
        retries: int = 1,
        timeout: float = 10.0,
        streaming_enabled: bool = True,
    ) -> None:
        self.tool_name = tool_name
        self.retries = retries
        self.timeout = timeout
        self.streaming_enabled = streaming_enabled

    @property
    def max_attempts(self) -> int:
        """Total attempts including the first call."""

        return self.retries + 1

    @property
    def reliability_profile(self) -> str:
        """Read-only metadata computed from retry and timeout settings."""

        if self.retries >= 3 and self.timeout >= 15:
            return "resilient"
        if self.retries == 0:
            return "fast-fail"
        return "balanced"

    def as_dict(self) -> dict[str, Any]:
        """Return config as a serializable dictionary."""

        return {
            "tool_name": self.tool_name,
            "retries": self.retries,
            "timeout": self.timeout,
            "streaming_enabled": self.streaming_enabled,
            "max_attempts": self.max_attempts,
            "reliability_profile": self.reliability_profile,
        }

    def __repr__(self) -> str:
        return (
            "ToolConfig("
            f"tool_name={self.tool_name!r}, "
            f"retries={self.retries}, "
            f"timeout={self.timeout}, "
            f"streaming_enabled={self.streaming_enabled}"
            ")"
        )

    def __str__(self) -> str:
        return f"{self.tool_name} config ({self.reliability_profile})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ToolConfig):
            return NotImplemented
        return self.as_dict() == other.as_dict()

    def __len__(self) -> int:
        return 4

