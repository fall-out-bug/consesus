"""Basic quality gate checks (file_size, type_hints, error_handling)."""

import ast
from pathlib import Path

from sdp.quality.models import QualityGateConfig as QualityGateConfigModel
from sdp.quality.validator_ast import ASTHelpers
from sdp.quality.validator_models import QualityGateViolation


class BasicQualityChecks:
    """Basic quality gate validation methods."""

    def __init__(
        self,
        config: QualityGateConfigModel,
        violations: list[QualityGateViolation],
    ) -> None:
        self._config = config
        self._violations = violations

    def check_file_size(self, path: Path, source_code: str, tree: ast.AST) -> None:
        """Check file size limits."""
        lines = source_code.split("\n")
        line_count = len(lines)

        if line_count > self._config.file_size.max_lines:
            self._violations.append(
                QualityGateViolation(
                    "file_size",
                    str(path),
                    None,
                    f"File too large: {line_count} lines (max: {self._config.file_size.max_lines})",
                    "error",
                )
            )

        # Count imports
        import_count = ASTHelpers.count_imports(tree)
        if import_count > self._config.file_size.max_imports:
            self._violations.append(
                QualityGateViolation(
                    "imports",
                    str(path),
                    None,
                    f"Too many imports: {import_count} (max: {self._config.file_size.max_imports})",
                    "warning",
                )
            )

        # Count functions
        function_count = ASTHelpers.count_functions(tree)
        if function_count > self._config.file_size.max_functions:
            self._violations.append(
                QualityGateViolation(
                    "functions",
                    str(path),
                    None,
                    f"Too many functions: {function_count} (max: {self._config.file_size.max_functions})",  # noqa: E501
                    "warning",
                )
            )

    def check_type_hints(self, path: Path, tree: ast.AST) -> None:
        """Check type hint requirements."""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Check return type
                if (
                    self._config.type_hints.require_return_types
                    and node.returns is None
                ):
                    self._violations.append(
                        QualityGateViolation(
                            "type_hints",
                            str(path),
                            node.lineno,
                            f"Function '{node.name}' missing return type annotation",
                            "error",
                        )
                    )

                # Check parameter types
                if self._config.type_hints.require_param_types:
                    for arg in node.args.args:
                        if arg.arg != "self" and arg.annotation is None:
                            self._violations.append(
                                QualityGateViolation(
                                    "type_hints",
                                    str(path),
                                    arg.lineno,
                                    f"Parameter '{arg.arg}' of function '{node.name}' "
                                    "missing type annotation",
                                    "warning",
                                )
                            )

    def check_error_handling(self, path: Path, tree: ast.AST) -> None:
        """Check error handling patterns."""
        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                # Check for bare except
                for handler in node.handlers:
                    if handler.type is None:  # bare except
                        if self._config.error_handling.forbid_bare_except:
                            self._violations.append(
                                QualityGateViolation(
                                    "error_handling",
                                    str(path),
                                    handler.lineno,
                                    "Bare except clause detected",
                                    "error",
                                )
                            )
