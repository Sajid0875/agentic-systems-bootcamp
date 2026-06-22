from typing import Any, Callable


# -----------------------------
# Base Descriptor
# -----------------------------

class ValidatedField:
    """
    Base data descriptor.

    It controls:
    - reading: __get__
    - writing: __set__
    - knowing its own attribute name: __set_name__
    """

    def __set_name__(self, owner: type, name: str) -> None:
        self.public_name = name
        self.private_name = f"_{name}"

    def __get__(self, instance: object, owner: type) -> Any:
        if instance is None:
            return self

        return getattr(instance, self.private_name)

    def __set__(self, instance: object, value: Any) -> None:
        validated_value = self.validate(value)
        setattr(instance, self.private_name, validated_value)

    def validate(self, value: Any) -> Any:
        return value


# -----------------------------
# Concrete Validation Descriptors
# -----------------------------

class NonEmptyString(ValidatedField):
    """Descriptor for string fields that cannot be empty."""

    def validate(self, value: Any) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{self.public_name} must be a string")

        value = value.strip()

        if not value:
            raise ValueError(f"{self.public_name} cannot be empty")

        return value


class IntegerRange(ValidatedField):
    """Descriptor for integer values inside a fixed range."""

    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any) -> int:
        if not isinstance(value, int):
            raise TypeError(f"{self.public_name} must be an integer")

        if not self.min_value <= value <= self.max_value:
            raise ValueError(
                f"{self.public_name} must be between "
                f"{self.min_value} and {self.max_value}"
            )

        return value


class FloatRange(ValidatedField):
    """Descriptor for float values inside a fixed range."""

    def __init__(self, min_value: float, max_value: float) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any) -> float:
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.public_name} must be a number")

        value = float(value)

        if not self.min_value <= value <= self.max_value:
            raise ValueError(
                f"{self.public_name} must be between "
                f"{self.min_value} and {self.max_value}"
            )

        return value


class ChoiceField(ValidatedField):
    """Descriptor for fields that must be one of fixed choices."""

    def __init__(self, choices: set[str]) -> None:
        self.choices = choices

    def validate(self, value: Any) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{self.public_name} must be a string")

        if value not in self.choices:
            raise ValueError(
                f"{self.public_name} must be one of {sorted(self.choices)}"
            )

        return value


# -----------------------------
# Non-Data Descriptor
# -----------------------------

class CachedValue:
    """
    Non-data descriptor.

    It only has __get__, so it is useful for lazy/cached values.
    """

    def __init__(self, function: Callable[[object], Any]) -> None:
        self.function = function
        self.name = function.__name__

    def __get__(self, instance: object, owner: type) -> Any:
        if instance is None:
            return self

        value = self.function(instance)
        instance.__dict__[self.name] = value
        return value


# -----------------------------
# Agent Config Model
# -----------------------------

class AgentConfig:
    """
    A small AI-agent configuration object.

    Descriptors validate fields before the agent uses them.
    """

    agent_name = NonEmptyString()
    model = ChoiceField({"gpt-4.1-mini", "claude-3.5-sonnet", "local-qwen"})
    system_prompt = NonEmptyString()

    temperature = FloatRange(0.0, 2.0)
    top_k = IntegerRange(1, 50)
    max_retries = IntegerRange(0, 10)
    timeout_seconds = FloatRange(0.1, 120.0)

    def __init__(
        self,
        agent_name: str,
        model: str,
        system_prompt: str,
        temperature: float,
        top_k: int,
        max_retries: int,
        timeout_seconds: float,
    ) -> None:
        self.agent_name = agent_name
        self.model = model
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.top_k = top_k
        self.max_retries = max_retries
        self.timeout_seconds = timeout_seconds

    @property
    def is_deterministic(self) -> bool:
        """
        Normal @property.

        This shows the built-in descriptor style.
        Low temperature means more predictable output.
        """
        return self.temperature <= 0.3

    @CachedValue
    def runtime_profile(self) -> dict[str, str]:
        """
        Cached non-data descriptor.

        This simulates an expensive computed value.
        It is calculated once and then stored in instance.__dict__.
        """
        print("Calculating runtime profile...")

        if self.temperature <= 0.3:
            behavior = "deterministic"
        elif self.temperature <= 1.0:
            behavior = "balanced"
        else:
            behavior = "creative"

        return {
            "agent": self.agent_name,
            "model": self.model,
            "behavior": behavior,
            "retrieval_depth": f"top {self.top_k}",
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "model": self.model,
            "system_prompt": self.system_prompt,
            "temperature": self.temperature,
            "top_k": self.top_k,
            "max_retries": self.max_retries,
            "timeout_seconds": self.timeout_seconds,
            "is_deterministic": self.is_deterministic,
        }

    def __repr__(self) -> str:
        return (
            f"AgentConfig(agent_name={self.agent_name!r}, "
            f"model={self.model!r}, temperature={self.temperature})"
        )


# -----------------------------
# Agent Runtime
# -----------------------------

class AgentRuntime:
    """
    Fake runtime that uses AgentConfig.

    This keeps the project connected to agentic AI.
    """

    def __init__(self, config: AgentConfig) -> None:
        self.config = config

    def run(self, user_task: str) -> str:
        return (
            f"Agent '{self.config.agent_name}' using {self.config.model} "
            f"is handling task: {user_task}"
        )


# -----------------------------
# Demo
# -----------------------------

def main() -> None:
    print("\n--- Valid Agent Config ---")

    config = AgentConfig(
        agent_name="research-agent",
        model="gpt-4.1-mini",
        system_prompt="You are a careful research assistant.",
        temperature=0.2,
        top_k=5,
        max_retries=3,
        timeout_seconds=30,
    )

    print(config)
    print(config.to_dict())

    print("\n--- @property Demo ---")
    print("Is deterministic:", config.is_deterministic)

    print("\n--- Cached Descriptor Demo ---")
    print(config.runtime_profile)
    print(config.runtime_profile)

    print("\n--- Agent Runtime Demo ---")
    runtime = AgentRuntime(config)
    print(runtime.run("Find sources for Python descriptors"))

    print("\n--- Invalid Config Demo ---")

    try:
        bad_config = AgentConfig(
            agent_name="",
            model="unknown-model",
            system_prompt="You are helpful.",
            temperature=5.0,
            top_k=100,
            max_retries=-1,
            timeout_seconds=0,
        )
        print(bad_config)
    except (TypeError, ValueError) as error:
        print("Validation error:", error)


if __name__ == "__main__":
    main()
