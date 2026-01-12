# Code Patterns Reference

> Used in Phase 2 and Phase 3 for copying standard structures

## Clean Architecture Layers

```
Domain (domain/)
    ↑ Entities, value objects, business rules
Application (application/)
    ↑ Use cases, ports, orchestration
Infrastructure (infrastructure/)
    ↑ DB, Redis, Docker, external adapters
Presentation (cli/, api/)
    ↑ CLI (Click), API (FastAPI)
```

**Development order:** Always inside-out (Domain → Application → Infrastructure → Presentation)

---

## Standard Structures

### State Machine

```python
# states.py
from enum import Enum, auto

class CleanupState(Enum):
    INITIAL = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
```

### Context

```python
# context.py
from dataclasses import dataclass, field
from pathlib import Path
from uuid import uuid4

@dataclass
class CleanupContext:
    execution_root: Path
    correlation_id: str = field(default_factory=lambda: uuid4().hex[:8])
    errors: list[str] = field(default_factory=list)
```

### Protocol

```python
# protocol.py
from typing import Protocol

class CleanupCommand(Protocol):
    def execute(
        self,
        ctx: CleanupContext
    ) -> tuple[CleanupContext, CleanupState]:
        ...
```

### Orchestrator

```python
# orchestrator.py
class CleanupOrchestrator:
    def __init__(
        self,
        commands: dict[CleanupState, CleanupCommand]
    ) -> None:
        self._commands = commands

    def run(self, ctx: CleanupContext) -> CleanupResult:
        state = CleanupState.INITIAL
        while state not in (CleanupState.COMPLETED, CleanupState.FAILED):
            cmd = self._commands.get(state)
            if cmd is None:
                break
            ctx, state = cmd.execute(ctx)
        return CleanupResult(success=state == CleanupState.COMPLETED)
```

### Logging

```python
import structlog
log = structlog.get_logger()

log.info("operation.start", submission_id=sid)
log.error("operation.failed", error=str(e), exc_info=True)
```

---

## Decomposing Large Tasks

### Large File (>200 lines)

```
WS-01: Create tests for structure (TDD: Red)
WS-02: Create structure (states, context, protocol) (TDD: Green)
WS-03: Extract commands/steps + tests
WS-04: Create orchestrator + tests
WS-05: Update original as thin wrapper + refactoring (TDD: Refactor)
```

### New Feature (TDD approach)

```
WS-01: Domain entities — tests BEFORE implementation (Red → Green)
WS-02: Application ports + use case — tests BEFORE implementation (Red → Green)
WS-03: Infrastructure adapter — tests (may be integration) (Red → Green)
WS-04: Presentation (CLI/API) — tests (Red → Green)
WS-05: Refactoring + regression check (Refactor)
```

**TDD Rule:** In each WS, write tests first (Red), then minimal implementation (Green), then refactor.

---

## Additional Patterns

### Repository (Infrastructure layer)

```python
# ports.py (Application)
from typing import Protocol

class SubmissionRepository(Protocol):
    def get_by_id(self, submission_id: str) -> Submission | None:
        ...

    def save(self, submission: Submission) -> None:
        ...

# repository.py (Infrastructure)
class PostgresSubmissionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, submission_id: str) -> Submission | None:
        row = self._session.query(SubmissionModel).filter_by(id=submission_id).first()
        return Submission.from_orm(row) if row else None

    def save(self, submission: Submission) -> None:
        model = SubmissionModel.from_domain(submission)
        self._session.add(model)
        self._session.commit()
```

### Factory (Application/Domain)

```python
# factory.py
class ExecutorFactory:
    def __init__(
        self,
        config: ExecutorConfig,
        logger: structlog.BoundLogger,
    ) -> None:
        self._config = config
        self._logger = logger

    def create(self, executor_type: ExecutorType) -> Executor:
        match executor_type:
            case ExecutorType.DIND:
                return DindExecutor(self._config.dind, self._logger)
            case ExecutorType.K8S:
                return K8sExecutor(self._config.k8s, self._logger)
            case _:
                raise ValueError(f"Unknown executor type: {executor_type}")
```

