#!/bin/bash
# hooks/post-build.sh
# Post-build validation for completed workstream

set -e

WS_ID="${1:-}"
MODULE="${2:-}"

if [ -z "$WS_ID" ]; then
    echo "Usage: hooks/post-build.sh WS-XXX [module]"
    exit 1
fi

echo "Running post-build checks for $WS_ID..."

# Get git root and navigate there
GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || GIT_ROOT="."
cd "$GIT_ROOT"

#######################################
# 1. Unit Tests
#######################################
echo ""
echo "=== Unit Tests ==="

if [ -d "tests/unit" ] && command -v poetry &> /dev/null; then
    poetry run pytest tests/unit/ -m fast -q --tb=short 2>/dev/null && {
        echo "✓ Fast tests passed"
    } || {
        echo "⚠️  Some fast tests failed"
        echo "   Run: poetry run pytest tests/unit/ -m fast -v"
    }
else
    echo "⏭️  Skipping tests"
fi

#######################################
# 2. Coverage Check
#######################################
echo ""
echo "=== Coverage Check ==="

if [ -d "tests/unit" ] && command -v poetry &> /dev/null; then
    if [ -n "$MODULE" ]; then
        poetry run pytest tests/unit/ --cov="src/$MODULE" --cov-report=term-missing --cov-fail-under=80 -q 2>/dev/null && {
            echo "✓ Coverage ≥ 80%"
        } || {
            echo "⚠️  Coverage may be below 80%"
        }
    else
        echo "⏭️  Skipping coverage (no module specified)"
    fi
else
    echo "⏭️  Skipping coverage"
fi

#######################################
# 3. Linters
#######################################
echo ""
echo "=== Linters ==="

if [ -d "src" ] && command -v poetry &> /dev/null; then
    poetry run ruff check src/ --quiet 2>/dev/null && {
        echo "✓ Ruff passed"
    } || {
        echo "⚠️  Ruff found issues"
    }
    
    poetry run mypy src/ --ignore-missing-imports --no-error-summary 2>/dev/null && {
        echo "✓ Mypy passed"
    } || {
        echo "⚠️  Mypy found issues"
    }
else
    echo "⏭️  Skipping linters"
fi

#######################################
# 4. TODO/FIXME Check
#######################################
echo ""
echo "=== TODO/FIXME Check ==="

if [ -d "src" ]; then
    TODO_COUNT=$(grep -rn "TODO\|FIXME\|HACK\|XXX" src/ 2>/dev/null | wc -l || echo "0")
    if [ "$TODO_COUNT" -gt 0 ]; then
        echo "⚠️  Found $TODO_COUNT TODO/FIXME markers"
        grep -rn "TODO\|FIXME" src/ 2>/dev/null | head -5
    else
        echo "✓ No TODO/FIXME found"
    fi
else
    echo "⏭️  Skipping TODO check"
fi

#######################################
# 5. Import Check
#######################################
echo ""
echo "=== Import Check ==="

if [ -n "$MODULE" ] && command -v python &> /dev/null; then
    IMPORT_PATH="$MODULE"
    python -c "import $IMPORT_PATH" 2>/dev/null && {
        echo "✓ Module imports successfully"
    } || {
        echo "⚠️  Module import failed"
    }
else
    echo "⏭️  Skipping import check"
fi

#######################################
# Summary
#######################################
echo ""
echo "================================"
echo "Post-build checks complete: $WS_ID"
echo "================================"
echo ""
echo "Next steps:"
echo "  1. Append Execution Report to WS file"
echo "  2. Commit changes"
echo "  3. Continue to next WS or run /review"

exit 0
