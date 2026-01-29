"""SDP init wizard - Re-exports for backwards compatibility."""

from sdp.init_dependencies import detect_dependencies, show_dependencies
from sdp.init_files import (
    collect_metadata,
    create_env_template,
    create_structure,
    generate_quality_gate,
)
from sdp.init_validation import install_git_hooks, run_doctor

__all__ = [
    "collect_metadata",
    "detect_dependencies",
    "show_dependencies",
    "create_structure",
    "generate_quality_gate",
    "create_env_template",
    "install_git_hooks",
    "run_doctor",
]
