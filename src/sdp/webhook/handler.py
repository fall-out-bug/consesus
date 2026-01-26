"""GitHub webhook event handler."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from .signature import SignatureValidator

from .signature import SignatureError, SignatureValidator

logger = logging.getLogger(__name__)


@dataclass
class WebhookEvent:
    """A GitHub webhook event."""

    event_type: str  # issues, project_v2, etc.
    action: str | None  # opened, edited, closed, etc.
    payload: dict[str, Any]
    received_at: datetime


class EventHandler:
    """Handles GitHub webhook events.

    Processes incoming webhook events and triggers appropriate actions.
    """

    def __init__(
        self,
        signature_validator: SignatureValidator | None = None,
        log_file: str | Path = ".sdp/webhook.log",
    ) -> None:
        """Initialize event handler.

        Args:
            signature_validator: Validator for webhook signatures
            log_file: Path to webhook event log
        """
        self._validator = signature_validator or SignatureValidator()
        self._log_file = Path(log_file)
        self._log_file.parent.mkdir(parents=True, exist_ok=True)

        # Registered event handlers
        self._handlers: dict[str, list[Callable[[WebhookEvent], None]]] = {}

    def on(self, event_type: str) -> Callable[[Callable[[WebhookEvent], None]], Callable[[WebhookEvent], None]]:
        """Decorator to register handler for event type.

        Args:
            event_type: Event type (e.g., "issues", "project_v2")

        Returns:
            Decorator function
        """

        def decorator(func: Callable[[WebhookEvent], None]) -> Callable[[WebhookEvent], None]:
            if event_type not in self._handlers:
                self._handlers[event_type] = []
            self._handlers[event_type].append(func)
            return func

        return decorator

    def handle(
        self,
        payload: bytes,
        signature_header: str | None = None,
    ) -> WebhookEvent:
        """Handle incoming webhook request.

        Args:
            payload: Raw request body bytes
            signature_header: X-Hub-Signature-256 header value

        Returns:
            WebhookEvent that was processed

        Raises:
            SignatureError: If signature validation fails
        """
        # Validate signature
        self._validator.validate(payload, signature_header)

        # Parse payload
        try:
            data = json.loads(payload.decode())
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON payload: {e}")
            raise

        # Extract event info
        # First try to determine event type from payload structure
        event_type = self._get_event_type_from_headers(data)
        action = data.get("action")

        event = WebhookEvent(
            event_type=event_type,
            action=action,
            payload=data,
            received_at=datetime.now(),
        )

        # Log event
        self._log_event(event)

        # Trigger handlers
        self._trigger_handlers(event)

        return event

    def _get_event_type_from_headers(self, payload: dict[str, Any]) -> str:
        """Extract event type from payload headers.

        Args:
            payload: Parsed JSON payload

        Returns:
            Event type string
        """
        # Try common fields
        if "issue" in payload:
            return "issues"
        elif "project_v2" in payload or "projects_v2_item" in payload:
            return "project_v2"
        elif "pull_request" in payload:
            return "pull_request"
        elif "repository" in payload:
            return "repository"

        return "unknown"

    def _log_event(self, event: WebhookEvent) -> None:
        """Log webhook event to file.

        Args:
            event: Event to log
        """
        try:
            log_entry = {
                "timestamp": event.received_at.isoformat(),
                "event_type": event.event_type,
                "action": event.action,
            }

            with open(self._log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")

        except Exception as e:
            logger.error(f"Failed to log event: {e}")

    def _trigger_handlers(self, event: WebhookEvent) -> None:
        """Trigger registered handlers for event.

        Args:
            event: Event to handle
        """
        handlers = self._handlers.get(event.event_type, [])

        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Handler error for {event.event_type}: {e}")

    def get_event_log(self, limit: int = 100) -> list[dict[str, Any]]:
        """Read recent events from log file.

        Args:
            limit: Maximum number of events to return

        Returns:
            List of event dicts
        """
        events: list[dict[str, Any]] = []

        if not self._log_file.exists():
            return events

        try:
            with open(self._log_file) as f:
                for line in f:
                    if line.strip():
                        try:
                            events.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue

                    if len(events) >= limit:
                        break

        except Exception as e:
            logger.error(f"Failed to read event log: {e}")

        # Return most recent first
        return list(reversed(events[-limit:]))
