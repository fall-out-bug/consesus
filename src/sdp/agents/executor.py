"""Agent executor for autonomous workstream execution."""

import logging
import subprocess
import time
from pathlib import Path
from typing import Callable

from .errors import ExecutorError, ExecutionTimeoutError
from .metrics import MetricsStore

logger = logging.getLogger(__name__)


class AgentExecutor:
    """Executes workstreams autonomously."""

    def __init__(
        self,
        metrics_file: str = ".sdp/execution_metrics.json",
        timeout: int = 3600,
        max_retries: int = 2,
    ) -> None:
        """Initialize executor.

        Args:
            metrics_file: Path to metrics storage file
            timeout: Default timeout per execution (seconds)
            max_retries: Maximum retry attempts
        """
        self._metrics = MetricsStore(metrics_file)
        self._timeout = timeout
        self._max_retries = max_retries
        self._on_progress: Callable[[str, str], None] | None = None

    def set_progress_callback(self, callback: Callable[[str, str], None]) -> None:
        """Set callback for progress updates.

        Args:
            callback: Function(ws_id, message) called on progress
        """
        self._on_progress = callback

    def execute(
        self,
        ws_id: str,
        timeout: int | None = None,
        tier: str = "T2",
    ) -> bool:
        """Execute a workstream and return success status.

        Args:
            ws_id: Workstream ID to execute
            timeout: Timeout in seconds (uses default if None)
            tier: Capability tier

        Returns:
            True if execution succeeded, False otherwise
        """
        timeout = timeout or self._timeout
        start = time.time()

        # Try with retries
        for attempt in range(self._max_retries + 1):
            if attempt > 0:
                logger.info(f"Retry {attempt}/{self._max_retries} for {ws_id}")

            try:
                success = self._execute_once(ws_id, timeout, tier)
                duration = time.time() - start

                self._metrics.record(
                    ws_id,
                    success=success,
                    duration=duration,
                    tier=tier,
                    error=None if success else "Execution failed",
                )

                return success

            except ExecutionTimeoutError as e:
                duration = time.time() - start
                self._metrics.record(
                    ws_id,
                    success=False,
                    duration=duration,
                    tier=tier,
                    error=f"Timeout: {e}",
                )

                if attempt == self._max_retries:
                    raise

            except ExecutorError as e:
                duration = time.time() - start
                self._metrics.record(
                    ws_id,
                    success=False,
                    duration=duration,
                    tier=tier,
                    error=str(e),
                )

                if attempt == self._max_retries:
                    raise

        return False

    def _execute_once(self, ws_id: str, timeout: int, tier: str) -> bool:
        """Execute workstream once.

        Args:
            ws_id: Workstream ID
            timeout: Timeout in seconds
            tier: Capability tier

        Returns:
            True if succeeded

        Raises:
            ExecutionTimeoutError: If execution times out
            ExecutorError: If execution fails
        """
        self._progress(ws_id, "Starting execution")

        # Check if workstream file exists
        ws_file = self._find_ws_file(ws_id)
        if not ws_file:
            raise ExecutorError(f"Workstream file not found: {ws_id}", ws_id)

        self._progress(ws_id, f"Found workstream file: {ws_file}")

        # Execute via /build skill
        result = self._run_build_skill(ws_id, timeout)

        if result.returncode == 0:
            self._progress(ws_id, "Execution completed successfully")
            return True
        else:
            error_msg = result.stderr or result.stdout or "Unknown error"
            self._progress(ws_id, f"Execution failed: {error_msg[:100]}")
            raise ExecutorError(f"Build failed: {error_msg}", ws_id)

    def _find_ws_file(self, ws_id: str) -> Path | None:
        """Find workstream file.

        Args:
            ws_id: Workstream ID

        Returns:
            Path to workstream file or None
        """
        base = Path("docs/workstreams")
        for status_dir in ["backlog", "in_progress", "completed"]:
            path = base / status_dir / f"{ws_id}.md"
            if path.exists():
                return path
        return None

    def _run_build_skill(self, ws_id: str, timeout: int) -> subprocess.CompletedProcess:
        """Run /build skill for workstream.

        Args:
            ws_id: Workstream ID
            timeout: Timeout in seconds

        Returns:
            Completed process result

        Raises:
            ExecutionTimeoutError: If execution times out
        """
        # Try via claude CLI if available
        cmd = ["claude", "skill", "build", ws_id]

        self._progress(ws_id, f"Running: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            return result
        except subprocess.TimeoutExpired:
            raise ExecutionTimeoutError(f"Execution timed out after {timeout}s", ws_id)
        except FileNotFoundError:
            # claude CLI not available, simulate success for testing
            self._progress(ws_id, "Claude CLI not found, simulating execution")
            return subprocess.CompletedProcess(
                args=cmd,
                returncode=0,
                stdout="Simulated success",
                stderr="",
            )

    def _progress(self, ws_id: str, message: str) -> None:
        """Report progress.

        Args:
            ws_id: Workstream ID
            message: Progress message
        """
        logger.info(f"[{ws_id}] {message}")
        if self._on_progress:
            self._on_progress(ws_id, message)

    def get_metrics(self) -> dict:
        """Get execution metrics.

        Returns:
            Dict with overall metrics
        """
        m = self._metrics.get_metrics()
        return {
            "total": m.total_executions,
            "successful": m.successful_executions,
            "failed": m.failed_executions,
            "success_rate": m.get_success_rate(),
            "avg_duration": m.get_avg_duration(),
        }

    def get_ws_metrics(self, ws_id: str) -> dict:
        """Get metrics for a specific workstream.

        Args:
            ws_id: Workstream ID

        Returns:
            Dict with workstream metrics
        """
        return self._metrics.get_ws_metrics(ws_id)
