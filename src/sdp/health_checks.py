"""Health checks for SDP doctor command.

Defines diagnostic checks for SDP installation and configuration.
"""

import subprocess
import sys
from pathlib import Path
from typing import Callable


class HealthCheckResult:
    """Result of a health check.

    Attributes:
        name: Check name
        passed: Whether check passed
        message: Human-readable message
        remediation: How to fix failure (optional)
    """

    def __init__(
        self,
        name: str,
        passed: bool,
        message: str,
        remediation: str | None = None,
    ) -> None:
        """Initialize health check result.

        Args:
            name: Check name
            passed: Whether check passed
            message: Human-readable message
            remediation: How to fix failure (optional)
        """
        self.name = name
        self.passed = passed
        self.message = message
        self.remediation = remediation


class HealthCheck:
    """Base class for health checks.

    Attributes:
        name: Check name
        critical: Whether check is critical (failure = non-zero exit)
        check_fn: Function to run check
    """

    def __init__(
        self,
        name: str,
        critical: bool,
        check_fn: Callable[[], HealthCheckResult],
    ) -> None:
        """Initialize health check.

        Args:
            name: Check name
            critical: Whether check is critical
            check_fn: Function to run check
        """
        self.name = name
        self.critical = critical
        self._check_fn = check_fn

    def run(self) -> HealthCheckResult:
        """Run the health check.

        Returns:
            HealthCheckResult
        """
        return self._check_fn()


def _check_python_version() -> HealthCheckResult:
    """Check Python version >= 3.10.

    Returns:
        HealthCheckResult
    """
    version = sys.version_info
    if version >= (3, 10):
        return HealthCheckResult(
            name="Python Version",
            passed=True,
            message=f"Python {version.major}.{version.minor}.{version.micro}",
        )
    else:
        return HealthCheckResult(
            name="Python Version",
            passed=False,
            message=f"Python {version.major}.{version.minor} (requires >= 3.10)",
            remediation="Upgrade to Python 3.10 or later",
        )


def _check_poetry() -> HealthCheckResult:
    """Check Poetry installation.

    Returns:
        HealthCheckResult
    """
    try:
        result = subprocess.run(
            ["poetry", "--version"],
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            version = result.stdout.decode().strip()
            return HealthCheckResult(
                name="Poetry",
                passed=True,
                message=version,
            )
        else:
            return HealthCheckResult(
                name="Poetry",
                passed=False,
                message="Poetry not found",
                remediation="Install Poetry: curl -sSL https://install.python-poetry.org | python3 -",
            )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return HealthCheckResult(
            name="Poetry",
            passed=False,
            message="Poetry not found",
            remediation="Install Poetry: curl -sSL https://install.python-poetry.org | python3 -",
        )


def _check_git_hooks() -> HealthCheckResult:
    """Check git hooks configuration.

    Returns:
        HealthCheckResult
    """
    cwd = Path.cwd()
    git_dir = cwd / ".git"

    if not git_dir.exists():
        return HealthCheckResult(
            name="Git Hooks",
            passed=False,
            message="Not a git repository",
            remediation="Initialize git: git init",
        )

    hooks_dir = git_dir / "hooks"
    pre_commit = hooks_dir / "pre-commit"

    if pre_commit.exists():
        return HealthCheckResult(
            name="Git Hooks",
            passed=True,
            message="pre-commit hook installed",
        )
    else:
        return HealthCheckResult(
            name="Git Hooks",
            passed=False,
            message="pre-commit hook not installed",
            remediation="Run: sdp init",
        )


def _check_beads() -> HealthCheckResult:
    """Check Beads CLI (optional).

    Returns:
        HealthCheckResult
    """
    try:
        result = subprocess.run(
            ["beads", "--version"],
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            version = result.stdout.decode().strip()
            return HealthCheckResult(
                name="Beads CLI",
                passed=True,
                message=version,
            )
        else:
            return HealthCheckResult(
                name="Beads CLI",
                passed=False,
                message="Not installed (optional)",
            )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return HealthCheckResult(
            name="Beads CLI",
            passed=False,
            message="Not installed (optional)",
        )


def _check_github_cli() -> HealthCheckResult:
    """Check GitHub CLI (optional).

    Returns:
        HealthCheckResult
    """
    try:
        result = subprocess.run(
            ["gh", "--version"],
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            version = result.stdout.decode().strip()
            return HealthCheckResult(
                name="GitHub CLI",
                passed=True,
                message=version,
            )
        else:
            return HealthCheckResult(
                name="GitHub CLI",
                passed=False,
                message="Not installed (optional)",
            )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return HealthCheckResult(
            name="GitHub CLI",
            passed=False,
            message="Not installed (optional)",
        )


def _check_telegram() -> HealthCheckResult:
    """Check Telegram configuration (optional).

    Returns:
        HealthCheckResult
    """
    env_file = Path.cwd() / ".env"

    if not env_file.exists():
        return HealthCheckResult(
            name="Telegram",
            passed=False,
            message="Not configured (optional)",
        )

    content = env_file.read_text()
    has_token = "TELEGRAM_BOT_TOKEN" in content
    has_chat_id = "TELEGRAM_CHAT_ID" in content

    if has_token and has_chat_id:
        return HealthCheckResult(
            name="Telegram",
            passed=True,
            message="Configured",
        )
    else:
        return HealthCheckResult(
            name="Telegram",
            passed=False,
            message="Not configured (optional)",
        )


def get_health_checks() -> list[HealthCheck]:
    """Get all health checks.

    Returns:
        List of HealthCheck objects
    """
    return [
        HealthCheck("Python Version", True, _check_python_version),
        HealthCheck("Poetry", True, _check_poetry),
        HealthCheck("Git Hooks", True, _check_git_hooks),
        HealthCheck("Beads CLI", False, _check_beads),
        HealthCheck("GitHub CLI", False, _check_github_cli),
        HealthCheck("Telegram", False, _check_telegram),
    ]
