"""Custom exceptions used by the toolkit runtime."""


class AgentCliError(Exception):
    """Base exception for framework-level errors."""


class DuplicateToolError(AgentCliError):
    """Raised when two tool classes try to register the same name."""


class ToolNotFoundError(AgentCliError):
    """Raised when a requested tool does not exist in the registry."""


class ToolValidationError(AgentCliError):
    """Raised when a tool receives invalid user input or configuration."""


class StreamNotSupportedError(AgentCliError):
    """Raised when a caller asks a non-streaming tool to stream output."""

