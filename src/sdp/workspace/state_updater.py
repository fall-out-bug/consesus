"""Workstream state field updates."""

from datetime import datetime
from pathlib import Path

import yaml


class StateUpdater:
    """Updates status fields in workstream files."""

    def update_status(self, ws_path: str | Path, status: str) -> None:
        """Update status field in workstream YAML frontmatter.

        Args:
            ws_path: Path to workstream file
            status: New status value
        """
        path = Path(ws_path)
        content = path.read_text()

        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                except yaml.YAMLError:
                    frontmatter = {}
            else:
                frontmatter = {}
        else:
            # No frontmatter, add it
            frontmatter = {}

        # Update status
        frontmatter["status"] = status.replace("-", "_")

        # Add/update timestamps
        now = datetime.now().isoformat()
        if status == "in-progress":
            frontmatter["started"] = now
        elif status == "completed":
            frontmatter["completed"] = now

        # Reconstruct file
        new_content = f"---\n{yaml.dump(frontmatter, default_flow_style=False)}---\n"

        if len(parts) >= 3:
            new_content += parts[2]
        else:
            new_content += content

        path.write_text(new_content)

    def update_assignee(self, ws_path: str | Path, assignee: str) -> None:
        """Update assignee field in workstream YAML frontmatter.

        Args:
            ws_path: Path to workstream file
            assignee: New assignee value
        """
        path = Path(ws_path)
        content = path.read_text()

        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                except yaml.YAMLError:
                    frontmatter = {}
            else:
                frontmatter = {}
        else:
            frontmatter = {}

        frontmatter["assignee"] = assignee

        new_content = f"---\n{yaml.dump(frontmatter, default_flow_style=False)}---"

        if len(parts) >= 3:
            new_content += parts[2]
        else:
            new_content += content

        path.write_text(new_content)

    def update_field(self, ws_path: str | Path, field: str, value: object) -> None:
        """Update any field in workstream YAML frontmatter.

        Args:
            ws_path: Path to workstream file
            field: Field name to update
            value: New value
        """
        path = Path(ws_path)
        content = path.read_text()

        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                except yaml.YAMLError:
                    frontmatter = {}
            else:
                frontmatter = {}
        else:
            frontmatter = {}

        frontmatter[field] = value

        new_content = f"---\n{yaml.dump(frontmatter, default_flow_style=False)}---"

        if len(parts) >= 3:
            new_content += parts[2]
        else:
            new_content += content

        path.write_text(new_content)
