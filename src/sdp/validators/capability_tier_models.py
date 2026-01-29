"""Capability tier validation data models."""


from dataclasses import dataclass, field
from enum import Enum


class CapabilityTier(str, Enum):
    """SDP capability tier levels."""

    T0 = "T0"
    T1 = "T1"
    T2 = "T2"
    T3 = "T3"


@dataclass
class ValidationCheck:
    """Single validation check result."""

    name: str
    passed: bool
    message: str
    details: list[str] = field(default_factory=list)


@dataclass
class ValidationResult:
    """Result of tier validation."""

    tier: CapabilityTier
    passed: bool
    checks: list[ValidationCheck]
    errors: list[str] = field(default_factory=list)
