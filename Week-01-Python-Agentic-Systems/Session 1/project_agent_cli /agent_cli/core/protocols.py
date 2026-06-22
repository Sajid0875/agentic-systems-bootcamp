"""Structural typing contracts for tools."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Protocol, runtime_checkable

from agent_cli.core.config import ToolConfig
from agent_cli.core.types import ToolContext, ToolMetadata, ToolOutput


@runtime_checkable
class ToolProtocol(Protocol):
    """A mypy-friendly contract for anything that behaves like a tool.

    The protocol lets the registry and CLI depend on behavior instead of a
    concrete base class. This is how larger frameworks stay extensible: user
    tools only need to satisfy a contract.
    """

    @property
    def name(self) -> str:
        """Registry-safe tool name."""

    @property
    def metadata(self) -> ToolMetadata:
        """Description and discovery metadata."""

    @property
    def config(self) -> ToolConfig:
        """Validated runtime configuration."""

    @property
    def mro_path(self) -> tuple[str, ...]:
        """Class resolution path used for educational introspection."""

    def execute(self, context: ToolContext) -> str:
        """Run the tool once and return a complete response."""

    def stream(self, context: ToolContext) -> Iterator[str]:
        """Yield response tokens incrementally."""

    def run(
        self,
        raw_input: str,
        *,
        stream: bool = False,
        session_id: str = "standalone",
    ) -> ToolOutput:
        """Validate input, execute the tool, and return a structured result."""
