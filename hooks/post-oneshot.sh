#!/bin/bash
# hooks/post-oneshot.sh
# Post-oneshot validation after autonomous feature execution

set -e

FEATURE="${1:-}"

if [ -z "$FEATURE" ]; then
    echo "Usage: hooks/post-oneshot.sh F{XX}"
    exit 1
fi

echo "Running post-oneshot validation for $FEATURE..."

# Get git root
GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || GIT_ROOT="."
cd "$GIT_ROOT"

#######################################
# 1. Verify all WS completed
#######################################
echo ""
echo "=== WS Completion Check ==="

CHECKPOINT_FILE=".oneshot/${FEATURE}-checkpoint.json"
if [ -f "$CHECKPOINT_FILE" ]; then
    STATUS=$(jq -r '.status' "$CHECKPOINT_FILE" 2>/dev/null || echo "unknown")
    COMPLETED=$(jq -r '.completed_ws | length' "$CHECKPOINT_FILE" 2>/dev/null || echo "0")
    PENDING=$(jq -r '.pending_ws | length' "$CHECKPOINT_FILE" 2>/dev/null || echo "0")
    
    echo "Status: $STATUS"
    echo "Completed WS: $COMPLETED"
    echo "Pending WS: $PENDING"
    
    if [ "$PENDING" -gt 0 ]; then
        echo "⚠️  Some WS still pending"
    else
        echo "✓ All WS completed"
    fi
else
    echo "⚠️  Checkpoint file not found"
fi

#######################################
# 2. Run full test suite
#######################################
echo ""
echo "=== Full Test Suite ==="

if [ -d "tests" ] && command -v poetry &> /dev/null; then
    poetry run pytest tests/ -q --tb=short 2>/dev/null && {
        echo "✓ All tests passed"
    } || {
        echo "⚠️  Some tests failed"
    }
else
    echo "⏭️  Skipping tests"
fi

#######################################
# 3. Coverage check
#######################################
echo ""
echo "=== Coverage Check ==="

if [ -d "tests" ] && command -v poetry &> /dev/null; then
    COVERAGE=$(poetry run pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=80 -q 2>/dev/null | grep "TOTAL" | awk '{print $4}' || echo "unknown")
    echo "Coverage: $COVERAGE"
    
    if [ "$COVERAGE" != "unknown" ]; then
        COV_NUM=${COVERAGE%\%}
        if [ "$COV_NUM" -ge 80 ]; then
            echo "✓ Coverage ≥ 80%"
        else
            echo "⚠️  Coverage below 80%"
        fi
    fi
else
    echo "⏭️  Skipping coverage"
fi

#######################################
# 4. Check for TODO/FIXME
#######################################
echo ""
echo "=== TODO/FIXME Check ==="

if [ -d "src" ]; then
    TODO_COUNT=$(grep -rn "TODO\|FIXME\|HACK\|XXX" src/ 2>/dev/null | wc -l || echo "0")
    if [ "$TODO_COUNT" -gt 0 ]; then
        echo "⚠️  Found $TODO_COUNT TODO/FIXME markers"
    else
        echo "✓ No TODO/FIXME found"
    fi
else
    echo "⏭️  Skipping TODO check"
fi

#######################################
# 5. Generate UAT Guide reminder
#######################################
echo ""
echo "=== UAT Guide ==="

UAT_FILE="docs/uat/${FEATURE}-uat-guide.md"
if [ -f "$UAT_FILE" ]; then
    echo "✓ UAT Guide exists: $UAT_FILE"
else
    echo "⚠️  UAT Guide not found. Generate with /review"
fi

#######################################
# Summary
#######################################
echo ""
echo "================================"
echo "Post-oneshot validation complete: $FEATURE"
echo "================================"
echo ""
echo "Next steps:"
echo "  1. Human: Review UAT Guide"
echo "  2. Human: Complete manual testing"
echo "  3. Human: Sign off UAT"
echo "  4. Run: /deploy $FEATURE"

exit 0
