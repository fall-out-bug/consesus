"""Priority levels for tasks."""

from enum import IntEnum


class Priority(IntEnum):
    """Task priority levels (lower = higher priority)."""

    BLOCKED = 0
    BACKLOG = 1
    NORMAL = 2
    ACTIVE = 3
    URGENT = 4

    @classmethod
    def from_string(cls, value: str) -> "Priority":
        """Convert string to Priority.

        Args:
            value: String representation

        Returns:
            Priority enum value
        """
        try:
            return cls[value.upper()]
        except KeyError:
            return cls.NORMAL

    def __str__(self) -> str:
        return self.name
