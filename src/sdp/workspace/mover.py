"""Workstream file management between status directories."""

import shutil
from pathlib import Path

from .index_updater import IndexUpdater
from .state_updater import StateUpdater
from .validator import MoveValidationError, MoveValidator


class WorkstreamMover:
    """Moves workstream files between status directories."""

    def __init__(self, base_dir: str = "docs/workstreams") -> None:
        """Initialize mover.

        Args:
            base_dir: Base directory containing status subdirectories
        """
        self._base = Path(base_dir)
        self._validator = MoveValidator()
        self._state_updater = StateUpdater()
        self._index_updater = IndexUpdater()

    def move(
        self,
        ws_id: str,
        to_status: str,
        update_index: bool = True,
        validate_ac: bool = False,
    ) -> Path:
        """Move workstream to new status directory.

        Args:
            ws_id: Workstream ID
            to_status: Target status (backlog, in-progress, completed, blocked)
            update_index: Whether to update INDEX.md
            validate_ac: Whether to validate acceptance criteria for completion

        Returns:
            New file path

        Raises:
            MoveValidationError: If move is invalid
        """
        # Find current file
        current_path = self._find_ws_file(ws_id)
        if not current_path:
            raise MoveValidationError(f"Workstream not found: {ws_id}", ws_id)

        # Get current status from path
        current_status = current_path.parent.name

        # Validate move
        self._validator.validate_move(str(current_path), to_status)

        # Special validation for completed status
        if validate_ac and to_status == "completed":
            content = current_path.read_text()
            errors = self._validator.validate_complete(content)
            if errors:
                raise MoveValidationError(
                    f"Cannot complete workstream: {', '.join(errors)}",
                    ws_id,
                )

        # Build new path
        new_status_dir = to_status.replace("-", "_")  # in-progress -> in_progress
        new_path = self._base / new_status_dir / f"{ws_id}.md"

        # Move file
        shutil.move(str(current_path), str(new_path))

        # Update YAML frontmatter
        self._state_updater.update_status(new_path, to_status)

        # Update INDEX.md
        if update_index:
            self._index_updater.update(ws_id, current_status, to_status)

        return new_path

    def start(self, ws_id: str) -> Path:
        """Start workstream (backlog -> in-progress).

        Args:
            ws_id: Workstream ID

        Returns:
            New file path
        """
        return self.move(ws_id, "in-progress")

    def complete(self, ws_id: str, validate: bool = True) -> Path:
        """Complete workstream (in-progress -> completed).

        Args:
            ws_id: Workstream ID
            validate: Whether to validate acceptance criteria

        Returns:
            New file path
        """
        return self.move(ws_id, "completed", validate_ac=validate)

    def block(self, ws_id: str) -> Path:
        """Block workstream.

        Args:
            ws_id: Workstream ID

        Returns:
            New file path
        """
        return self.move(ws_id, "blocked")

    def unblock(self, ws_id: str) -> Path:
        """Unblock workstream (blocked -> backlog).

        Args:
            ws_id: Workstream ID

        Returns:
            New file path
        """
        return self.move(ws_id, "backlog")

    def _find_ws_file(self, ws_id: str) -> Path | None:
        """Find workstream file in any status directory.

        Args:
            ws_id: Workstream ID

        Returns:
            Path to workstream file or None
        """
        for status_dir in ["backlog", "in_progress", "completed", "blocked"]:
            path = self._base / status_dir / f"{ws_id}.md"
            if path.exists():
                return path
        return None

    def list_in_status(self, status: str) -> list[Path]:
        """List all workstreams in a status directory.

        Args:
            status: Status to list (backlog, in-progress, completed, blocked)

        Returns:
            List of workstream file paths
        """
        status_dir = status.replace("-", "_")
        path = self._base / status_dir

        if not path.exists():
            return []

        return list(path.glob("*.md"))
