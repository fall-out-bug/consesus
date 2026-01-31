"""DEPRECATED: Use sdp.core.feature submodule instead.

This module provides backward compatibility by re-exporting from the feature package.
"""

import warnings

from sdp.core.feature import (
    CircularDependencyError,
    Feature,
    MissingDependencyError,
    load_feature_from_directory,
    load_feature_from_spec,
)

warnings.warn(
    "Importing from sdp.core.feature module directly is deprecated. "
    "Use 'from sdp.core.feature import ...' instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "CircularDependencyError",
    "MissingDependencyError",
    "Feature",
    "load_feature_from_directory",
    "load_feature_from_spec",
]
