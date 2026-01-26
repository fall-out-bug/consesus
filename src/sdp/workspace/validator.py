"""Validation for workstream state transitions."""


class MoveValidationError(Exception):
    """Raised when a workstream move is invalid."""

    def __init__(self, message: str, ws_id: str | None = None) -> None:
        """Initialize error.

        Args:
            message: Error message
            ws_id: Associated workstream ID
        """
        self.ws_id = ws_id
        super().__init__(message)


class MoveValidator:
    """Validates workstream state transitions."""

    VALID_TRANSITIONS = {
        "backlog": ["in_progress"],
        "in_progress": ["backlog", "completed", "blocked"],
        "blocked": ["backlog", "in_progress"],
        "completed": ["backlog", "in_progress"],  # Can reopen
    }

    def validate_move(self, current_path: str, to_status: str) -> None:
        """Validate a workstream move.

        Args:
            current_path: Current workstream file path
            to_status: Target status (backlog, in-progress, completed, blocked)

        Raises:
            MoveValidationError: If move is invalid
        """
        from pathlib import Path

        path = Path(current_path)

        # Check file exists
        if not path.exists():
            raise MoveValidationError(f"Workstream file not found: {current_path}")

        # Determine current status from path
        current_status = self._get_status_from_path(path)

        # Normalize status values
        to_status_normalized = to_status.replace("-", "_")

        # Check if transition is valid
        if to_status_normalized not in self.VALID_TRANSITIONS.get(current_status, []):
            raise MoveValidationError(
                f"Invalid transition: {current_status} -> {to_status_normalized}",
            )

    def validate_complete(self, ws_content: str) -> list[str]:
        """Validate workstream can be completed.

        Args:
            ws_content: Workstream file content

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Check for acceptance criteria
        if "## Acceptance Criteria" in ws_content:
            ac_section = ws_content.split("## Acceptance Criteria")[1].split("##")[0]

            # Look for unchecked items
            if "- [ ]" in ac_section:
                errors.append("Not all acceptance criteria are checked")

            # Look for TODO or incomplete items
            if "TODO" in ac_section or "FIXME" in ac_section:
                errors.append("Acceptance criteria contains TODO/FIXME")

        return errors

    def _get_status_from_path(self, path: Path) -> str:
        """Extract status from directory path.

        Args:
            path: Path to workstream file

        Returns:
            Status string (backlog, in_progress, completed)
        """
        parent = path.parent.name
        return parent
