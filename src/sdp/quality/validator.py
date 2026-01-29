"""Quality gate validator implementation."""

import ast
from pathlib import Path
from typing import Any

from sdp.quality.config import QualityGateConfigLoader
from sdp.quality.models import QualityGateConfig as QualityGateConfigModel
from sdp.quality.validator_checks_advanced import AdvancedQualityChecks
from sdp.quality.validator_checks_basic import BasicQualityChecks
from sdp.quality.validator_models import QualityGateViolation


class QualityGateValidator:
    """Validates code against quality gate configuration."""

    def __init__(
        self,
        config: QualityGateConfigModel | None = None,
        config_path: str | Path | None = None,
    ) -> None:
        """Initialize validator.

        Args:
            config: Pre-loaded configuration object. If None, loads from config_path.
            config_path: Path to quality-gate.toml file.
        """
        if config:
            self._config = config
        else:
            loader = QualityGateConfigLoader(config_path)
            errors = loader.validate()
            if errors:
                raise ValueError("Invalid configuration:\n" + "\n".join(f"  - {e}" for e in errors))
            self._config = loader.config

        self._violations: list[QualityGateViolation] = []
        self._basic_checks = BasicQualityChecks(self._config, self._violations)
        self._advanced_checks = AdvancedQualityChecks(self._config, self._violations)

    @property
    def violations(self) -> list[QualityGateViolation]:
        """Get list of violations found during validation."""
        return self._violations

    def validate_file(self, file_path: str | Path) -> list[QualityGateViolation]:
        """Validate a single Python file against all enabled quality gates.

        Args:
            file_path: Path to Python file to validate.

        Returns:
            List of violations found.
        """
        # Clear existing violations instead of creating new list
        self._violations.clear()
        path = Path(file_path)

        if not path.exists():
            self._violations.append(
                QualityGateViolation("file_not_found", str(path), None, "File not found", "error")
            )
            return self._violations

        if not path.suffix == ".py":
            self._violations.append(
                QualityGateViolation("invalid_file", str(path), None, "Not a Python file", "error")
            )
            return self._violations

        try:
            source_code = path.read_text()
            tree = ast.parse(source_code, filename=str(path))

            # Run all enabled checks
            self._run_all_checks(path, source_code, tree)

        except SyntaxError as e:
            self._violations.append(
                QualityGateViolation(
                    "syntax_error",
                    str(path),
                    e.lineno,
                    f"Syntax error: {e.msg}",
                    "error",
                )
            )

        return self._violations

    def validate_directory(
        self,
        directory: str | Path,
        pattern: str = "*.py",
        recursive: bool = True,
    ) -> list[QualityGateViolation]:
        """Validate all Python files in a directory.

        Args:
            directory: Path to directory to validate.
            pattern: Glob pattern for files to match (default: "*.py").
            recursive: Whether to search recursively (default: True).

        Returns:
            List of all violations found.
        """
        # Clear existing violations instead of creating new list
        self._violations.clear()
        dir_path = Path(directory)

        if not dir_path.exists():
            self._violations.append(
                QualityGateViolation("dir_not_found", str(dir_path), None, "Directory not found", "error")
            )
            return self._violations

        if recursive:
            files = dir_path.rglob(pattern)
        else:
            files = dir_path.glob(pattern)

        for file_path in files:
            if file_path.is_file():
                self.validate_file(file_path)

        return self._violations

    def _run_all_checks(self, path: Path, source_code: str, tree: ast.AST) -> None:
        """Run all enabled quality checks on a file."""
        if self._config.file_size.enabled:
            self._basic_checks.check_file_size(path, source_code, tree)

        if self._config.complexity.enabled:
            self._advanced_checks.check_complexity(path, tree)

        if self._config.type_hints.enabled:
            self._basic_checks.check_type_hints(path, tree)

        if self._config.error_handling.enabled:
            self._basic_checks.check_error_handling(path, tree)

        if self._config.architecture.enabled:
            self._advanced_checks.check_architecture(path, tree)

        if self._config.documentation and self._config.documentation.enabled:
            self._advanced_checks.check_documentation(path, tree)

        if self._config.security and self._config.security.enabled:
            self._advanced_checks.check_security(path, source_code)

        if self._config.performance and self._config.performance.enabled:
            self._advanced_checks.check_performance(path, tree)

    def get_summary(self) -> dict[str, Any]:
        """Get summary of validation results."""
        errors = [v for v in self._violations if v.severity == "error"]
        warnings = [v for v in self._violations if v.severity == "warning"]

        by_category: dict[str, int] = {}
        for violation in self._violations:
            by_category[violation.category] = by_category.get(violation.category, 0) + 1

        return {
            "total": len(self._violations),
            "errors": len(errors),
            "warnings": len(warnings),
            "by_category": by_category,
        }

    def print_report(self) -> None:
        """Print validation report to stdout."""
        summary = self.get_summary()

        print(f"\n{'='*60}")
        print("Quality Gate Validation Report")
        print(f"{'='*60}")
        print(f"Total violations: {summary['total']}")
        print(f"  Errors: {summary['errors']}")
        print(f"  Warnings: {summary['warnings']}")

        if summary['by_category']:
            print("\nViolations by category:")
            for category, count in sorted(summary['by_category'].items()):
                print(f"  {category}: {count}")

        if self._violations:
            print(f"\n{'='*60}")
            print("Detailed violations:")
            print(f"{'='*60}")
            for violation in self._violations:
                print(violation)

        print(f"{'='*60}\n")
