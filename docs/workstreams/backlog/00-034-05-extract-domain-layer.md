---
ws_id: 00-034-05
feature: F034
status: READY
complexity: MEDIUM
project_id: "00"
depends_on:
  - 00-034-01
---

# Workstream: Extract Domain Layer

**ID:** 00-034-05  
**Feature:** F034 (A+ Quality Initiative)  
**Status:** READY  
**Owner:** AI Agent  
**Complexity:** MEDIUM (~500 LOC refactoring)

---

## Goal

Создать чистый domain layer `src/sdp/domain/` с Pure domain entities, устранив нарушение Clean Architecture (beads/ → core/).

---

## Context

**Текущая проблема:**

```
beads/skills_oneshot.py ──imports──> core/workstream.py
beads/sync_service.py   ──imports──> core/workstream.py
```

Это нарушает Clean Architecture: `beads/` (infrastructure) не должен напрямую зависеть от `core/` (application).

**Решение:** Извлечь pure domain types в `sdp/domain/`, от которого могут зависеть все модули.

**Целевая архитектура:**
```
                    ┌─────────────┐
                    │   domain/   │  ← Pure entities, no deps
                    └─────────────┘
                          ↑
            ┌─────────────┼─────────────┐
            │             │             │
      ┌─────────┐   ┌─────────┐   ┌─────────┐
      │  core/  │   │ beads/  │   │ unified/│
      └─────────┘   └─────────┘   └─────────┘
```

---

## Scope

### In Scope
- ✅ Create `src/sdp/domain/` package
- ✅ Extract pure domain entities from `core/`
- ✅ Update imports in `beads/`, `core/`, `unified/`
- ✅ Add dependency linting rule
- ✅ Document architecture in `docs/concepts/clean-architecture/`

### Out of Scope
- ❌ Full Clean Architecture migration (too large)
- ❌ Splitting `core/` into application/infrastructure
- ❌ Changing external APIs

---

## Dependencies

**Depends On:**
- [x] 00-034-01: Split Large Files (Phase 1) — workstream.py already split

**Blocks:**
- 00-034-03: Increase Test Coverage (cleaner structure = easier testing)

---

## Acceptance Criteria

- [ ] `src/sdp/domain/` exists with pure entities
- [ ] `grep -r "from sdp.core" src/sdp/beads/` returns 0 results
- [ ] `grep -r "from sdp.core" src/sdp/unified/` returns 0 results (except allowed)
- [ ] All tests pass
- [ ] Architecture documented

---

## Implementation Plan

### Task 1: Create Domain Package Structure

```
src/sdp/domain/
├── __init__.py           # Public exports
├── workstream.py         # Workstream, WorkstreamStatus, WorkstreamScope
├── feature.py            # Feature, FeatureStatus
├── project.py            # Project, Release
├── exceptions.py         # DomainError, ValidationError
└── value_objects.py      # WorkstreamId, FeatureId, Scope
```

### Task 2: Extract Workstream Domain Entities

**From `core/workstream/models.py` → `domain/workstream.py`:**

```python
# src/sdp/domain/workstream.py
"""Pure domain entities for workstreams."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class WorkstreamStatus(Enum):
    """Workstream lifecycle status."""
    BACKLOG = "backlog"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    DONE = "done"


class WorkstreamScope(Enum):
    """Workstream size classification."""
    SMALL = "small"      # < 500 LOC
    MEDIUM = "medium"    # 500-1500 LOC
    LARGE = "large"      # > 1500 LOC (should split)


@dataclass(frozen=True)
class WorkstreamId:
    """Value object for workstream identifier."""
    project: str   # PP
    feature: str   # FFF
    sequence: str  # SS
    
    def __str__(self) -> str:
        return f"{self.project}-{self.feature}-{self.sequence}"
    
    @classmethod
    def parse(cls, ws_id: str) -> "WorkstreamId":
        """Parse PP-FFF-SS format."""
        parts = ws_id.split("-")
        if len(parts) != 3:
            raise ValueError(f"Invalid WS ID: {ws_id}")
        return cls(project=parts[0], feature=parts[1], sequence=parts[2])


@dataclass
class Workstream:
    """Core workstream entity."""
    id: WorkstreamId
    title: str
    status: WorkstreamStatus
    scope: WorkstreamScope
    goal: str
    depends_on: list[WorkstreamId]
    
    # Optional metadata
    owner: Optional[str] = None
    feature_id: Optional[str] = None
```

### Task 3: Extract Feature Domain Entities

**From `core/feature.py` → `domain/feature.py`:**

