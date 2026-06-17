"""Metrics captured during tool execution."""

from __future__ import annotations


class ToolMetrics:
    """Small slotted metrics object for execution summaries."""

    __slots__ = ("failures", "runs", "total_duration_ms")

    def __init__(
        self,
        *,
        runs: int = 0,
        failures: int = 0,
        total_duration_ms: float = 0.0,
    ) -> None:
        self.runs = runs
        self.failures = failures
        self.total_duration_ms = total_duration_ms

    @property
    def average_duration_ms(self) -> float:
        """Average duration across successful and failed runs."""

        total_runs = len(self)
        if total_runs == 0:
            return 0.0
        return self.total_duration_ms / total_runs

    def record(self, *, duration_ms: float, failed: bool = False) -> None:
        """Record one execution outcome."""

        self.runs += 1
        self.total_duration_ms += duration_ms
        if failed:
            self.failures += 1

    def __len__(self) -> int:
        return self.runs

    def __str__(self) -> str:
        return (
            f"{self.runs} run(s), {self.failures} failure(s), "
            f"{self.average_duration_ms:.2f} ms avg"
        )

    def __repr__(self) -> str:
        return (
            "ToolMetrics("
            f"runs={self.runs}, "
            f"failures={self.failures}, "
            f"total_duration_ms={self.total_duration_ms:.2f}"
            ")"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ToolMetrics):
            return NotImplemented
        return (
            self.runs == other.runs
            and self.failures == other.failures
            and self.total_duration_ms == other.total_duration_ms
        )
