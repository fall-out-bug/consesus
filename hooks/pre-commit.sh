#!/bin/bash
# hooks/pre-commit.sh
# Pre-commit hook for SDP projects

set -e

echo "Running pre-commit checks..."

# Get git root
GIT_ROOT=$(git rev-parse --show-toplevel)
cd "$GIT_ROOT"

#######################################
# 1. Check for TODO/FIXME in staged files
#######################################
echo ""
echo "=== Checking for TODO/FIXME ==="

STAGED_PY=$(git diff --cached --name-only --diff-filter=ACM | grep "\.py$" || true)

if [ -n "$STAGED_PY" ]; then
    TODO_FOUND=false
    for FILE in $STAGED_PY; do
        if grep -n "TODO\|FIXME\|HACK\|XXX" "$FILE" 2>/dev/null; then
            echo "WARNING: TODO/FIXME found in $FILE"
            TODO_FOUND=true
        fi
    done
    
    if [ "$TODO_FOUND" = true ]; then
        echo ""
        echo "⚠️  TODO/FIXME markers found in staged files."
        echo "   Remove them or create separate WS for tracking."
        # Not blocking, just warning
    else
        echo "✓ No TODO/FIXME in staged files"
    fi
fi

#######################################
# 2. Check file sizes
#######################################
echo ""
echo "=== Checking file sizes ==="

if [ -n "$STAGED_PY" ]; then
    LARGE_FILES=false
    for FILE in $STAGED_PY; do
        if [ -f "$FILE" ]; then
            LINES=$(wc -l < "$FILE")
            if [ "$LINES" -gt 200 ]; then
                echo "WARNING: $FILE has $LINES lines (limit: 200)"
                LARGE_FILES=true
            fi
        fi
    done
    
    if [ "$LARGE_FILES" = true ]; then
        echo ""
        echo "⚠️  Large files detected. Consider splitting."
        # Not blocking, just warning
    else
        echo "✓ All Python files under 200 lines"
    fi
fi

#######################################
# 3. Check type hints (basic)
#######################################
echo ""
echo "=== Checking type hints ==="

if [ -n "$STAGED_PY" ]; then
    MISSING_HINTS=false
    for FILE in $STAGED_PY; do
        if [ -f "$FILE" ]; then
            # Check for functions without return type hints
            NO_RETURN=$(grep -n "def.*):$" "$FILE" 2>/dev/null || true)
            if [ -n "$NO_RETURN" ]; then
                echo "WARNING: Functions without return type in $FILE:"
                echo "$NO_RETURN"
                MISSING_HINTS=true
            fi
        fi
    done
    
    if [ "$MISSING_HINTS" = true ]; then
        echo ""
        echo "⚠️  Some functions missing return type hints."
        # Not blocking, just warning
    else
        echo "✓ Return type hints present"
    fi
fi

#######################################
# 4. Check Clean Architecture (domain imports)
#######################################
echo ""
echo "=== Checking Clean Architecture ==="

DOMAIN_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep "domain/.*\.py$" || true)

if [ -n "$DOMAIN_FILES" ]; then
    BAD_IMPORTS=$(git diff --cached -- $DOMAIN_FILES | grep -E "^\+.*from .*(infrastructure|presentation)" || true)
    
    if [ -n "$BAD_IMPORTS" ]; then
        echo "BLOCKED: Domain layer importing infrastructure/presentation"
        echo ""
        echo "Offending imports:"
        echo "$BAD_IMPORTS"
        echo ""
        echo "Domain layer must NOT import from:"
        echo "  - infrastructure/*"
        echo "  - presentation/*"
        exit 1
    else
        echo "✓ Clean Architecture: domain layer clean"
    fi
fi

#######################################
# 5. Run linters (if available)
#######################################
echo ""
echo "=== Running linters ==="

if command -v poetry &> /dev/null && [ -f "pyproject.toml" ]; then
    # Ruff check (fast)
    if poetry run ruff check --quiet $STAGED_PY 2>/dev/null; then
        echo "✓ Ruff check passed"
    else
        echo "⚠️  Ruff found issues (not blocking)"
    fi
else
    echo "⏭️  Skipping linters (poetry not available)"
fi

#######################################
# 6. Run fast tests (if available)
#######################################
echo ""
echo "=== Running fast tests ==="

if command -v poetry &> /dev/null && [ -d "tests/unit" ]; then
    if poetry run pytest tests/unit/ -m fast -q --tb=no 2>/dev/null; then
        echo "✓ Fast tests passed"
    else
        echo "⚠️  Some fast tests failed (check before push)"
    fi
else
    echo "⏭️  Skipping tests (poetry or tests not available)"
fi

#######################################
# Summary
#######################################
echo ""
echo "================================"
echo "Pre-commit checks complete"
echo "================================"

exit 0