```python
# src/sdp/domain/feature.py
"""Pure domain entities for features."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from .workstream import WorkstreamId


class FeatureStatus(Enum):
    """Feature lifecycle status."""
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"


@dataclass
class Feature:
    """Core feature entity."""
    id: str
    title: str
    status: FeatureStatus
    workstreams: list[WorkstreamId] = field(default_factory=list)
    description: Optional[str] = None
```

### Task 4: Create Domain Exceptions

```python
# src/sdp/domain/exceptions.py
"""Domain-level exceptions."""


class DomainError(Exception):
    """Base exception for domain errors."""
    pass


class ValidationError(DomainError):
    """Validation constraint violated."""
    pass


class WorkstreamNotFoundError(DomainError):
    """Workstream does not exist."""
    pass


class DependencyCycleError(DomainError):
    """Circular dependency detected."""
    pass
```

### Task 5: Update Imports in beads/

**Before:**
```python
# beads/skills_oneshot.py
from sdp.core.workstream import Workstream, WorkstreamStatus
```

**After:**
```python
# beads/skills_oneshot.py
from sdp.domain.workstream import Workstream, WorkstreamStatus
```

**Files to update:**
- [ ] `beads/skills_oneshot.py`
- [ ] `beads/sync_service.py`
- [ ] `beads/skills_design.py`
- [ ] `beads/skills_build.py`
- [ ] `beads/scope_manager.py`

### Task 6: Update Imports in core/

**Keep core/ using domain:**
```python
# core/workstream/parser.py
from sdp.domain.workstream import Workstream, WorkstreamStatus, WorkstreamId
```

**Files to update:**
- [ ] `core/workstream/parser.py`
- [ ] `core/workstream/validator.py`
- [ ] `core/decomposition.py`
- [ ] `core/feature.py`

### Task 7: Add Deprecation Warnings

```python
# core/workstream/models.py (DEPRECATED)
import warnings
from sdp.domain.workstream import *  # Re-export

warnings.warn(
    "Import from sdp.domain.workstream instead of sdp.core.workstream.models",
    DeprecationWarning,
    stacklevel=2
)
```

### Task 8: Add Dependency Linting

**Create `scripts/check_architecture.py`:**

```python
#!/usr/bin/env python3
"""Check Clean Architecture dependency rules."""

import ast
import sys
from pathlib import Path

FORBIDDEN_IMPORTS = {
    "sdp/beads/": ["sdp.core"],
    "sdp/unified/": ["sdp.core"],  # except allowed
    "sdp/domain/": ["sdp.core", "sdp.beads", "sdp.unified", "sdp.cli"],
}

def check_imports(file: Path, forbidden: list[str]) -> list[str]:
    """Check file for forbidden imports."""
    violations = []
    tree = ast.parse(file.read_text())
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            module = node.module if isinstance(node, ast.ImportFrom) else None
            if module and any(module.startswith(f) for f in forbidden):
                violations.append(f"{file}:{node.lineno}: imports {module}")
    return violations

# ... main logic
```

### Task 9: Update Architecture Documentation

**Update `docs/concepts/clean-architecture/README.md`:**

- Add domain layer description
- Update dependency diagram
- Document allowed/forbidden imports

---

## DO / DON'T

### Domain Layer

**✅ DO:**
- Keep domain entities pure (no external deps)
- Use dataclasses for entities
- Use Enum for status values
- Use value objects for identifiers

**❌ DON'T:**
- Import anything from core/, beads/, unified/ in domain/
- Add I/O operations to domain entities
- Add framework dependencies (pydantic, etc.) to domain
- Put business logic that needs external services

---

## Files to Create

- [ ] `src/sdp/domain/__init__.py`
- [ ] `src/sdp/domain/workstream.py`
- [ ] `src/sdp/domain/feature.py`
- [ ] `src/sdp/domain/project.py`
- [ ] `src/sdp/domain/exceptions.py`
- [ ] `src/sdp/domain/value_objects.py`
- [ ] `scripts/check_architecture.py`
- [ ] `tests/unit/domain/test_workstream.py`
- [ ] `tests/unit/domain/test_feature.py`

## Files to Modify

- [ ] `src/sdp/beads/*.py` (5+ files)
- [ ] `src/sdp/core/*.py` (5+ files)
- [ ] `src/sdp/unified/*.py` (if needed)
- [ ] `docs/concepts/clean-architecture/README.md`

---

## Test Plan

### Unit Tests
- [ ] Domain entities are instantiable
- [ ] Value objects are immutable
- [ ] Exceptions have correct hierarchy
- [ ] WorkstreamId.parse() handles edge cases

### Architecture Tests
- [ ] `scripts/check_architecture.py` passes
- [ ] No forbidden imports in domain/
- [ ] No beads/ → core/ imports

### Regression
- [ ] All existing tests pass
- [ ] CLI commands work

---

**Version:** 1.0  
**Created:** 2026-01-31
