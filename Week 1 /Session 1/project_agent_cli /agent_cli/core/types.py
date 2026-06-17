"""TypedDict models shared across the framework.

These models intentionally stay small. They mirror the contract objects you
see in AI frameworks: a runtime context enters a tool, a structured result
comes back, and metadata makes tools discoverable by agents or CLIs.
"""

from __future__ import annotations

from typing import TypedDict


class ToolContext(TypedDict):
    """Runtime data passed into a tool execution."""

    raw_input: str
    session_id: str
    metadata: dict[str, str]


class ToolOutput(TypedDict):
    """Structured output returned from every tool run."""

    tool: str
    content: str
    tokens: list[str]
    duration_ms: float
    session_id: str


class ToolMetadata(TypedDict):
    """Public metadata used by the CLI and by future agent planners."""

    name: str
    description: str
    tags: tuple[str, ...]
    examples: tuple[str, ...]
    streamable: bool

