"""Tier metrics storage for promotion/demotion tracking."""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class TierMetrics:
    """Metrics for tier promotion/demotion.

    Args:
        ws_id: Workstream ID
        current_tier: Current capability tier (T0, T1, T2, T3)
        total_attempts: Total number of build attempts
        successful_attempts: Number of successful attempts
        consecutive_failures: Number of consecutive failed attempts
        last_updated: Timestamp of last update
    """

    ws_id: str
    current_tier: str
    total_attempts: int = 0
    successful_attempts: int = 0
    consecutive_failures: int = 0
    last_updated: datetime = field(default_factory=datetime.now)

    @property
    def success_rate(self) -> float:
        """Calculate success rate (0.0 - 1.0).

        Returns:
            Success rate as float, 0.0 if no attempts
        """
        if self.total_attempts == 0:
            return 0.0
        return self.successful_attempts / self.total_attempts


class TierMetricsStore:
    """Store and retrieve tier metrics from JSON file.

    Provides persistent storage for tracking workstream execution metrics
    to support automatic tier promotion/demotion.
    """

    def __init__(self, storage_path: Path = Path(".sdp/tier_metrics.json")) -> None:
        """Initialize metrics store.

        Args:
            storage_path: Path to JSON file for persistence
        """
        self.storage_path = storage_path
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._metrics: dict[str, TierMetrics] = {}
        self._load()

    def _load(self) -> None:
        """Load metrics from storage file."""
        if not self.storage_path.exists():
            self._metrics = {}
            return

        try:
            with open(self.storage_path, encoding="utf-8") as f:
                data = json.load(f)
                self._metrics = {}
                for ws_id, m in data.items():
                    # Parse datetime from ISO format
                    m["last_updated"] = datetime.fromisoformat(m["last_updated"])
                    self._metrics[ws_id] = TierMetrics(**m)
        except (json.JSONDecodeError, KeyError, ValueError):
            # If file is corrupted, start fresh
            self._metrics = {}

    def _save(self) -> None:
        """Save metrics to storage file."""
        data = {
            ws_id: {
                "ws_id": m.ws_id,
                "current_tier": m.current_tier,
                "total_attempts": m.total_attempts,
                "successful_attempts": m.successful_attempts,
                "consecutive_failures": m.consecutive_failures,
                "last_updated": m.last_updated.isoformat(),
            }
            for ws_id, m in self._metrics.items()
        }
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def record_attempt(self, ws_id: str, tier: str, success: bool) -> None:
        """Record a build attempt.

        Args:
            ws_id: Workstream ID
            tier: Current capability tier
            success: Whether attempt succeeded
        """
        if ws_id not in self._metrics:
            self._metrics[ws_id] = TierMetrics(ws_id=ws_id, current_tier=tier)

        metrics = self._metrics[ws_id]
        metrics.total_attempts += 1
        if success:
            metrics.successful_attempts += 1
            metrics.consecutive_failures = 0
        else:
            metrics.consecutive_failures += 1
        metrics.last_updated = datetime.now()

        self._save()

    def get_metrics(self, ws_id: str) -> Optional[TierMetrics]:
        """Get metrics for workstream.

        Args:
            ws_id: Workstream ID

        Returns:
            TierMetrics if exists, None otherwise
        """
        return self._metrics.get(ws_id)

    def check_promotion_eligible(self, ws_id: str) -> Optional[str]:
        """Check if workstream is eligible for tier change.

        Args:
            ws_id: Workstream ID

        Returns:
            New tier if eligible, None otherwise
        """
        metrics = self.get_metrics(ws_id)
        if not metrics:
            return None

        from sdp.core.tier_promoter import check_tier_change

        return check_tier_change(metrics)
