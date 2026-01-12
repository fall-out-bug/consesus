#!/bin/bash
# sdp/hooks/post-build.sh
# Post-build checks for /build command
# Usage: ./post-build.sh WS-060-01 [module_path]

set -e

WS_ID=$1
MODULE=${2:-""}

if [ -z "$WS_ID" ]; then
    echo "❌ Usage: ./post-build.sh WS-ID [module_path]"
    exit 1
fi

echo "🔍 Post-build checks for $WS_ID"
echo "================================"

cd tools/hw_checker

# Check 1: Fast tests (regression)
echo ""
echo "Check 1: Regression tests"
if poetry run pytest tests/unit/ -m fast -q --tb=no 2>/dev/null; then
    FAST_COUNT=$(poetry run pytest tests/unit/ -m fast --collect-only -q 2>/dev/null | tail -1 | grep -oE "[0-9]+" | head -1 || echo "0")
    echo "✓ Regression tests passed ($FAST_COUNT tests)"
else
    echo "❌ Regression tests failed"
    echo "   Run: cd tools/hw_checker && poetry run pytest tests/unit/ -m fast -v"
    exit 1
fi

# Check 2: Linters
echo ""
echo "Check 2: Linters"

if [ -n "$MODULE" ]; then
    LINT_PATH="src/hw_checker/$MODULE"
else
    LINT_PATH="src/hw_checker/"
fi

# Ruff
if poetry run ruff check "$LINT_PATH" --quiet 2>/dev/null; then
    echo "✓ Ruff: no issues"
else
    echo "⚠️ Ruff found issues (run: ruff check $LINT_PATH)"
fi

# Mypy (optional, soft fail)
if poetry run mypy "$LINT_PATH" --ignore-missing-imports --no-error-summary 2>/dev/null; then
    echo "✓ Mypy: no issues"
else
    echo "⚠️ Mypy found issues (run: mypy $LINT_PATH)"
fi

# Check 3: TODO/FIXME
echo ""
echo "Check 3: No TODO/FIXME"
if [ -n "$MODULE" ]; then
    TODO_PATH="src/hw_checker/$MODULE"
else
    TODO_PATH="src/hw_checker/"
fi

TODO_COUNT=$(grep -rn "TODO\|FIXME\|HACK\|XXX" "$TODO_PATH" 2>/dev/null | wc -l || echo "0")
if [ "$TODO_COUNT" -eq 0 ]; then
    echo "✓ No TODO/FIXME markers"
else
    echo "❌ Found $TODO_COUNT TODO/FIXME markers"
    grep -rn "TODO\|FIXME\|HACK\|XXX" "$TODO_PATH" 2>/dev/null | head -5
    exit 1
fi

# Check 4: File sizes
echo ""
echo "Check 4: File sizes (< 200 LOC)"
LARGE_FILES=$(find "$TODO_PATH" -name "*.py" -exec wc -l {} \; 2>/dev/null | awk '$1 > 200 {print $2 " (" $1 " lines)"}')
if [ -z "$LARGE_FILES" ]; then
    echo "✓ All files < 200 LOC"
else
    echo "⚠️ Large files found:"
    echo "$LARGE_FILES"
fi

# Check 5: Import check
echo ""
echo "Check 5: Import check"
if [ -n "$MODULE" ]; then
    IMPORT_PATH="hw_checker.$MODULE"
    if python -c "import $IMPORT_PATH" 2>/dev/null; then
        echo "✓ Module imports successfully"
    else
        echo "⚠️ Module import failed (run: python -c 'import $IMPORT_PATH')"
    fi
else
    echo "  Skipped (no module specified)"
fi

# Check 6: Coverage (if tests exist for module)
echo ""
echo "Check 6: Coverage"
if [ -n "$MODULE" ]; then
    TEST_FILE="tests/unit/test_${MODULE}.py"
    if [ -f "$TEST_FILE" ]; then
        COV_RESULT=$(poetry run pytest "$TEST_FILE" --cov="hw_checker/$MODULE" --cov-report=term-missing --cov-fail-under=80 -q 2>&1)
        if echo "$COV_RESULT" | grep -q "PASSED\|passed"; then
            COV_PCT=$(echo "$COV_RESULT" | grep -oE "[0-9]+%" | head -1 || echo "N/A")
            echo "✓ Coverage: $COV_PCT (≥80%)"
        else
            echo "⚠️ Coverage check failed"
            echo "   Run: pytest $TEST_FILE --cov=hw_checker/$MODULE --cov-fail-under=80"
        fi
    else
        echo "  Skipped (no test file: $TEST_FILE)"
    fi
else
    echo "  Skipped (no module specified)"
fi

echo ""
echo "================================"
echo "✅ Post-build checks PASSED"
echo ""
echo "Next steps:"
echo "1. Append Execution Report to WS file"
echo "2. Run /build for next WS (if any)"
echo "3. After all WS: /review {feature}"
