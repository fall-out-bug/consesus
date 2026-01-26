"""Execution metrics tracking."""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class ExecutionRecord:
    """Record of a single workstream execution."""

    ws_id: str
    success: bool
    duration: float
    started_at: datetime
    completed_at: datetime
    attempts: int = 1
    error_message: str | None = None
    tier: str = "T2"  # Capability tier

    @property
    def duration_minutes(self) -> float:
        """Duration in minutes."""
        return self.duration / 60


@dataclass
class ExecutionMetrics:
    """Metrics storage for workstream executions."""

    records: list[ExecutionRecord] = field(default_factory=list)
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0

    def add_record(self, record: ExecutionRecord) -> None:
        """Add an execution record.

        Args:
            record: Record to add
        """
        self.records.append(record)
        self.total_executions += 1
        if record.success:
            self.successful_executions += 1
        else:
            self.failed_executions += 1

    def get_success_rate(self, ws_id: str | None = None) -> float:
        """Calculate success rate.

        Args:
            ws_id: Optional workstream ID to filter by

        Returns:
            Success rate as percentage (0-100)
        """
        if ws_id:
            ws_records = [r for r in self.records if r.ws_id == ws_id]
        else:
            ws_records = self.records

        if not ws_records:
            return 0.0

        successful = sum(1 for r in ws_records if r.success)
        return (successful / len(ws_records)) * 100

    def get_avg_duration(self, ws_id: str | None = None) -> float:
        """Get average execution duration.

        Args:
            ws_id: Optional workstream ID to filter by

        Returns:
            Average duration in seconds
        """
        if ws_id:
            ws_records = [r for r in self.records if r.ws_id == ws_id]
        else:
            ws_records = self.records

        if not ws_records:
            return 0.0

        return sum(r.duration for r in ws_records) / len(ws_records)

    def get_records_for_ws(self, ws_id: str) -> list[ExecutionRecord]:
        """Get all records for a workstream.

        Args:
            ws_id: Workstream ID

        Returns:
            List of records for the workstream
        """
        return [r for r in self.records if r.ws_id == ws_id]


class MetricsStore:
    """Persistent storage for execution metrics."""

    def __init__(self, storage_file: str = ".sdp/execution_metrics.json") -> None:
        """Initialize metrics store.

        Args:
            storage_file: Path to storage file
        """
        self._storage_file = Path(storage_file)
        self._metrics = ExecutionMetrics()
        self._load()

    def record(
        self,
        ws_id: str,
        success: bool,
        duration: float,
        tier: str = "T2",
        error: str | None = None,
    ) -> None:
        """Record an execution.

        Args:
            ws_id: Workstream ID
            success: Whether execution succeeded
            duration: Duration in seconds
            tier: Capability tier
            error: Optional error message
        """
        now = datetime.now()
        record = ExecutionRecord(
            ws_id=ws_id,
            success=success,
            duration=duration,
            started_at=now,
            completed_at=now,  # Simplified - actual would track start time
            tier=tier,
            error_message=error,
        )
        self._metrics.add_record(record)
        self._save()

    def get_metrics(self) -> ExecutionMetrics:
        """Get all metrics.

        Returns:
            Copy of current metrics
        """
        return self._metrics

    def get_ws_metrics(self, ws_id: str) -> dict:
        """Get metrics for a specific workstream.

        Args:
            ws_id: Workstream ID

        Returns:
            Dict with metrics for the workstream
        """
        records = self._metrics.get_records_for_ws(ws_id)

        if not records:
            return {
                "ws_id": ws_id,
                "total": 0,
                "successful": 0,
                "failed": 0,
                "success_rate": 0.0,
                "avg_duration": 0.0,
            }

        successful = sum(1 for r in records if r.success)
        return {
            "ws_id": ws_id,
            "total": len(records),
            "successful": successful,
            "failed": len(records) - successful,
            "success_rate": (successful / len(records)) * 100,
            "avg_duration": sum(r.duration for r in records) / len(records),
        }

    def _load(self) -> None:
        """Load metrics from storage."""
        if not self._storage_file.exists():
            return

        try:
            data = json.loads(self._storage_file.read_text())
            for record_data in data.get("records", []):
                record = ExecutionRecord(
                    ws_id=record_data["ws_id"],
                    success=record_data["success"],
                    duration=record_data["duration"],
                    started_at=datetime.fromisoformat(record_data["started_at"]),
                    completed_at=datetime.fromisoformat(record_data["completed_at"]),
                    attempts=record_data.get("attempts", 1),
                    error_message=record_data.get("error_message"),
                    tier=record_data.get("tier", "T2"),
                )
                self._metrics.add_record(record)
        except Exception:
            # Start fresh if loading fails
            pass

    def _save(self) -> None:
        """Save metrics to storage."""
        self._storage_file.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "records": [
                {
                    "ws_id": r.ws_id,
                    "success": r.success,
                    "duration": r.duration,
                    "started_at": r.started_at.isoformat(),
                    "completed_at": r.completed_at.isoformat(),
                    "attempts": r.attempts,
                    "error_message": r.error_message,
                    "tier": r.tier,
                }
                for r in self._metrics.records
            ]
        }

        self._storage_file.write_text(json.dumps(data, indent=2))
