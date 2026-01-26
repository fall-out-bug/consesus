"""Tests for webhook event handler."""

import json
import pytest
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

from sdp.webhook.handler import EventHandler, WebhookEvent
from sdp.webhook.signature import SignatureValidator


@pytest.fixture
def signature_validator() -> SignatureValidator:
    """Create signature validator."""
    return SignatureValidator("test_secret")


@pytest.fixture
def event_handler(tmp_path: Path) -> EventHandler:
    """Create event handler."""
    return EventHandler(log_file=str(tmp_path / "webhook.log"))


def test_webhook_event_dataclass() -> None:
    """Test WebhookEvent dataclass."""
    event = WebhookEvent(
        event_type="issues",
        action="opened",
        payload={"test": "data"},
        received_at=datetime(2024, 1, 1, 12, 0, 0),
    )

    assert event.event_type == "issues"
    assert event.action == "opened"
    assert event.payload == {"test": "data"}


def test_event_handler_initialization(event_handler: EventHandler) -> None:
    """Test handler initialization."""
    assert event_handler._validator is not None
    assert event_handler._log_file.parent.exists()


def test_event_handler_handle_valid(event_handler: EventHandler, signature_validator: SignatureValidator) -> None:
    """Test handling valid webhook event."""
    payload = b'{"action": "opened", "issue": {"id": 1}}'
    signature = signature_validator.sign(payload)

    event = event_handler.handle(payload, signature)

    assert event.event_type == "issues"
    assert event.action == "opened"


def test_event_handler_handle_invalid_json(event_handler: EventHandler, signature_validator: SignatureValidator) -> None:
    """Test handling invalid JSON raises error."""
    payload = b"not json"
    signature = signature_validator.sign(payload)

    with pytest.raises(json.JSONDecodeError):
        event_handler.handle(payload, signature)


def test_event_handler_log_event(event_handler: EventHandler) -> None:
    """Test event logging."""
    event = WebhookEvent(
        event_type="issues",
        action="opened",
        payload={},
        received_at=datetime(2024, 1, 1, 12, 0, 0),
    )

    event_handler._log_event(event)

    # Check log file
    content = event_handler._log_file.read_text()
    assert "issues" in content
    assert "opened" in content


def test_event_handler_decorator(event_handler: EventHandler) -> None:
    """Test on decorator for registering handlers."""
    received = []

    @event_handler.on("issues")
    def handle_issue(event: WebhookEvent) -> None:
        received.append(event)

    event = WebhookEvent(
        event_type="issues",
        action="opened",
        payload={},
        received_at=datetime(2024, 1, 1, 12, 0, 0),
    )

    event_handler._trigger_handlers(event)

    assert len(received) == 1
    assert received[0].event_type == "issues"


def test_event_handler_get_event_log(event_handler: EventHandler) -> None:
    """Test getting event log."""
    # Add some events
    event = WebhookEvent(
        event_type="issues",
        action="opened",
        payload={},
        received_at=datetime(2024, 1, 1, 12, 0, 0),
    )

    event_handler._log_event(event)
    event_handler._log_event(event)

    events = event_handler.get_event_log(limit=10)

    assert len(events) == 2


def test_event_handler_get_event_log_empty(event_handler: EventHandler) -> None:
    """Test getting event log when file doesn't exist."""
    # Remove log file
    event_handler._log_file.unlink(missing_ok=True)

    events = event_handler.get_event_log()

    assert len(events) == 0


def test_event_handler_get_event_log_limit(event_handler: EventHandler) -> None:
    """Test get_event_log respects limit."""
    # Add multiple events
    for _ in range(5):
        event = WebhookEvent(
            event_type="issues",
            action="opened",
            payload={},
            received_at=datetime(2024, 1, 1, 12, 0, 0),
        )
        event_handler._log_event(event)

    events = event_handler.get_event_log(limit=3)

    assert len(events) == 3


def test_event_handler_handler_error(event_handler: EventHandler) -> None:
    """Test handler errors are caught and logged."""
    @event_handler.on("issues")
    def failing_handler(event: WebhookEvent) -> None:
        raise ValueError("Test error")

    event = WebhookEvent(
        event_type="issues",
        action="opened",
        payload={},
        received_at=datetime(2024, 1, 1, 12, 0, 0),
    )

    # Should not raise
    event_handler._trigger_handlers(event)


def test_event_handler_multiple_handlers(event_handler: EventHandler) -> None:
    """Test multiple handlers for same event type."""
    received = []

    @event_handler.on("issues")
    def handler1(event: WebhookEvent) -> None:
        received.append("handler1")

    @event_handler.on("issues")
    def handler2(event: WebhookEvent) -> None:
        received.append("handler2")

    event = WebhookEvent(
        event_type="issues",
        action="opened",
        payload={},
        received_at=datetime(2024, 1, 1, 12, 0, 0),
    )

    event_handler._trigger_handlers(event)

    assert len(received) == 2
    assert "handler1" in received
    assert "handler2" in received


def test_event_handler_extract_event_type_issues(event_handler: EventHandler) -> None:
    """Test extracting event type from issues payload."""
    payload = b'{"issue": {"id": 1}}'
    signature = "sha256=skip"

    event = event_handler.handle(payload, signature)

    assert event.event_type == "issues"


def test_event_handler_extract_event_type_project(event_handler: EventHandler) -> None:
    """Test extracting event type from project_v2 payload."""
    payload = b'{"project_v2": {"id": 1}}'
    signature = "sha256=skip"

    event = event_handler.handle(payload, signature)

    assert event.event_type == "project_v2"
