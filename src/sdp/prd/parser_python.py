"""Python annotation parser.

This module extracts PRD flow annotations from Python source files.
"""

import ast
import re
from pathlib import Path

from .annotations import FlowStep


def parse_python_annotations(path: Path) -> list[FlowStep]:
    """Parse @prd_flow and @prd_step decorators from Python file.

    This function uses regex to find decorator patterns in Python files.
    It looks for @prd_flow("name") and @prd_step(N, "desc") patterns.

    Args:
        path: Path to the Python file

    Returns:
        List of FlowStep objects found in the file
    """
    try:
        content = path.read_text()
    except Exception:
        return []

    steps = []

    # Pattern 1: @prd_flow("name") followed by @prd_step(N, "desc")
    # Pattern 2: @prd_step(N, "desc") followed by @prd_flow("name")
    # Pattern 3: @prd_flow("name") without step (step_number defaults to 0)

    # Combined pattern to match both orders
    flow_pattern = re.compile(
        r'@prd_flow\(["\']([^"\']+)["\']\)\s*\n'
        r'(?:@prd_step\((\d+),\s*["\']([^"\']+)["\']\)\s*\n)?'
        r'(?:async\s+)?def\s+(\w+)',
        re.MULTILINE
    )

    for match in flow_pattern.finditer(content):
        flow_name = match.group(1)
        step_num_str = match.group(2)
        step_desc = match.group(3)
        func_name = match.group(4)

        # Determine step number and description
        if step_num_str:
            step_num = int(step_num_str)
            desc = step_desc or f"{func_name}"
        else:
            step_num = 0
            desc = func_name

        # Calculate line number
        line_number = content[:match.start()].count('\n') + 1

        steps.append(FlowStep(
            flow_name=flow_name,
            step_number=step_num,
            description=desc,
            source_file=path,
            line_number=line_number
        ))

    return steps


def parse_directory(directory: Path, pattern: str = "**/*.py") -> list[FlowStep]:
    """Parse all Python files in directory matching pattern.

    Args:
        directory: Root directory to search
        pattern: Glob pattern for files (default: "**/*.py")

    Returns:
        List of FlowStep objects from all matching files
    """
    all_steps = []

    try:
        for file in directory.glob(pattern):
            # Skip common non-source directories
            if any(skip in str(file) for skip in ["venv", ".venv", "__pycache__", ".tox", "node_modules", ".git"]):
                continue

            if file.is_file():
                all_steps.extend(parse_python_annotations(file))
    except Exception:
        pass

    return all_steps


def parse_python_annotations_ast(path: Path) -> list[FlowStep]:
    """Parse @prd_flow and @prd_step decorators using AST.

    This is an alternative implementation using Python's AST module.
    It's more robust but may fail on syntax errors.

    Args:
        path: Path to the Python file

    Returns:
        List of FlowStep objects found in the file
    """
    try:
        content = path.read_text()
        tree = ast.parse(content, filename=str(path))
    except Exception:
        # Fall back to regex if AST parsing fails
        return parse_python_annotations(path)

    visitor = _PRDVisitor(path)
    visitor.visit(tree)
    return visitor.steps


class _PRDVisitor(ast.NodeVisitor):
    """AST visitor that extracts PRD annotations."""

    def __init__(self, path: Path) -> None:
        self.steps: list[FlowStep] = []
        self.current_flow: str | None = None
        self.path = path

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definition and extract decorators."""
        flow_data = self._extract_flow_data(node)
        if flow_data:
            self.steps.append(flow_data)
        self.generic_visit(node)

    def _extract_flow_data(self, node: ast.FunctionDef) -> FlowStep | None:
        """Extract flow data from function decorators.

        Args:
            node: Function definition node

        Returns:
            FlowStep if decorators found, None otherwise
        """
        flow_name = None
        step_number = None
        description = None

        # Check decorators
        for decorator in node.decorator_list:
            if not isinstance(decorator, ast.Call):
                continue

            if not hasattr(decorator.func, 'id'):
                continue

            # @prd_flow("name")
            if decorator.func.id == 'prd_flow':
                flow_name = self._extract_flow_name(decorator)

            # @prd_step(N, "desc")
            elif decorator.func.id == 'prd_step':
                step_number, description = self._extract_step_data(decorator)

        if not flow_name:
            return None

        # Set defaults
        if step_number is None:
            step_number = 0
        if description is None:
            description = node.name

        # Normalize types
        flow_name = self._normalize_string(flow_name)
        step_number = self._normalize_int(step_number)
        description = self._normalize_string(description)

        return FlowStep(
            flow_name=flow_name,
            step_number=step_number,
            description=description,
            source_file=self.path,
            line_number=node.lineno
        )

    def _extract_flow_name(self, decorator: ast.Call) -> str | None:
        """Extract flow name from @prd_flow decorator."""
        if decorator.args and isinstance(decorator.args[0], ast.Constant):
            value = decorator.args[0].value
            if isinstance(value, str):
                return value
        return None

    def _extract_step_data(self, decorator: ast.Call) -> tuple[str | None, str | None]:
        """Extract step number and description from @prd_step decorator."""
        step_number = None
        description = None

        if len(decorator.args) >= 2:
            if isinstance(decorator.args[0], ast.Constant):
                value = decorator.args[0].value
                if isinstance(value, (int, str)):
                    step_number = value
            if isinstance(decorator.args[1], ast.Constant):
                value = decorator.args[1].value
                if isinstance(value, str):
                    description = value

        return step_number, description

    def _normalize_string(self, value: str | None) -> str:
        """Normalize value to string."""
        if not isinstance(value, str):
            value = str(value) if value else ""
        return value

    def _normalize_int(self, value: int | str | None) -> int:
        """Normalize value to integer."""
        if isinstance(value, int):
            return value
        if isinstance(value, str) and value.isdigit():
            return int(value)
        return 0

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Visit async function definition."""
        # Treat async functions the same as regular functions
        # Create a fake FunctionDef-like object with same attributes
        class _FuncDefWrapper:
            def __init__(self, async_node: ast.AsyncFunctionDef):
                self.name = async_node.name
                self.decorator_list = async_node.decorator_list
                self.lineno = async_node.lineno

        wrapper = _FuncDefWrapper(node)
        self.visit_FunctionDef(wrapper)  # type: ignore[arg-type]

    visitor = PRDVisitor()
    visitor.visit(tree)

    return steps
