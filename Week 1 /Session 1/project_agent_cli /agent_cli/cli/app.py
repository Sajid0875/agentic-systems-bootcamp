"""Argparse-powered CLI for the Agent-Ready CLI Toolkit."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from agent_cli.core import ExecutionSession, ToolRegistry
from agent_cli.core.exceptions import AgentCliError


def build_parser() -> argparse.ArgumentParser:
    """Build the command parser."""

    parser = argparse.ArgumentParser(
        prog="python main.py",
        description="Agent-Ready CLI Toolkit",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list-tools", help="List registered tools")

    describe_parser = subparsers.add_parser("describe", help="Describe a tool")
    describe_parser.add_argument("tool_name", help="Registered tool name")

    run_parser = subparsers.add_parser("run", help="Run a tool")
    run_parser.add_argument("tool_name", help="Registered tool name")
    run_parser.add_argument(
        "tool_input",
        nargs="*",
        help="Input text. If omitted, stdin or an interactive prompt is used.",
    )
    run_parser.add_argument(
        "--stream",
        action="store_true",
        help="Use the tool's generator-based streaming mode",
    )
    run_parser.add_argument("--retries", type=int, default=1, help="Retry count")
    run_parser.add_argument("--timeout", type=float, default=10.0, help="Timeout metadata")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return an exit code."""

    _load_builtin_tools()
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "list-tools":
            _list_tools()
        elif args.command == "describe":
            _describe_tool(args.tool_name)
        elif args.command == "run":
            _run_tool(args)
        else:
            parser.error(f"unknown command {args.command!r}")
    except AgentCliError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    return 0


def _load_builtin_tools() -> None:
    import agent_cli.tools  # noqa: F401


def _list_tools() -> None:
    for name, tool_cls in ToolRegistry.items():
        tool = tool_cls()
        print(f"{name:<12} {tool.metadata['description']}")


def _describe_tool(tool_name: str) -> None:
    tool = ToolRegistry.create(tool_name)
    metadata = tool.metadata
    print(f"Name: {metadata['name']}")
    print(f"Description: {metadata['description']}")
    print(f"Streamable: {metadata['streamable']}")
    print(f"Tags: {', '.join(metadata['tags']) or 'none'}")
    print("Examples:")
    for example in metadata["examples"]:
        print(f"  - {example}")
    print(f"MRO: {' -> '.join(tool.mro_path)}")
    print(f"Config: {tool.config}")


def _run_tool(args: argparse.Namespace) -> None:
    raw_input = _resolve_input(args.tool_input)
    tool = ToolRegistry.create(
        args.tool_name,
        retries=args.retries,
        timeout=args.timeout,
    )

    with ExecutionSession() as session:
        session.add_resource(f"{tool.name}-runtime")
        result = tool.run(raw_input, stream=args.stream, session_id=session.session_id)

    if args.stream:
        print("".join(result["tokens"]).strip())
    else:
        print(result["content"])

    print(
        f"\n[{result['tool']}] "
        f"{len(result['tokens'])} token(s), "
        f"{result['duration_ms']:.2f} ms, "
        f"session={result['session_id']}"
    )


def _resolve_input(parts: list[str]) -> str:
    if parts:
        return " ".join(parts)

    if not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        if data:
            return data

    return input("Input: ").strip()


if __name__ == "__main__":
    raise SystemExit(main())

