"""Execution session context manager."""

from __future__ import annotations

from time import perf_counter
from types import TracebackType
from typing import Any
from uuid import uuid4

from agent_cli.core.types import ToolContext
from agent_cli.utils import FrameworkLogger


class ExecutionSession:
    """Context manager for a single CLI or agent execution session."""

    __slots__ = ("_closed", "_resources", "_started_at", "session_id")

    def __init__(self, session_id: str | None = None) -> None:
        self.session_id = session_id or f"session-{uuid4().hex[:10]}"
        self._resources: list[str] = []
        self._started_at = 0.0
        self._closed = False

    def __enter__(self) -> ExecutionSession:
        self._started_at = perf_counter()
        FrameworkLogger.info(f"session {self.session_id} started")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        self.cleanup()
        duration_ms = (perf_counter() - self._started_at) * 1000
        if exc_value is None:
            FrameworkLogger.info(
                f"session {self.session_id} ended in {duration_ms:.2f} ms"
            )
        else:
            FrameworkLogger.error(
                f"session {self.session_id} failed after "
                f"{duration_ms:.2f} ms: {exc_value}"
            )
        return False

    @property
    def closed(self) -> bool:
        """Whether cleanup has already happened."""

        return self._closed

    def add_resource(self, name: str) -> None:
        """Track a logical resource for cleanup."""

        self._resources.append(name)

    def build_context(
        self,
        raw_input: str,
        *,
        metadata: dict[str, str] | None = None,
    ) -> ToolContext:
        """Build a typed execution context for a tool."""

        return {
            "raw_input": raw_input,
            "session_id": self.session_id,
            "metadata": metadata or {},
        }

    def cleanup(self) -> None:
        """Release tracked resources.

        The sample framework tracks logical names rather than open sockets or
        file handles, but the pattern is the same as production resource cleanup.
        """

        if self._closed:
            return

        for resource in reversed(self._resources):
            FrameworkLogger.info(f"session {self.session_id} released {resource}")

        self._resources.clear()
        self._closed = True

    def __repr__(self) -> str:
        state = "closed" if self.closed else "open"
        return f"ExecutionSession(session_id={self.session_id!r}, state={state!r})"

    def __str__(self) -> str:
        return self.session_id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExecutionSession):
            return NotImplemented
        return self.session_id == other.session_id

    def __len__(self) -> int:
        return len(self._resources)