### Adapter (Infrastructure)

```python
# adapter.py
class GCPStorageAdapter:
    """Adapts GCS to StoragePort interface."""

    def __init__(self, client: storage.Client, bucket_name: str) -> None:
        self._client = client
        self._bucket = self._client.bucket(bucket_name)

    def upload(self, local_path: Path, remote_path: str) -> str:
        blob = self._bucket.blob(remote_path)
        blob.upload_from_filename(str(local_path))
        return blob.public_url

    def download(self, remote_path: str, local_path: Path) -> None:
        blob = self._bucket.blob(remote_path)
        blob.download_to_filename(str(local_path))
```

---

## Anti-patterns (What NOT to do)

### God Object
```python
class HomeworkManager:  # 1500 lines, does everything
    def run(self): ...
    def grade(self): ...
    def publish(self): ...
    def cleanup(self): ...
```
✅ **Instead:** Split into Executor, Grader, Publisher, Cleaner (SRP)

### Anemic Model
```python
@dataclass
class Submission:
    id: str
    status: str  # just data, no logic
```
✅ **Instead:** Add domain methods (`submit()`, `fail()`, `complete()`)

### Leaky Abstraction
```python
# Application layer
def process(submission: Submission):
    sql = f"UPDATE submissions SET status='{submission.status}'"  # SQL in application!
```
✅ **Instead:** Use Repository port

### Circular Dependencies
```python
# module_a.py
from module_b import B

# module_b.py
from module_a import A  # circular import!
```
✅ **Instead:** Protocol in separate file, import via TYPE_CHECKING

### Implicit Dependencies
```python
def process():
    db = get_global_db()  # where did DB come from?
```
✅ **Instead:** Dependency Injection via constructor

---

## Bash Commands Reference

```bash
# Import check
python -c "from myproject.module import Class"

# Tests with coverage
pytest tests/unit/test_module.py -v \
  --cov=src/module \
  --cov-report=term-missing \
  --cov-fail-under=80

# Regression
pytest tests/unit/ -m fast -v

# Code quality
ruff check src/module/ --select=C901
wc -l src/module/*.py

# Type checking (strict typing)
mypy src/module/ --strict --no-implicit-optional
```

---

## Strict Typing (Type Hints Guidelines)

### Required Rules

```python
# ✅ Always specify return type (even for None)
def process(data: str) -> None:
    print(data)

# ❌ Without type hints
def process(data):
    print(data)

# ✅ Use modern syntax (Python 3.10+)
def get_items() -> list[str]:
    return []

# ❌ Old syntax
from typing import List
def get_items() -> List[str]:
    return []

# ✅ Union via |
def find(id: str) -> Submission | None:
    ...

# ❌ Optional
from typing import Optional
def find(id: str) -> Optional[Submission]:
    ...

# ✅ Full signatures in Protocol
class Repository(Protocol):
    def save(self, item: Submission) -> None:
        ...

# ❌ Incomplete signatures
class Repository(Protocol):
    def save(self, item):  # no types!
        ...
```

### Forbidden Constructs

```python
# ❌ Any (except justified cases)
from typing import Any
def process(data: Any) -> Any:  # too broad!
    ...

# ✅ Specific types
def process(data: dict[str, int]) -> list[str]:
    ...

# ❌ Implicit Optional
def get_user(id: str) -> User:  # can return None?
    return None  # mypy error!

# ✅ Explicit Optional
def get_user(id: str) -> User | None:
    return None  # OK
```

### Dataclasses with Types

```python
# ✅ All fields with types
@dataclass
class Config:
    timeout: int
    retries: int = 3
    tags: list[str] = field(default_factory=list)

# ❌ Without types
@dataclass
class Config:
    timeout  # what is this?
    retries = 3  # what type?
```

### CI Check

```bash
# Add to WS completion criteria
mypy src/module/ --strict --no-implicit-optional

# If mypy fails → CHANGES REQUESTED
```

Full list: See `PROTOCOL.md` → Quick Reference
