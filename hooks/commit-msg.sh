#!/bin/bash
# sdp/hooks/commit-msg.sh
# Git commit-msg hook for conventional commits validation
# Install: ln -sf ../../sdp/hooks/commit-msg.sh .git/hooks/commit-msg

COMMIT_MSG_FILE=$1
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

echo "🔍 Validating commit message..."

# Conventional commits pattern
# type(scope): description
# Types: feat, fix, docs, test, refactor, style, chore, perf, ci, build
PATTERN="^(feat|fix|docs|test|refactor|style|chore|perf|ci|build)(\([a-z0-9_-]+\))?: .{1,}"

# Also allow merge commits and revert commits
MERGE_PATTERN="^Merge "
REVERT_PATTERN="^Revert "

# Get first line of commit message
FIRST_LINE=$(echo "$COMMIT_MSG" | head -1)

# Check patterns
if echo "$FIRST_LINE" | grep -qE "$PATTERN"; then
    echo "✓ Valid conventional commit"
    exit 0
fi

if echo "$FIRST_LINE" | grep -qE "$MERGE_PATTERN"; then
    echo "✓ Merge commit"
    exit 0
fi

if echo "$FIRST_LINE" | grep -qE "$REVERT_PATTERN"; then
    echo "✓ Revert commit"
    exit 0
fi

# Invalid commit message
echo ""
echo "❌ Invalid commit message format!"
echo ""
echo "Expected: type(scope): description"
echo "Got:      $FIRST_LINE"
echo ""
echo "Valid types:"
echo "  feat     - New feature"
echo "  fix      - Bug fix"
echo "  docs     - Documentation"
echo "  test     - Tests"
echo "  refactor - Refactoring"
echo "  style    - Formatting"
echo "  chore    - Maintenance"
echo "  perf     - Performance"
echo "  ci       - CI/CD"
echo "  build    - Build system"
echo ""
echo "Examples:"
echo "  feat(lms): WS-060-01 - implement domain layer"
echo "  test(lms): WS-060-01 - add unit tests"
echo "  docs(lms): WS-060-01 - execution report"
echo "  fix(grading): resolve race condition in worker"
echo ""
echo "Scope should match feature slug (e.g., lms, grading, api)"

exit 1
