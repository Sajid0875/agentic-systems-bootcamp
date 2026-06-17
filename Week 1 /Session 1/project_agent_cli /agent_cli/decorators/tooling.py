"""Class decorator for attaching discovery metadata to tools."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, TypeVar

C = TypeVar("C", bound=type[Any])


def tool(
    *,
    tags: Sequence[str] = (),
    examples: Sequence[str] = (),
) -> Any:
    """Attach agent-discovery metadata to a class-based tool.

    Registration still happens in ``BaseTool.__init_subclass__``. The decorator
    layers extra metadata onto the class after Python creates it, similar to how
    real frameworks combine class hooks and decorators.
    """

    def decorate(cls: C) -> C:
        normalized_tags = tuple(tag.strip().lower() for tag in tags if tag.strip())
        normalized_examples = tuple(example.strip() for example in examples if example.strip())
        setattr(cls, "_tool_tags", normalized_tags)
        setattr(cls, "_tool_examples", normalized_examples)
        return cls

    return decorate

