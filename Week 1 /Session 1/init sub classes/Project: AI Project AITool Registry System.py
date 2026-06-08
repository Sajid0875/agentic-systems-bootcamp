class AgentTool:
    registry = {}

    def __init_subclass__(cls, tool_name=None, **kwargs):
        super().__init_subclass__(**kwargs)

        if tool_name is None:
            raise TypeError(
                f"{cls.__name__} must define tool_name"
            )

        AgentTool.registry[tool_name] = cls


class SearchTool(AgentTool,tool_name="search"):
    def run(self, query):
        return f"Searching: {query}"


class CalculatorTool(
    AgentTool,
    tool_name="calculator"
):
    def run(self, expression):
        return eval(expression)


class WeatherTool(
    AgentTool,
    tool_name="weather"
):
    def run(self, city):
        return f"Weather data for {city}"


print("Registered Tools:\n")

for name, tool in AgentTool.registry.items():
    print(name, "->", tool.__name__)

print("\nTesting Tools:\n")

search = AgentTool.registry["search"]()
print(search.run("LangGraph"))

weather = AgentTool.registry["weather"]()
print(weather.run("London"))