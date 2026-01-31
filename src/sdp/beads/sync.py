"""
Bidirectional sync between SDP workstreams and Beads tasks.

This module is split into smaller modules for better maintainability.
Import from the sub-modules:
- mapping: MappingManager, resolve_ws_id_to_beads_id, BeadsSyncError
- status_mapper: map_sdp_status_to_beads, map_beads_status_to_sdp, map_sdp_size_to_beads_priority
- sync_service: BeadsSyncService

This module remains for backward compatibility.
"""

# Re-export all public APIs for backward compatibility
from .sync.mapping import BeadsSyncError, resolve_ws_id_to_beads_id  # noqa: F401
from .sync.sync_service import BeadsSyncService  # noqa: F401

__all__ = [
    "BeadsSyncError",
    "resolve_ws_id_to_beads_id",
    "BeadsSyncService",
]
