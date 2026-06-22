"""Deterministic search tool used for local CLI demos."""

from __future__ import annotations

from collections.abc import Iterator

from agent_cli.core import BaseTool
from agent_cli.core.types import ToolContext
from agent_cli.decorators import tool


@tool(
    tags=("retrieval", "search", "agent-tool"),
    examples=(
        "python descriptors in ai frameworks",
        "how langgraph uses tools",
    ),
)
class SearchTool(
    BaseTool,
    tool_name="search",
    description="Searches a small in-memory knowledge base and returns ranked notes.",
    streamable=True,
):
    """Search a local knowledge base without relying on network access."""

    __slots__ = ()

    _documents = (
        (
            "descriptors",
            "Descriptors validate configuration fields before tools execute.",
        ),
        (
            "protocols",
            "Protocols let agent runtimes accept any object with the right behavior.",
        ),
        (
            "streaming",
            "Generator-based streaming yields partial outputs for responsive agents.",
        ),
        (
            "registry",
            "__init_subclass__ can register tools as soon as classes are created.",
        ),
        (
            "cli",
            "A CLI exposes tool discovery, descriptions, and execution for operators.",
        ),
    )

    def execute(self, context: ToolContext) -> str:
        query_terms = {
            term.lower()
            for term in context["raw_input"].replace("-", " ").split()
            if len(term) > 2
        }

        scored: list[tuple[int, str, str]] = []
        for title, body in self._documents:
            haystack = f"{title} {body}".lower()
            score = sum(1 for term in query_terms if term in haystack)
            if score:
                scored.append((score, title, body))

        if not scored:
            return (
                "No exact local match found. Try terms like descriptors, "
                "protocols, streaming, registry, or cli."
            )

        scored.sort(key=lambda item: (-item[0], item[1]))
        lines = [
            f"{index}. {title}: {body}"
            for index, (_, title, body) in enumerate(scored[:3], start=1)
        ]
        return "\n".join(lines)

    def stream(self, context: ToolContext) -> Iterator[str]:
        for line in self.execute(context).splitlines():
            for token in line.split(" "):
                yield f"{token} "
            yield "\n"

