"""Base class for all framework tools."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from time import perf_counter
from typing import Any, ClassVar

from agent_cli.core.config import ToolConfig
from agent_cli.core.exceptions import StreamNotSupportedError, ToolValidationError
from agent_cli.core.metrics import ToolMetrics
from agent_cli.core.mixins import LoggingMixin, MetricsMixin, RetryMixin
from agent_cli.core.registry import ToolRegistry
from agent_cli.core.types import ToolContext, ToolMetadata, ToolOutput
from agent_cli.decorators import log_execution, measure_time


class BaseTool(LoggingMixin, RetryMixin, MetricsMixin, ABC):
    """Base class that gives tools registration, config, and execution flow."""

    __slots__ = ("_metrics", "config")

    _tool_name: ClassVar[str]
    _tool_tags: ClassVar[tuple[str, ...]] = ()
    _tool_examples: ClassVar[tuple[str, ...]] = ()
    _streamable: ClassVar[bool] = False
    description: ClassVar[str] = ""

    def __init_subclass__(
        cls,
        *,
        tool_name: str | None = None,
        description: str = "",
        streamable: bool = False,
        abstract: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init_subclass__(**kwargs)
        if abstract:
            return

        if tool_name is None:
            raise TypeError(f"{cls.__name__} must define tool_name='...'")

        normalized_name = tool_name.strip().lower()
        if not normalized_name:
            raise ToolValidationError(f"{cls.__name__} received an empty tool name")

        cls._tool_name = normalized_name
        cls.description = description.strip()
        cls._streamable = streamable
        ToolRegistry.register(normalized_name, cls)

    def __init__(
        self,
        *,
        retries: int = 1,
        timeout: float = 10.0,
        streaming_enabled: bool = True,
    ) -> None:
        self.config = ToolConfig(
            tool_name=self.name,
            retries=retries,
            timeout=timeout,
            streaming_enabled=streaming_enabled,
        )
        self._metrics = ToolMetrics()

    @property
    def name(self) -> str:
        """Stable registry name for this tool."""

        return self._tool_name

    @property
    def metadata(self) -> ToolMetadata:
        """Public metadata used by the CLI and future planners."""

        return {
            "name": self.name,
            "description": self.description,
            "tags": self._tool_tags,
            "examples": self._tool_examples,
            "streamable": self.is_streaming_available,
        }

    @property
    def is_streaming_available(self) -> bool:
        """Whether this tool supports token streaming."""

        return self._streamable and self.config.streaming_enabled

    @property
    def mro_path(self) -> tuple[str, ...]:
        """Read-only view of the class resolution order."""

        return tuple(cls.__name__ for cls in self.__class__.mro())

    @abstractmethod
    def execute(self, context: ToolContext) -> str:
        """Run the concrete tool and return a complete response."""

    def stream(self, context: ToolContext) -> Iterator[str]:
        """Default streaming behavior that yields space-preserving tokens."""

        if not self.is_streaming_available:
            raise StreamNotSupportedError(f"{self.name} does not support streaming")

        for token in self.execute(context).split(" "):
            yield f"{token} "

    @log_execution
    @measure_time
    def run(
        self,
        raw_input: str,
        *,
        stream: bool = False,
        session_id: str = "standalone",
    ) -> ToolOutput:
        """Validate input, run the tool, and return structured output."""

        context = self._build_context(raw_input, session_id=session_id)
        started_at = perf_counter()
        failed = False
        try:
            if stream:
                if not self.is_streaming_available:
                    raise StreamNotSupportedError(
                        f"{self.name} was asked to stream but streaming is disabled"
                    )
                tokens = self.with_retries(lambda: list(self.stream(context)))
                content = "".join(tokens).strip()
            else:
                content = self.with_retries(lambda: self.execute(context))
                tokens = self._tokenize(content)

            return {
                "tool": self.name,
                "content": content,
                "tokens": tokens,
                "duration_ms": (perf_counter() - started_at) * 1000,
                "session_id": session_id,
            }
        except Exception:
            failed = True
            raise
        finally:
            self.record_metric(
                duration_ms=(perf_counter() - started_at) * 1000,
                failed=failed,
            )

    def _build_context(self, raw_input: str, *, session_id: str) -> ToolContext:
        cleaned = raw_input.strip()
        if not cleaned:
            raise ToolValidationError(f"{self.name} requires non-empty input")

        return {
            "raw_input": cleaned,
            "session_id": session_id,
            "metadata": {"tool": self.name},
        }

    def _tokenize(self, content: str) -> list[str]:
        return content.split()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name={self.name!r}, "
            f"config={self.config!r}, "
            f"metrics={self.metrics!r}"
            ")"
        )

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseTool):
            return NotImplemented
        return self.name == other.name and self.config == other.config

    def __len__(self) -> int:
        return len(self.metadata["examples"])
