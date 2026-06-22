"""Mixin behavior used by tool classes.

The base class combines these mixins through normal Python MRO. Each mixin owns
one cross-cutting concern, which keeps the execution code readable.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar

from agent_cli.core.metrics import ToolMetrics
from agent_cli.utils import FrameworkLogger

R = TypeVar("R")


class LoggingMixin:
    """Adds framework logging helpers."""

    __slots__ = ()

    @property
    def name(self) -> str:
        return getattr(self, "_tool_name", self.__class__.__name__.lower())

    def log(self, message: str) -> None:
        """Write a tool-scoped log message."""

        FrameworkLogger.info(f"{self.name}: {message}")


class RetryMixin:
    """Retries transient failures according to the tool configuration."""

    __slots__ = ()

    config: Any

    def with_retries(self, operation: Callable[[], R]) -> R:
        """Run an operation with retry semantics."""

        last_error: Exception | None = None
        for attempt in range(1, self.config.max_attempts + 1):
            try:
                return operation()
            except Exception as error:
                last_error = error
                FrameworkLogger.warning(
                    f"{self.config.tool_name}: attempt "
                    f"{attempt}/{self.config.max_attempts} failed: {error}"
                )

        if last_error is None:
            raise RuntimeError("retry loop exited without running operation")

        raise last_error


class MetricsMixin:
    """Adds metrics recording to tools."""

    __slots__ = ()

    _metrics: ToolMetrics

    @property
    def metrics(self) -> ToolMetrics:
        """Execution metrics for this tool instance."""

        return self._metrics

    def record_metric(self, *, duration_ms: float, failed: bool = False) -> None:
        """Record a tool execution outcome."""

        self._metrics.record(duration_ms=duration_ms, failed=failed)
