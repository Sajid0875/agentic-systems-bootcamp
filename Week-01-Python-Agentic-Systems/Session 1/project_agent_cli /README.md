# Agent-Ready CLI Toolkit

A portfolio-grade mini Python framework that models the internal shape of modern agent frameworks: typed tool contracts, automatic registration, decorators, context-managed execution, streaming output, validated configuration, mixins, and a CLI.

## Run It

```bash
python main.py list-tools
python main.py describe search
python main.py run search python descriptors registry
python main.py run summarize "Agent frameworks register tools and stream results." --stream
python main.py run translate es::hello agent framework
```

On systems where `python` is not available, use `python3` with the same commands.

Run tests:

```bash
python -m unittest discover -s agent_cli/tests
```

## Architecture

```text
agent_cli/
├── core/          # Tool base class, registry, protocols, session, config, mixins
├── tools/         # SearchTool, SummarizeTool, TranslateTool
├── decorators/    # @tool, @log_execution, @measure_time
├── descriptors/   # Validated descriptor fields
├── cli/           # argparse interface
├── utils/         # framework logger
└── tests/         # unittest coverage
```

## Python Concepts Used

`__init_subclass__`: `BaseTool` registers each concrete subclass automatically. This is the central plugin-like mechanism.

`Protocol`: `ToolProtocol` defines the structural interface expected by the registry and CLI.

`TypedDict`: `ToolContext`, `ToolOutput`, and `ToolMetadata` make runtime data explicit and mypy-friendly.

Decorators: `@tool` attaches discovery metadata. `@log_execution` and `@measure_time` wrap execution without changing call signatures because they use `ParamSpec`.

Context managers: `ExecutionSession` logs session start/end and cleans tracked resources.

Generators: each built-in tool implements `stream()` with `yield` for token-by-token output.

Descriptors: `ToolConfig` uses `IdentifierField`, `IntegerRange`, `FloatRange`, and `BooleanField` to validate runtime config.

Properties: `ToolConfig.max_attempts`, `ToolConfig.reliability_profile`, `BaseTool.metadata`, and `BaseTool.mro_path` expose computed read-only state.

Dunder methods: framework objects implement `__repr__`, `__str__`, `__eq__`, and `__len__` where they provide useful semantics.

`__slots__`: core objects avoid accidental attributes and show memory-conscious framework design.

MRO and mixins: `BaseTool(LoggingMixin, RetryMixin, MetricsMixin, ABC)` composes cross-cutting behavior. `describe TOOL_NAME` prints the MRO chain.

## How This Maps To Real Agent Frameworks

LangGraph, CrewAI, and PydanticAI all need a discoverable catalog of callable capabilities. This project mirrors that with `ToolRegistry` and automatic registration.

Agent runtimes pass structured state through execution nodes. This project models that with `ToolContext` and `ToolOutput`.

Production frameworks decorate tools with metadata so planners know when and how to call them. This project uses `@tool(tags=..., examples=...)`.

Real systems stream model/tool output to improve responsiveness. This project uses generator-based streaming instead of fake string slicing hidden inside the CLI.

PydanticAI leans heavily on validation and typed contracts. This project uses descriptors and `Protocol` to teach the same design pressure without depending on external packages.

## What Recruiters Should Notice

- You understand framework internals, not only app-level scripting.
- You can design type-safe contracts and registry-based plugin systems.
- You can separate core runtime, CLI, descriptors, decorators, tools, and tests.
- You can explain why Python’s advanced features matter in backend and AI infrastructure.
- You know when a global registry is useful and where it becomes a production tradeoff.

## Design Challenge Notes

A global registry is simple and realistic for a learning framework, but large production systems often add explicit plugin loading, dependency injection, namespaces, versioning, and sandboxing. That would be the next architectural upgrade.

The current streaming path collects generated tokens into `ToolOutput` so tests and CLI output stay deterministic. A production CLI could print tokens as they arrive while separately recording metrics.

The built-in tools are deterministic and local by design. That keeps the framework testable, but the same interfaces can wrap web search, vector retrieval, LLM calls, or database operations.
