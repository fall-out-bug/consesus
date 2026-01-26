"""Task representation for queue."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .priority import Priority


@dataclass
class Task:
    """A task in the execution queue."""

    ws_id: str
    priority: Priority = Priority.NORMAL
    retry_count: int = 0
    max_retries: int = 2
    created_at: datetime = field(default_factory=datetime.now)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_ready(self) -> bool:
        """Check if task is ready to run (not blocked)."""
        return self.priority != Priority.BLOCKED

    @property
    def can_retry(self) -> bool:
        """Check if task can be retried."""
        return self.retry_count < self.max_retries

    @property
    def is_running(self) -> bool:
        """Check if task is currently running."""
        return self.started_at is not None and self.completed_at is None

    @property
    def is_complete(self) -> bool:
        """Check if task is complete."""
        return self.completed_at is not None

    def __lt__(self, other: "Task") -> bool:
        """Compare tasks for priority queue (higher priority first)."""
        return self.priority < other.priority

    def mark_started(self) -> None:
        """Mark task as started."""
        if self.started_at is None:
            self.started_at = datetime.now()

    def mark_complete(self, success: bool = True, error: str | None = None) -> None:
        """Mark task as complete.

        Args:
            success: Whether task succeeded
            error: Error message if failed
        """
        self.completed_at = datetime.now()
        if not success:
            self.error_message = error

    def increment_retry(self) -> None:
        """Increment retry count."""
        self.retry_count += 1
        self.started_at = None
        self.completed_at = None
