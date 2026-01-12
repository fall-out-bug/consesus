#!/bin/bash
# Helper script to create commits with Co-authored-by for AI assistance

set -euo pipefail

# Get commit message from arguments or stdin
if [ $# -eq 0 ]; then
    echo "Usage: $0 'commit message'"
    echo "   or: echo 'commit message' | $0"
    exit 1
fi

COMMIT_MSG="$1"

# Add Co-authored-by trailer
FULL_MSG="${COMMIT_MSG}

Co-authored-by: Cursor AI <cursor-ai@cursor.sh>"

# Create commit
git commit -m "$FULL_MSG"

echo "✓ Commit created with Co-authored-by trailer"
