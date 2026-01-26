"""Thread-safe priority queue for task management."""

import threading
from queue import PriorityQueue, Empty
from typing import Callable

from .priority import Priority
from .state import QueueState
from .task import Task


class TaskQueue:
    """Thread-safe priority queue for task management."""

    def __init__(self, state_file: str = ".sdp/queue_state.json") -> None:
        """Initialize task queue.

        Args:
            state_file: Path to queue state file for persistence
        """
        self._queue: PriorityQueue[Task] = PriorityQueue()
        self._lock = threading.Lock()
        self._state_file = state_file
        self._count = 0  # Track queue size since PriorityQueue doesn't expose it
        self._load_state()  # Load existing state

    def _load_state(self) -> None:
        """Load queue state from file."""
        from datetime import datetime

        task_dicts = QueueState.load(self._state_file)
        for task_dict in task_dicts:
            try:
                # Reconstruct Task from dict
                task = Task(
                    ws_id=task_dict.get("ws_id", ""),
                    priority=Priority.from_string(task_dict.get("priority", "NORMAL")),
                    retry_count=task_dict.get("retry_count", 0),
                    max_retries=task_dict.get("max_retries", 2),
                    metadata=task_dict.get("metadata", {}),
                )

                # Parse datetime fields
                if "created_at" in task_dict:
                    task.created_at = datetime.fromisoformat(task_dict["created_at"])
                if "started_at" in task_dict and task_dict["started_at"]:
                    task.started_at = datetime.fromisoformat(task_dict["started_at"])
                if "completed_at" in task_dict and task_dict["completed_at"]:
                    task.completed_at = datetime.fromisoformat(task_dict["completed_at"])

                self._queue.put(task)
                self._count += 1
            except Exception:
                # Skip invalid tasks
                continue

    def enqueue(self, task: Task) -> None:
        """Add task to queue.

        Args:
            task: Task to add
        """
        with self._lock:
            self._queue.put(task)
            self._count += 1
            self._save_state()

    def dequeue(self, timeout: float | None = None) -> Task | None:
        """Remove and return highest priority task.

        Args:
            timeout: Seconds to wait, None for blocking

        Returns:
            Task or None if queue is empty
        """
        with self._lock:
            try:
                task = self._queue.get(block=True, timeout=timeout or 0.001)
                self._count = max(0, self._count - 1)
                self._save_state()
                return task
            except Empty:
                return None

    def peek(self) -> Task | None:
        """View highest priority task without removing.

        Returns:
            Highest priority task or None if empty
        """
        with self._lock:
            if self._count == 0:
                return None
            # PriorityQueue doesn't support peek directly
            # We need to get and re-put
            try:
                task = self._queue.get_nowait()
                self._queue.put_nowait(task)
                return task
            except Empty:
                return None

    def remove(self, ws_id: str) -> Task | None:
        """Remove task by workstream ID.

        Args:
            ws_id: Workstream ID to remove

        Returns:
            Removed task or None if not found
        """
        with self._lock:
            temp_tasks = []
            found = None

            while self._count > 0:
                try:
                    task = self._queue.get_nowait()
                    if task.ws_id == ws_id and found is None:
                        found = task
                        self._count -= 1
                    else:
                        temp_tasks.append(task)
                except Empty:
                    break

            # Put back remaining tasks
            for task in temp_tasks:
                self._queue.put_nowait(task)

            if found:
                self._save_state()

            return found

    def size(self) -> int:
        """Get current queue size.

        Returns:
            Number of tasks in queue
        """
        with self._lock:
            return self._count

    def is_empty(self) -> bool:
        """Check if queue is empty.

        Returns:
            True if queue has no tasks
        """
        return self.size() == 0

    def clear(self) -> None:
        """Clear all tasks from queue."""
        with self._lock:
            while self._count > 0:
                try:
                    self._queue.get_nowait()
                    self._count -= 1
                except Empty:
                    break
            QueueState.clear(self._state_file)

    def foreach(self, callback: Callable[[Task], None]) -> None:
        """Apply callback to each task in queue.

        Args:
            callback: Function to call for each task
        """
        with self._lock:
            temp_tasks = []

            while self._count > 0:
                try:
                    task = self._queue.get_nowait()
                    callback(task)
                    temp_tasks.append(task)
                except Empty:
                    break

            # Put back all tasks
            for task in temp_tasks:
                self._queue.put_nowait(task)

    def _save_state(self) -> None:
        """Persist queue state to file."""
        QueueState.save(self._queue, self._state_file)
