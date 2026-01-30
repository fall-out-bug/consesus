"""Traceability service for AC→Test mapping."""

import re
from pathlib import Path

from sdp.beads.base import BeadsClient
from sdp.traceability.models import (
    ACTestMapping,
    MappingStatus,
    TraceabilityReport,
)


class TraceabilityService:
    """Check and manage AC→Test traceability."""

    def __init__(self, client: BeadsClient):
        """Initialize service with Beads client.

        Args:
            client: Beads client instance
        """
        self._client = client

    def check_traceability(self, ws_id: str) -> TraceabilityReport:
        """Check traceability for workstream.

        Args:
            ws_id: Workstream ID (e.g., "00-032-01")

        Returns:
            Traceability report

        Raises:
            ValueError: If workstream not found
        """
        # Get WS from Beads or markdown fallback
        task = self._get_ws_task(ws_id)
        if task:
            acs = self._extract_acs(task.description or "")
            stored_mappings = task.sdp_metadata.get("traceability", [])
        else:
            # Markdown fallback: read from docs/workstreams/
            content = self._get_ws_content_from_markdown(ws_id)
            if not content:
                raise ValueError(f"WS not found: {ws_id}")
            acs = self._extract_acs(content)
            stored_mappings = []

        # Build report
        mappings = []
        for ac_id, ac_desc in acs:
            # Find stored mapping
            stored = next(
                (m for m in stored_mappings if m["ac_id"] == ac_id),
                None,
            )

            if stored:
                mappings.append(ACTestMapping.from_dict(stored))
            else:
                mappings.append(
                    ACTestMapping(
                        ac_id=ac_id,
                        ac_description=ac_desc,
                        test_file=None,
                        test_name=None,
                        status=MappingStatus.MISSING,
                    )
                )

        return TraceabilityReport(ws_id=ws_id, mappings=mappings)

    def add_mapping(
        self, ws_id: str, ac_id: str, test_file: str, test_name: str
    ) -> None:
        """Add AC→Test mapping.

        Args:
            ws_id: Workstream ID
            ac_id: Acceptance criterion ID (e.g., "AC1")
            test_file: Test file path
            test_name: Test function name

        Raises:
            ValueError: If workstream not found
        """
        task = self._get_ws_task(ws_id)
        if not task:
            raise ValueError(f"WS not found: {ws_id}")

        # Get current mappings
        metadata = task.sdp_metadata.copy()
        mappings = metadata.get("traceability", [])

        # Update or add
        existing = next((m for m in mappings if m["ac_id"] == ac_id), None)
        if existing:
            existing["test_file"] = test_file
            existing["test_name"] = test_name
            existing["status"] = "mapped"
        else:
            # Extract AC description from task
            acs = self._extract_acs(task.description or "")
            ac_desc = next((desc for aid, desc in acs if aid == ac_id), "")

            mappings.append(
                {
                    "ac_id": ac_id,
                    "ac_description": ac_desc,
                    "test_file": test_file,
                    "test_name": test_name,
                    "status": "mapped",
                    "confidence": 1.0,
                }
            )

        metadata["traceability"] = mappings
        # Note: We need to update the task with new metadata
        # For now, store it back in sdp_metadata
        task.sdp_metadata = metadata

    def _get_ws_task(self, ws_id: str):
        """Get Beads task for workstream.

        Args:
            ws_id: Workstream ID

        Returns:
            Beads task or None if not found

        Note:
            Currently uses external_ref to find task.
            In future, may use dedicated WS index.
        """
        try:
            tasks = self._client.list_tasks()
        except Exception:
            return None
        for task in tasks:
            if task.external_ref == ws_id:
                return task
        return None

    def _get_ws_content_from_markdown(self, ws_id: str) -> str | None:
        """Get WS content from markdown file (fallback when Beads has no task).

        Searches docs/workstreams/backlog and docs/workstreams/completed.
        """
        cwd = Path.cwd()
        for subdir in ("backlog", "completed"):
            ws_dir = cwd / "docs" / "workstreams" / subdir
            if not ws_dir.exists():
                continue
            for f in ws_dir.glob(f"{ws_id}-*.md"):
                return f.read_text(encoding="utf-8")
        return None

    def _extract_acs(self, description: str) -> list[tuple[str, str]]:
        """Extract ACs from WS description.

        Looks for patterns like:
        - [ ] AC1: Description
        - AC1: Description

        Args:
            description: Task description text

        Returns:
            List of (ac_id, ac_description) tuples
        """
        pattern = r"(?:- \[[ x]\] )?(AC\d+):\s*(.+?)(?:\n|$)"
        matches = re.findall(pattern, description, re.IGNORECASE)
        return [(m[0].upper(), m[1].strip()) for m in matches]
