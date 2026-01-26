"""Exceptions for agent execution."""


class ExecutorError(Exception):
    """Base exception for executor errors."""

    def __init__(self, message: str, ws_id: str | None = None) -> None:
        """Initialize error.

        Args:
            message: Error message
            ws_id: Associated workstream ID
        """
        self.ws_id = ws_id
        super().__init__(message)


class ExecutionTimeoutError(ExecutorError):
    """Raised when execution times out."""


class PreCheckError(ExecutorError):
    """Raised when pre-execution checks fail."""


class TaskUpdateError(ExecutorError):
    """Raised when task update fails."""