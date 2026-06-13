# Mini Typed AI Agent

A simple Python project built to practice modern Python typing concepts used in Backend Engineering and Agentic AI systems.

## Project Goal

The purpose of this project is to learn and apply Python typing concepts in a realistic mini-agent architecture rather than isolated examples.

The agent:

* Accepts a user query
* Selects an appropriate tool
* Executes the tool
* Stores the result in memory
* Displays previous interactions

---

## Concepts Covered

### TypedDict

Used to define a fixed schema for agent state.

```python
class AgentState(TypedDict):
    query: str
    tool_name: str
    result: str
```

### Protocol

Used to define a common interface for tools.

```python
class Tool(Protocol):
    name: str

    def run(self, query: str) -> str:
        ...
```

### TypeVar

Used as a placeholder type for reusable components.

```python
T = TypeVar("T")
```

### Generic

Used to create a reusable typed memory store.

```python
class MemoryStore(Generic[T]):
```

### Callable

Used for tool selection functions.

```python
Callable[[str], Tool]
```

### Optional

Used when a value may or may not exist.

```python
Optional[T]
```

### Annotated

Used to attach metadata to a type.

```python
AgentName = Annotated[str, "Name of the agent"]
```

### ParamSpec

Used to preserve function signatures inside decorators.

```python
P = ParamSpec("P")
```

### Decorators

A logging decorator is implemented for tool execution tracking.

### mypy

The project is fully type-checked using mypy.

---

## Features

### Search Tool

Simulates a search operation.

Example:

```text
Input:
Python typing

Output:
Searching for: Python typing
```

### Calculator Tool

Performs basic calculations.

Example:

```text
Input:
2 + 2

Output:
Calculation result: 4
```

### Agent Memory

Stores:

* User query
* Tool used
* Tool result

---

## Running the Project

Run the application:

```bash
python main.py
```

Example Output:

```text
[LOG] Calling run
Searching for: Python typing

[LOG] Calling run
Calculation result: 4

[LOG] Calling run
Calculation result: 50
```

---

## Type Checking

Install mypy:

```bash
pip install mypy
```

Run type checks:

```bash
mypy main.py
```

---

## Learning Outcome

This project demonstrates how Python typing is used in real-world software design.

After completing this project, you should understand:

* Type Hints
* TypedDict
* Protocol
* Callable
* TypeVar
* Generic
* Optional
* Annotated
* ParamSpec
* Decorator Typing
* mypy

These concepts form the foundation for modern Backend Engineering, FastAPI applications, AI Agents, LangGraph workflows, RAG systems, and MCP-based architectures.

