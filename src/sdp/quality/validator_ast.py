"""AST helpers for quality gate validation."""

import ast


class ASTHelpers:
    """Helper methods for AST analysis."""

    @staticmethod
    def calculate_complexity(node: ast.AST) -> int:
        """Calculate cyclomatic complexity of an AST node.

        Args:
            node: AST node to analyze.

        Returns:
            Complexity score (higher is more complex).
        """
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, (ast.And, ast.Or)):
                complexity += 1
            elif isinstance(child, (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp)):
                complexity += 1

        return complexity

    @staticmethod
    def count_imports(tree: ast.AST) -> int:
        """Count import statements in AST.

        Args:
            tree: AST to analyze.

        Returns:
            Number of import statements.
        """
        return sum(1 for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom)))

    @staticmethod
    def count_functions(tree: ast.AST) -> int:
        """Count function definitions in AST.

        Args:
            tree: AST to analyze.

        Returns:
            Number of function definitions.
        """
        return sum(
            1 for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        )

    @staticmethod
    def has_line_breaks(source_code: str, start: int, end: int) -> bool:
        """Check if there are line breaks in a range.

        Args:
            source_code: Source code string.
            start: Start position.
            end: End position.

        Returns:
            True if line breaks found.
        """
        segment = source_code[start:end]
        return "\n" in segment
