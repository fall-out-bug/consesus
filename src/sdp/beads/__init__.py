"""
SDP + Beads Integration.

This module provides integration between SDP (Spec-Driven Protocol) and Beads
(git-backed issue tracker for AI agents).

Key components:
- BeadsClient: Interface for interacting with Beads
- MockBeadsClient: In-memory mock for development/testing
- CLIBeadsClient: Real Beads via CLI subprocess
- BeadsSyncService: Bidirectional sync between SDP workstreams and Beads tasks

Usage:
    from sdp.beads import create_beads_client, BeadsSyncService

    # Create client (mock for development, real for production)
    client = create_beads_client(use_mock=True)  # Mock
    client = create_beads_client()  # Real (requires Beads installed)

    # Create sync service
    sync = BeadsSyncService(client)

    # Sync workstream to Beads
    result = sync.sync_workstream_to_beads("docs/workstreams/backlog/00-001-01.md")
    print(f"Created Beads task: {result.beads_id}")
"""

from .client import (
    BeadsClient,
    MockBeadsClient,
    CLIBeadsClient,
    create_beads_client,
    BeadsClientError,
)
from .models import (
    BeadsTask,
    BeadsTaskCreate,
    BeadsStatus,
    BeadsPriority,
    BeadsDependency,
    BeadsDependencyType,
    BeadsSyncResult,
)

__all__ = [
    # Client
    "BeadsClient",
    "MockBeadsClient",
    "CLIBeadsClient",
    "create_beads_client",
    "BeadsClientError",
    # Models
    "BeadsTask",
    "BeadsTaskCreate",
    "BeadsStatus",
    "BeadsPriority",
    "BeadsDependency",
    "BeadsDependencyType",
    "BeadsSyncResult",
]

__version__ = "0.1.0"
