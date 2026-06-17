"""Reusable validating descriptors for configuration fields."""

from __future__ import annotations

import re
from typing import Any, Generic, TypeVar, cast, overload

T = TypeVar("T")
_MISSING = object()


class ValidatedField(Generic[T]):
    """Base data descriptor that validates before storing a value.

    Values are stored under a private slot name, so this descriptor works with
    slotted classes and prevents arbitrary attributes from being created.
    """

    __slots__ = ("default", "private_name", "public_name")

    def __init__(self, default: T | object = _MISSING) -> None:
        self.default = default
        self.public_name = ""
        self.private_name = ""

    def __set_name__(self, owner: type[object], name: str) -> None:
        self.public_name = name
        self.private_name = f"_{name}"

    @overload
    def __get__(self, instance: None, owner: type[object]) -> ValidatedField[T]:
        ...

    @overload
    def __get__(self, instance: object, owner: type[object]) -> T:
        ...

    def __get__(
        self,
        instance: object | None,
        owner: type[object],
    ) -> T | ValidatedField[T]:
        if instance is None:
            return self

        if hasattr(instance, self.private_name):
            return cast(T, getattr(instance, self.private_name))

        if self.default is not _MISSING:
            return cast(T, self.default)

        raise AttributeError(f"{self.public_name} has not been configured")

    def __set__(self, instance: object, value: Any) -> None:
        setattr(instance, self.private_name, self.validate(value))

    def validate(self, value: Any) -> T:
        """Return a validated value.

        Subclasses override this method with concrete validation rules.
        """

        return cast(T, value)


class NonEmptyString(ValidatedField[str]):
    """Descriptor for string fields that must contain visible text."""

    def validate(self, value: Any) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{self.public_name} must be a string")

        cleaned = value.strip()
        if not cleaned:
            raise ValueError(f"{self.public_name} cannot be empty")

        return cleaned


class IdentifierField(NonEmptyString):
    """Descriptor for registry identifiers such as ``search`` or ``translate``."""

    _pattern = re.compile(r"^[a-z][a-z0-9_-]*$")

    def validate(self, value: Any) -> str:
        cleaned = super().validate(value)
        if not self._pattern.fullmatch(cleaned):
            raise ValueError(
                f"{self.public_name} must start with a lowercase letter and "
                "contain only lowercase letters, numbers, underscores, or hyphens"
            )

        return cleaned


class IntegerRange(ValidatedField[int]):
    """Descriptor for integer values constrained to an inclusive range."""

    __slots__ = ("max_value", "min_value")

    def __init__(self, min_value: int, max_value: int, default: int) -> None:
        super().__init__(default)
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{self.public_name} must be an integer")

        if not self.min_value <= value <= self.max_value:
            raise ValueError(
                f"{self.public_name} must be between "
                f"{self.min_value} and {self.max_value}"
            )

        return value


class FloatRange(ValidatedField[float]):
    """Descriptor for numeric values constrained to an inclusive range."""

    __slots__ = ("max_value", "min_value")

    def __init__(self, min_value: float, max_value: float, default: float) -> None:
        super().__init__(default)
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{self.public_name} must be a number")

        cleaned = float(value)
        if not self.min_value <= cleaned <= self.max_value:
            raise ValueError(
                f"{self.public_name} must be between "
                f"{self.min_value} and {self.max_value}"
            )

        return cleaned


class BooleanField(ValidatedField[bool]):
    """Descriptor for strict boolean configuration fields."""

    def validate(self, value: Any) -> bool:
        if not isinstance(value, bool):
            raise TypeError(f"{self.public_name} must be a boolean")

        return value

