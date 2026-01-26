"""PID file management for daemon process."""

import os
from pathlib import Path


class PIDError(Exception):
    """Raised when PID operations fail."""


class PIDManager:
    """Manages daemon PID file for tracking process state."""

    def __init__(self, pid_file: str | Path) -> None:
        """Initialize PID manager.

        Args:
            pid_file: Path to PID file
        """
        self._pid_file = Path(pid_file)

    def write(self, pid: int) -> None:
        """Write PID to file.

        Args:
            pid: Process ID to write
        """
        self._pid_file.parent.mkdir(parents=True, exist_ok=True)
        self._pid_file.write_text(str(pid))

    def read(self) -> int:
        """Read PID from file.

        Returns:
            Process ID from file

        Raises:
            PIDError: If PID file doesn't exist
        """
        if not self._pid_file.exists():
            raise PIDError(f"PID file not found: {self._pid_file}")
        return int(self._pid_file.read_text())

    def remove(self) -> None:
        """Remove PID file if it exists."""
        if self._pid_file.exists():
            self._pid_file.unlink()

    def is_running(self) -> bool:
        """Check if the process in PID file is currently running.

        Returns:
            True if process is running, False otherwise
        """
        try:
            pid = self.read()
            os.kill(pid, 0)  # Signal 0 doesn't kill, just checks existence
            return True
        except (PIDError, OSError):
            return False
