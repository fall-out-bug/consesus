#!/usr/bin/env python3
"""Migrate workstream IDs to PP-FFF-SS format with validation and dry-run support.

This script standardizes workstream IDs across the SDP protocol by:
1. Converting WS-FFF-SS → PP-FFF-SS format
2. Adding project_id field to frontmatter
3. Updating filenames to match new format
4. Validating all references and dependencies

Usage:
    python scripts/migrate_workstream_ids.py --dry-run
    python scripts/migrate_workstream_ids.py --project-id 00
    python scripts/migrate_workstream_ids.py --project-id 02 --path ../hw_checker

Examples:
    # Dry run for SDP (project 00)
    python scripts/migrate_workstream_ids.py --dry-run

    # Migrate SDP workstreams
    python scripts/migrate_workstream_ids.py --project-id 00

    # Migrate hw_checker workstreams
    python scripts/migrate_workstream_ids.py --project-id 02 --path ../hw_checker
"""

import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sdp.scripts import WorkstreamMigrator, WorkstreamMigrationError


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Migrate workstream IDs to PP-FFF-SS format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--project-id",
        default="00",
        help="Project ID (default: 00 for SDP)",
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=Path.cwd(),
        help="Path to project root (default: current directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform dry run without making changes",
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()

    try:
        migrator = WorkstreamMigrator(
            root_path=args.path,
            project_id=args.project_id,
            dry_run=args.dry_run,
        )
        stats = migrator.migrate()

        # Exit with error code if any failures
        return 1 if stats["failed"] > 0 else 0

    except WorkstreamMigrationError as e:
        print(f"❌ Migration error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n\n⚠️  Migration cancelled by user")
        return 130
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
