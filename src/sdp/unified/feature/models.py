"""Models for @feature skill orchestrator.

Provides data models for feature execution state, phases, and skip flags.
"""

from dataclasses import dataclass, field
from enum import Enum


class FeaturePhase(str, Enum):
    """Feature development phases."""

    REQUIREMENTS = "requirements"
    ARCHITECTURE = "architecture"
    EXECUTION = "execution"


@dataclass
class SkipFlags:
    """Skip flags for bypassing approval gates."""

    skip_requirements: bool = False
    skip_architecture: bool = False
    skip_uat: bool = False


@dataclass
class FeatureExecution:
    """Feature execution state.

    Tracks progress through @feature workflow phases including
    requirements, architecture, and execution with skip flag support.
    """

    feature_id: str
    feature_name: str
    skip_flags: SkipFlags = field(default_factory=SkipFlags)
    completed_phases: list[FeaturePhase] = field(default_factory=list)
    status: str = "in_progress"
