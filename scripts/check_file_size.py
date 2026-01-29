#!/usr/bin/env python3
"""Check that Python files do not exceed size limits.

This script ensures all Python files in src/ are under 200 LOC
to maintain AI-readiness and code quality.
"""

import sys
from pathlib import Path


def count_loc(file_path: Path) -> int:
    """Count lines of code in a Python file.

    Args:
        file_path: Path to Python file

    Returns:
        Number of non-blank, non-comment lines
    """
    lines = file_path.read_text(encoding='utf-8').splitlines()
    loc = 0

    for line in lines:
        stripped = line.strip()
        # Skip empty lines and comments
        if stripped and not stripped.startswith('#'):
            loc += 1

    return loc


def check_file_sizes(max_loc: int = 200) -> bool:
    """Check all Python files in src/ for size violations.

    Args:
        max_loc: Maximum allowed lines of code per file

    Returns:
        True if all files pass, False otherwise
    """
    src_path = Path('src/sdp')
    violations = []

    for py_file in src_path.rglob('*.py'):
        loc = count_loc(py_file)

        if loc > max_loc:
            violations.append({
                'file': py_file,
                'loc': loc,
                'limit': max_loc
            })

    if violations:
        print(f"❌ Found {len(violations)} file(s) exceeding {max_loc} LOC limit:", file=sys.stderr)
        for v in sorted(violations, key=lambda x: x['loc'], reverse=True):
            print(f"  {v['file']}: {v['loc']} LOC (limit: {v['limit']})", file=sys.stderr)
        return False

    print(f"✅ All files under {max_loc} LOC")
    return True


if __name__ == '__main__':
    if not check_file_sizes():
        sys.exit(1)
    sys.exit(0)
