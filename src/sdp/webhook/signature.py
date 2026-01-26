"""GitHub webhook signature validation."""

from __future__ import annotations

import hashlib
import hmac
import logging

logger = logging.getLogger(__name__)


class SignatureError(Exception):
    """Raised when webhook signature validation fails."""

    pass


class SignatureValidator:
    """Validates GitHub webhook signatures.

    Uses HMAC-SHA256 to verify webhook payloads.
    """

    def __init__(self, webhook_secret: str | None = None) -> None:
        """Initialize signature validator.

        Args:
            webhook_secret: GitHub webhook secret (optional for testing)
        """
        self._secret = webhook_secret or ""

    def validate(
        self,
        payload: bytes,
        signature_header: str | None,
    ) -> bool:
        """Validate webhook payload signature.

        Args:
            payload: Raw request body bytes
            signature_header: Value of X-Hub-Signature-256 header

        Returns:
            True if signature is valid

        Raises:
            SignatureError: If signature is invalid
        """
        if not self._secret:
            logger.warning("No webhook secret configured, skipping validation")
            return True

        if not signature_header:
            raise SignatureError("Missing signature header")

        if not signature_header.startswith("sha256="):
            raise SignatureError(f"Invalid signature format: {signature_header[:10]}...")

        # Extract signature
        signature = signature_header[7:]  # Remove "sha256=" prefix

        # Compute expected signature
        expected = hmac.new(
            self._secret.encode(),
            payload,
            hashlib.sha256,
        ).hexdigest()

        # Constant-time comparison to prevent timing attacks
        if not hmac.compare_digest(expected, signature):
            raise SignatureError("Signature mismatch")

        return True

    def sign(self, payload: bytes) -> str:
        """Generate signature for payload (useful for testing).

        Args:
            payload: Raw payload bytes

        Returns:
            Signature header value (e.g., "sha256=abc123...")
        """
        if not self._secret:
            raise SignatureError("Cannot sign without webhook secret")

        signature = hmac.new(
            self._secret.encode(),
            payload,
            hashlib.sha256,
        ).hexdigest()

        return f"sha256={signature}"
