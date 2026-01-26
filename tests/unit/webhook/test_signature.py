"""Tests for webhook signature validation."""

import pytest

from sdp.webhook.signature import SignatureError, SignatureValidator


def test_signature_validator_init() -> None:
    """Test validator initialization."""
    validator = SignatureValidator("test_secret")
    assert validator._secret == "test_secret"


def test_signature_validator_no_secret() -> None:
    """Test validator without secret always validates."""
    validator = SignatureValidator()
    assert validator.validate(b"payload", None) is True


def test_sign_and_validate() -> None:
    """Test signing and validating payloads."""
    validator = SignatureValidator("my_secret")

    payload = b'{"test": "data"}'
    signature = validator.sign(payload)

    assert signature.startswith("sha256=")
    assert validator.validate(payload, signature) is True


def test_validate_valid_signature() -> None:
    """Test validating a valid signature."""
    validator = SignatureValidator("my_secret")

    payload = b'{"test": "data"}'
    # Manually compute expected signature
    import hmac
    import hashlib

    expected = hmac.new(
        b"my_secret",
        payload,
        hashlib.sha256,
    ).hexdigest()
    signature_header = f"sha256={expected}"

    assert validator.validate(payload, signature_header) is True


def test_validate_missing_header() -> None:
    """Test validation fails without signature header."""
    validator = SignatureValidator("my_secret")

    with pytest.raises(SignatureError, match="Missing signature"):
        validator.validate(b"payload", None)


def test_validate_invalid_format() -> None:
    """Test validation fails with invalid format."""
    validator = SignatureValidator("my_secret")

    with pytest.raises(SignatureError, match="Invalid signature format"):
        validator.validate(b"payload", "invalid_format")


def test_validate_signature_mismatch() -> None:
    """Test validation fails with wrong signature."""
    validator = SignatureValidator("my_secret")

    with pytest.raises(SignatureError, match="Signature mismatch"):
        validator.validate(b"payload", "sha256=wrong_signature")


def test_sign_without_secret() -> None:
    """Test signing without secret raises error."""
    validator = SignatureValidator()

    with pytest.raises(SignatureError):
        validator.sign(b"payload")


def test_validate_with_empty_secret() -> None:
    """Test validation with empty secret skips validation."""
    validator = SignatureValidator("")

    # Should not raise even with invalid signature
    assert validator.validate(b"payload", "invalid") is True


def test_sign_produces_deterministic_result() -> None:
    """Test signing produces same result for same input."""
    validator = SignatureValidator("test_secret")
    payload = b'{"data": "value"}'

    sig1 = validator.sign(payload)
    sig2 = validator.sign(payload)

    assert sig1 == sig2
