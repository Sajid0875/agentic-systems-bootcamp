"""Small deterministic translation tool."""

from __future__ import annotations

from collections.abc import Iterator

from agent_cli.core import BaseTool
from agent_cli.core.types import ToolContext
from agent_cli.decorators import tool


@tool(
    tags=("translation", "text", "agent-tool"),
    examples=(
        "es::hello agent framework",
        "ur::python tool",
    ),
)
class TranslateTool(
    BaseTool,
    tool_name="translate",
    description="Translates common demo phrases to Spanish or Urdu using a local lexicon.",
    streamable=True,
):
    """Translate a small set of common learning phrases."""

    __slots__ = ()

    _lexicons = {
        "es": {
            "hello": "hola",
            "agent": "agente",
            "framework": "marco",
            "python": "python",
            "tool": "herramienta",
            "search": "busqueda",
            "summary": "resumen",
            "translate": "traducir",
            "typing": "tipado",
        },
        "ur": {
            "hello": "salam",
            "agent": "agent",
            "framework": "framework",
            "python": "python",
            "tool": "tool",
            "search": "talash",
            "summary": "khulasa",
            "translate": "tarjuma",
            "typing": "typing",
        },
    }

    def execute(self, context: ToolContext) -> str:
        target_language, text = self._parse_input(context["raw_input"])
        lexicon = self._lexicons[target_language]
        translated_words = [
            lexicon.get(word.lower().strip(".,!?"), word)
            for word in text.split()
        ]
        return f"{target_language}: {' '.join(translated_words)}"

    def stream(self, context: ToolContext) -> Iterator[str]:
        for token in self.execute(context).split(" "):
            yield f"{token} "

    def _parse_input(self, raw_input: str) -> tuple[str, str]:
        if "::" in raw_input:
            language, text = raw_input.split("::", maxsplit=1)
            language = language.strip().lower()
            text = text.strip()
        else:
            language = "es"
            text = raw_input.strip()

        if language not in self._lexicons:
            supported = ", ".join(sorted(self._lexicons))
            raise ValueError(f"unsupported language {language!r}; choose one of: {supported}")

        if not text:
            raise ValueError("translation input cannot be empty")

        return language, text

