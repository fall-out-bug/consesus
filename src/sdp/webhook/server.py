"""GitHub webhook HTTP server."""

from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .handler import EventHandler

from .handler import EventHandler
from .signature import SignatureValidator, SignatureError


logger = logging.getLogger(__name__)


class WebhookServer:
    """HTTP server for receiving GitHub webhooks.

    Uses a simple HTTP server implementation for minimal dependencies.
    """

    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = 8080,
        webhook_secret: str | None = None,
        log_file: str = ".sdp/webhook.log",
    ) -> None:
        """Initialize webhook server.

        Args:
            host: Host to bind to
            port: Port to listen on
            webhook_secret: GitHub webhook secret for validation
            log_file: Path to event log file
        """
        self._host = host
        self._port = port
        self._running = False

        # Create signature validator and event handler
        self._validator = SignatureValidator(webhook_secret)
        self._handler = EventHandler(self._validator, log_file)

    @property
    def handler(self) -> EventHandler:
        """Get the event handler instance."""
        return self._handler

    def start(self) -> None:
        """Start the webhook server (blocking)."""
        try:
            from http.server import BaseHTTPRequestHandler, HTTPServer
        except ImportError:
            logger.error("http.server not available")
            return

        self._running = True

        class WebhookHandler(BaseHTTPRequestHandler):
            """HTTP request handler for webhooks."""

            def __init__(self, server_instance: WebhookServer) -> None:
                self._server = server_instance

            def __call__(
                self,
                *args: Any,
                **kwargs: Any,
            ) -> None:
                """Handle request."""
                super().__init__(*args, **kwargs)

            def do_POST(self) -> None:
                """Handle POST request (webhook delivery)."""
                if self.path != "/webhook":
                    self.send_error(404, "Not Found")
                    return

                # Get signature header
                signature = self.headers.get("X-Hub-Signature-256")

                # Read payload
                content_length = int(self.headers.get("Content-Length", 0))
                payload = self.rfile.read(content_length)

                # Handle event
                try:
                    self._server._handler.handle(payload, signature)
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'{"status": "ok"}')
                except SignatureError as e:
                    logger.warning(f"Signature validation failed: {e}")
                    self.send_error(401, "Invalid signature")
                except Exception as e:
                    logger.exception("Error handling webhook")
                    self.send_error(500, str(e))

            def do_GET(self) -> None:
                """Handle GET request (health check)."""
                if self.path == "/health":
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'{"status": "healthy"}')
                elif self.path == "/events":
                    events = self._server._handler.get_event_log()
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()

                    import json
                    self.wfile.write(json.dumps(events).encode())
                else:
                    self.send_error(404, "Not Found")

            def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
                """Suppress default logging."""
                pass

        # Create and bind server
        handler_factory = lambda *args, **kwargs: WebhookHandler(self)(*args, **kwargs)
        server = HTTPServer((self._host, self._port), lambda *args, **kwargs: WebhookHandler(self)(*args, **kwargs))

        logger.info(f"Webhook server listening on {self._host}:{self._port}")

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            logger.info("Webhook server stopped")
        finally:
            self._running = False
            server.server_close()

    def stop(self) -> None:
        """Stop the webhook server."""
        self._running = False


def start_server(
    host: str = "0.0.0.0",
    port: int = 8080,
    webhook_secret: str | None = None,
    smee_url: str | None = None,
) -> WebhookServer:
    """Start webhook server.

    Args:
        host: Host to bind to
        port: Port to listen on
        webhook_secret: GitHub webhook secret
        smee_url: SMEE.io URL for webhook tunneling (optional)

    Returns:
        WebhookServer instance
    """
    if smee_url:
        logger.info(f"SMEE tunneling URL: {smee_url}")
        logger.info("Configure GitHub webhook to forward to this URL")

    # Get secret from env if not provided
    if not webhook_secret:
        webhook_secret = os.getenv("GITHUB_WEBHOOK_SECRET")

    server = WebhookServer(
        host=host,
        port=port,
        webhook_secret=webhook_secret,
    )

    return server


def start_server_background(
    host: str = "0.0.0.0",
    port: int = 8080,
    webhook_secret: str | None = None,
) -> WebhookServer:
    """Start webhook server in background thread.

    Args:
        host: Host to bind to
        port: Port to listen on
        webhook_secret: GitHub webhook secret

    Returns:
        WebhookServer instance
    """
    import threading

    server = WebhookServer(
        host=host,
        port=port,
        webhook_secret=webhook_secret,
    )

    thread = threading.Thread(target=server.start, daemon=True)
    thread.start()

    logger.info(f"Webhook server started in background on {host}:{port}")

    return server
