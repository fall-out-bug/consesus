#!/bin/bash
# hooks/pre-deploy.sh
# Pre-deployment validation

set -e

FEATURE="${1:-}"

if [ -z "$FEATURE" ]; then
    echo "Usage: hooks/pre-deploy.sh F{XX}"
    exit 1
fi

echo "Running pre-deploy checks for $FEATURE..."

# Get git root
GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || GIT_ROOT="."
cd "$GIT_ROOT"

#######################################
# 1. Check all WS are APPROVED
#######################################
echo ""
echo "=== Review Status Check ==="

if [ -d "docs/workstreams" ]; then
    WS_FILES=$(find docs/workstreams -name "WS-${FEATURE#F}*.md" 2>/dev/null || true)
    
    if [ -n "$WS_FILES" ]; then
        ALL_APPROVED=true
        for WS_FILE in $WS_FILES; do
            if ! grep -q "APPROVED" "$WS_FILE" 2>/dev/null; then
                echo "⚠️  Not approved: $WS_FILE"
                ALL_APPROVED=false
            fi
        done
        
        if [ "$ALL_APPROVED" = true ]; then
            echo "✓ All WS approved"
        else
            echo ""
            echo "BLOCKED: Not all WS are approved"
            exit 1
        fi
    else
        echo "⚠️  No WS files found for $FEATURE"
    fi
else
    echo "⏭️  Skipping review check (no workstreams dir)"
fi

#######################################
# 2. Check UAT completed
#######################################
echo ""
echo "=== UAT Status Check ==="

UAT_FILE="docs/uat/${FEATURE}-uat-guide.md"
if [ -f "$UAT_FILE" ]; then
    if grep -q "\[x\].*APPROVED" "$UAT_FILE" 2>/dev/null; then
        echo "✓ UAT signed off"
    else
        echo "⚠️  UAT not signed off in $UAT_FILE"
        echo "   Human must complete UAT testing"
    fi
else
    echo "⚠️  UAT guide not found: $UAT_FILE"
fi

#######################################
# 3. Run full test suite
#######################################
echo ""
echo "=== Full Test Suite ==="

if [ -d "tests" ] && command -v poetry &> /dev/null; then
    poetry run pytest tests/ -q --tb=short 2>/dev/null && {
        echo "✓ All tests passed"
    } || {
        echo "BLOCKED: Tests failed"
        exit 1
    }
else
    echo "⏭️  Skipping tests"
fi

#######################################
# 4. Check coverage
#######################################
echo ""
echo "=== Coverage Check ==="

if [ -d "tests" ] && command -v poetry &> /dev/null; then
    poetry run pytest tests/ --cov=src --cov-fail-under=80 -q 2>/dev/null && {
        echo "✓ Coverage ≥ 80%"
    } || {
        echo "BLOCKED: Coverage below 80%"
        exit 1
    }
else
    echo "⏭️  Skipping coverage"
fi

#######################################
# Summary
#######################################
echo ""
echo "================================"
echo "Pre-deploy checks complete: $FEATURE"
echo "================================"
echo ""
echo "Ready for deployment!"

exit 0
