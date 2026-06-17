"""Global tool registry powered by ``__init_subclass__``."""

from __future__ import annotations

from typing import Any, cast

from agent_cli.core.exceptions import DuplicateToolError, ToolNotFoundError
from agent_cli.core.protocols import ToolProtocol


class ToolRegistry:
    """In-memory registry of tool classes.

    The registry is intentionally global because agent frameworks need one
    discoverable catalog that planners, CLIs, and execution runtimes can query.
    """

    __slots__ = ()

    _tools: dict[str, type[Any]] = {}

    @classmethod
    def register(cls, name: str, tool_cls: type[Any]) -> None:
        """Register a tool class under a normalized name."""

        existing = cls._tools.get(name)
        if existing is not None and existing is not tool_cls:
            raise DuplicateToolError(
                f"tool name {name!r} is already registered by {existing.__name__}"
            )

        cls._tools[name] = tool_cls

    @classmethod
    def get(cls, name: str) -> type[Any]:
        """Return a tool class by name."""

        try:
            return cls._tools[name]
        except KeyError as error:
            available = ", ".join(cls.names()) or "none"
            raise ToolNotFoundError(
                f"unknown tool {name!r}; available tools: {available}"
            ) from error

    @classmethod
    def create(cls, name: str, **kwargs: Any) -> ToolProtocol:
        """Instantiate a registered tool."""

        tool_cls = cls.get(name)
        return cast(ToolProtocol, tool_cls(**kwargs))

    @classmethod
    def names(cls) -> tuple[str, ...]:
        """Return registered tool names in deterministic order."""

        return tuple(sorted(cls._tools))

    @classmethod
    def items(cls) -> tuple[tuple[str, type[Any]], ...]:
        """Return registry items in deterministic order."""

        return tuple((name, cls._tools[name]) for name in cls.names())

    @classmethod
    def clear(cls) -> None:
        """Clear the registry.

        This is useful in tests and mirrors how plugin systems isolate test
        cases. Application code should normally import tools instead.
        """

        cls._tools.clear()

    @classmethod
    def __len__(cls) -> int:
        return len(cls._tools)

