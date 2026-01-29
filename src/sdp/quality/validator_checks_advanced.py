"""Advanced quality gate checks (complexity, architecture, documentation, security, performance)."""

import ast
import re
from pathlib import Path
from typing import cast

from sdp.quality.architecture import ArchitectureChecker
from sdp.quality.models import QualityGateConfig as QualityGateConfigModel
from sdp.quality.validator_ast import ASTHelpers
from sdp.quality.validator_models import QualityGateViolation


class AdvancedQualityChecks:
    """Advanced quality gate validation methods."""

    def __init__(
        self,
        config: QualityGateConfigModel,
        violations: list[QualityGateViolation],
    ) -> None:
        self._config = config
        self._violations = violations
        self._architecture_checker = ArchitectureChecker(config.architecture, violations)

    def check_complexity(self, path: Path, tree: ast.AST) -> None:
        """Check cyclomatic complexity."""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                complexity = ASTHelpers.calculate_complexity(node)
                if complexity > self._config.complexity.max_cc:
                    self._violations.append(
                        QualityGateViolation(
                            "complexity",
                            str(path),
                            node.lineno,
                            f"Function '{node.name}' has complexity {complexity} "
                            f"(max: {self._config.complexity.max_cc})",
                            "error",
                        )
                    )

    def check_architecture(self, path: Path, tree: ast.AST) -> None:
        """Check architecture layer violations using portable ArchitectureChecker."""
        self._architecture_checker.check_architecture(path, tree)

    def check_documentation(self, path: Path, tree: ast.AST) -> None:
        """Check documentation requirements."""
        documentation = self._config.documentation
        if documentation is not None and documentation.require_module_docstrings:
            has_module_docstring = ast.get_docstring(cast(ast.Module, tree)) is not None
            if not has_module_docstring:
                self._violations.append(
                    QualityGateViolation(
                        "documentation",
                        str(path),
                        1,
                        "Module missing docstring",
                        "warning",
                    )
                )

    def check_security(self, path: Path, source_code: str) -> None:
        """Check for security issues."""
        security = self._config.security
        if security is not None and security.forbid_hardcoded_secrets:
            # Check for common secret patterns
            secret_patterns = [
                r'password\s*=\s*["\']([^"\']+)["\']',
                r'api_key\s*=\s*["\']([^"\']+)["\']',
                r'secret\s*=\s*["\']([^"\']+)["\']',
                r'token\s*=\s*["\']([^"\']+)["\']',
            ]

            for pattern in secret_patterns:
                matches = re.finditer(pattern, source_code, re.IGNORECASE)
                for match in matches:
                    line_num = source_code[: match.start()].count("\n") + 1
                    self._violations.append(
                        QualityGateViolation(
                            "security",
                            str(path),
                            line_num,
                            "Possible hardcoded secret detected",
                            "error",
                        )
                    )

        security = self._config.security
        if security is not None and security.forbid_eval_usage:
            if "eval(" in source_code:
                line_num = source_code.index("eval(")
                line_num = source_code[:line_num].count("\n") + 1
                self._violations.append(
                    QualityGateViolation(
                        "security",
                        str(path),
                        line_num,
                        "Use of eval() detected (security risk)",
                        "error",
                    )
                )

    def check_performance(self, path: Path, tree: ast.AST) -> None:
        """Check performance anti-patterns."""
        performance = self._config.performance
        if performance is None:
            return

        if performance.max_nesting_depth is not None:
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    depth = self._calculate_nesting_depth(node)
                    if depth > performance.max_nesting_depth:
                        self._violations.append(
                            QualityGateViolation(
                                "performance",
                                str(path),
                                node.lineno,
                                f"Function '{node.name}' has nesting depth {depth} "
                                f"(max: {performance.max_nesting_depth})",
                                "warning",
                            )
                        )

    def _calculate_nesting_depth(self, node: ast.AST) -> int:
        """Calculate maximum nesting depth in a function."""
        max_depth = 0

        def _depth_at(child_node: ast.AST, current_depth: int) -> None:
            nonlocal max_depth
            max_depth = max(max_depth, current_depth)
            for grandchild in ast.iter_child_nodes(child_node):
                if isinstance(
                    grandchild,
                    (ast.If, ast.While, ast.For, ast.AsyncFor, ast.With, ast.With, ast.Try),
                ):
                    _depth_at(grandchild, current_depth + 1)

        _depth_at(node, 0)
        return max_depth
