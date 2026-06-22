"""Function decorators for execution logging and timing."""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from time import perf_counter
from typing import TypeVar

try:
    from typing import ParamSpec
except ImportError:  # Python 3.9 compatibility for the local macOS runtime.
    from typing import TypeVar as ParamSpec  # type: ignore[misc, assignment]

from agent_cli.utils import FrameworkLogger

P = ParamSpec("P")
R = TypeVar("R")


def log_execution(func: Callable[P, R]) -> Callable[P, R]:
    """Log function start, success, and failure while preserving its signature."""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        owner = args[0].__class__.__name__ if args else func.__module__
        FrameworkLogger.info(f"starting {owner}.{func.__name__}")
        try:
            result = func(*args, **kwargs)
        except Exception as error:
            FrameworkLogger.error(f"failed {owner}.{func.__name__}: {error}")
            raise

        FrameworkLogger.info(f"finished {owner}.{func.__name__}")
        return result

    return wrapper


def measure_time(func: Callable[P, R]) -> Callable[P, R]:
    """Measure and log a function's wall-clock duration."""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        started_at = perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            duration_ms = (perf_counter() - started_at) * 1000
            owner = args[0].__class__.__name__ if args else func.__module__
            FrameworkLogger.info(
                f"{owner}.{func.__name__} took {duration_ms:.2f} ms"
            )

    return wrapper
