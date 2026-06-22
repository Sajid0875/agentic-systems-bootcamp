"""Unit tests for registry, descriptors, execution, and streaming."""

from __future__ import annotations

import unittest

import agent_cli.tools  # noqa: F401
from agent_cli.core import ToolConfig, ToolRegistry
from agent_cli.core.exceptions import StreamNotSupportedError, ToolValidationError


class ToolRegistryTests(unittest.TestCase):
    def test_builtin_tools_register_automatically(self) -> None:
        self.assertEqual(("search", "summarize", "translate"), ToolRegistry.names())

    def test_registry_creates_protocol_compatible_tool(self) -> None:
        tool = ToolRegistry.create("summarize")
        result = tool.run("Python protocols make tools easier to test.")

        self.assertEqual(result["tool"], "summarize")
        self.assertIn("Summary", result["content"])


class DescriptorConfigTests(unittest.TestCase):
    def test_config_validates_descriptor_fields(self) -> None:
        config = ToolConfig(tool_name="search", retries=3, timeout=20.0)

        self.assertEqual("resilient", config.reliability_profile)
        self.assertEqual(4, len(config))

    def test_invalid_config_fails_fast(self) -> None:
        with self.assertRaises(ValueError):
            ToolConfig(tool_name="Bad Name", retries=1, timeout=10.0)

        with self.assertRaises(ValueError):
            ToolConfig(tool_name="search", retries=9, timeout=10.0)


class ToolExecutionTests(unittest.TestCase):
    def test_streaming_uses_generator_tokens(self) -> None:
        tool = ToolRegistry.create("translate")
        result = tool.run("es::hello agent framework", stream=True)

        self.assertEqual("es: hola agente marco", result["content"])
        self.assertGreater(len(result["tokens"]), 1)

    def test_empty_input_is_rejected(self) -> None:
        tool = ToolRegistry.create("search")

        with self.assertRaises(ToolValidationError):
            tool.run("   ")

    def test_streaming_can_be_disabled_per_instance(self) -> None:
        tool = ToolRegistry.create("search", streaming_enabled=False)

        with self.assertRaises(StreamNotSupportedError):
            tool.run("descriptors", stream=True)


if __name__ == "__main__":
    unittest.main()

