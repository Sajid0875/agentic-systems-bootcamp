"""Text summarization tool with deterministic extractive behavior."""

from __future__ import annotations

from collections.abc import Iterator

from agent_cli.core import BaseTool
from agent_cli.core.types import ToolContext
from agent_cli.decorators import tool


@tool(
    tags=("summarization", "text", "agent-tool"),
    examples=(
        "Agent frameworks register tools, validate inputs, and stream responses.",
        "Python descriptors and protocols make framework internals safer.",
    ),
)
class SummarizeTool(
    BaseTool,
    tool_name="summarize",
    description="Creates a compact extractive summary of user-provided text.",
    streamable=True,
):
    """Summarize text by selecting the most informative sentence."""

    __slots__ = ()

    def execute(self, context: ToolContext) -> str:
        text = context["raw_input"]
        sentences = self._split_sentences(text)
        chosen = max(sentences, key=lambda sentence: (len(set(sentence.split())), len(sentence)))
        word_count = len(text.split())
        return f"Summary ({word_count} words): {chosen}"

    def stream(self, context: ToolContext) -> Iterator[str]:
        for token in self.execute(context).split(" "):
            yield f"{token} "

    def _split_sentences(self, text: str) -> list[str]:
        normalized = text.replace("?", ".").replace("!", ".")
        sentences = [sentence.strip() for sentence in normalized.split(".") if sentence.strip()]
        if sentences:
            return sentences
        return [text.strip()]

