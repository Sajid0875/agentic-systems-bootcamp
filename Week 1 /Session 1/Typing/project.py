from typing import (
    Protocol,
    TypedDict,
    TypeVar,
    Generic,
    Callable,
    Optional,
    Annotated,
    ParamSpec,
)
from functools import wraps


# =========================
# Annotated
# =========================

AgentName = Annotated[str, "Name of the agent"]


# =========================
# TypedDict
# =========================

class AgentState(TypedDict):
    query: str
    tool_name: str
    result: str


# =========================
# Protocol
# =========================

class Tool(Protocol):
    name: str

    def run(self, query: str) -> str:
        ...


# =========================
# TypeVar + Generic
# =========================

T = TypeVar("T")


class MemoryStore(Generic[T]):
    def __init__(self) -> None:
        self.items: dict[str, T] = {}

    def set(self, key: str, value: T) -> None:
        self.items[key] = value

    def get(self, key: str) -> Optional[T]:
        return self.items.get(key)

    def all_items(self) -> dict[str, T]:
        return self.items


# =========================
# ParamSpec + TypeVar
# Decorator for logging
# =========================

P = ParamSpec("P")
R = TypeVar("R")


def log_call(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"[LOG] Calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


# =========================
# Tools
# =========================

class SearchTool:
    name = "search"

    @log_call
    def run(self, query: str) -> str:
        return f"Searching for: {query}"


class CalculatorTool:
    name = "calculator"

    @log_call
    def run(self, query: str) -> str:
        try:
            result = eval(query)
            return f"Calculation result: {result}"
        except Exception:
            return "Invalid calculation"


# =========================
# Callable
# =========================

ToolSelector = Callable[[str], Tool]


def select_tool(query: str, tools: dict[str, Tool]) -> Tool:
    if any(char.isdigit() for char in query):
        return tools["calculator"]

    return tools["search"]


# =========================
# Agent
# =========================

class Agent:
    def __init__(
        self,
        name: AgentName,
        tools: dict[str, Tool],
        memory: MemoryStore[AgentState],
        selector: ToolSelector,
    ) -> None:
        self.name = name
        self.tools = tools
        self.memory = memory
        self.selector = selector

    def run(self, query: str) -> str:
        tool = self.selector(query)
        result = tool.run(query)

        state: AgentState = {
            "query": query,
            "tool_name": tool.name,
            "result": result,
        }

        self.memory.set(query, state)

        return result

    def show_memory(self) -> None:
        print("\n--- Agent Memory ---")

        for key, state in self.memory.all_items().items():
            print(f"Query: {state['query']}")
            print(f"Tool Used: {state['tool_name']}")
            print(f"Result: {state['result']}")
            print("-" * 20)


# =========================
# Main App
# =========================

def main() -> None:
    search_tool = SearchTool()
    calculator_tool = CalculatorTool()

    tools: dict[str, Tool] = {
        "search": search_tool,
        "calculator": calculator_tool,
    }

    memory = MemoryStore[AgentState]()

    agent = Agent(
        name="Mini Typed Agent",
        tools=tools,
        memory=memory,
        selector=lambda query: select_tool(query, tools),
    )

    print(agent.run("Python typing"))
    print(agent.run("2 + 2"))
    print(agent.run("10 * 5"))

    agent.show_memory()


if __name__ == "__main__":
    main()
