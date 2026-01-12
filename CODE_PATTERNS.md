# hw_checker Patterns Reference

> Используется в phase-2 и phase-3 для копирования типовых структур

## Clean Architecture Layers

```
Domain (hw_checker/domain/)
    ↑ Entities, value objects, business rules
Application (hw_checker/application/)
    ↑ Use cases, ports, orchestration
Infrastructure (hw_checker/infrastructure/)
    ↑ DB, Redis, Docker, GCP adapters
Presentation (hw_checker/cli/, presentation/)
    ↑ CLI (Click), API (FastAPI)
```

**Порядок разработки:** Всегда inside-out (Domain → Application → Infrastructure → Presentation)

---

## Типовые структуры

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

## Декомпозиция больших задач

### Большой файл (>200 строк)

```
WS-01: Создать тесты для структуры (TDD: Red)
WS-02: Создать структуру (states, context, protocol) (TDD: Green)
WS-03: Извлечь commands/steps + тесты
WS-04: Создать orchestrator + тесты
WS-05: Обновить оригинал как thin wrapper + рефакторинг (TDD: Refactor)
```

### Новая фича (TDD-подход)

```
WS-01: Domain entities — тесты ДО реализации (Red → Green)
WS-02: Application ports + use case — тесты ДО реализации (Red → Green)
WS-03: Infrastructure adapter — тесты (может быть integration) (Red → Green)
WS-04: Presentation (CLI/API) — тесты (Red → Green)
WS-05: Рефакторинг + regression check (Refactor)
```

**Правило TDD:** В каждом WS сначала пишутся тесты (Red), затем минимальная реализация (Green), затем рефакторинг.

---

## Дополнительные паттерны

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
    """Адаптирует GCS к интерфейсу StoragePort."""
    
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

## Антипаттерны (что НЕ делать)

### ❌ God Object
```python
class HomeworkManager:  # 1500 строк, делает всё
    def run(self): ...
    def grade(self): ...
    def publish(self): ...
    def cleanup(self): ...
```
✅ **Вместо этого:** Разбить на Executor, Grader, Publisher, Cleaner (SRP)

### ❌ Анемичная модель
```python
@dataclass
class Submission:
    id: str
    status: str  # просто данные, нет логики
```
✅ **Вместо этого:** Добавить domain методы (`submit()`, `fail()`, `complete()`)

### ❌ Leaky Abstraction
```python
# Application слой
def process(submission: Submission):
    sql = f"UPDATE submissions SET status='{submission.status}'"  # SQL в application!
```
✅ **Вместо этого:** Использовать Repository port

### ❌ Circular Dependencies
```python
# module_a.py
from module_b import B

# module_b.py
from module_a import A  # циклический импорт!
```
✅ **Вместо этого:** Protocol в отдельном файле, импорт через TYPE_CHECKING

### ❌ Implicit Dependencies
```python
def process():
    db = get_global_db()  # где взялась БД?
```
✅ **Вместо этого:** Dependency Injection через конструктор

---

## Bash Commands Reference

```bash
# Import check
python -c "from hw_checker.module import Class"

# Tests with coverage
pytest tests/unit/test_module.py -v \
  --cov=hw_checker/module \
  --cov-report=term-missing \
  --cov-fail-under=80

# Regression
pytest tests/unit/ -m fast -v

# Code quality
ruff check hw_checker/module/ --select=C901
wc -l hw_checker/module/*.py

# Type checking (строгая типизация)
mypy hw_checker/module/ --strict --no-implicit-optional
```

---

## Строгая типизация (Type Hints Guidelines)

### Обязательные правила

```python
# ✅ Всегда указывай возвращаемый тип (даже для None)
def process(data: str) -> None:
    print(data)

# ❌ Без type hints
def process(data):
    print(data)

# ✅ Используй modern syntax (Python 3.10+)
def get_items() -> list[str]:
    return []

# ❌ Старый синтаксис
from typing import List
def get_items() -> List[str]:
    return []

# ✅ Union через |
def find(id: str) -> Submission | None:
    ...

# ❌ Optional
from typing import Optional
def find(id: str) -> Optional[Submission]:
    ...

# ✅ Полные сигнатуры в Protocol
class Repository(Protocol):
    def save(self, item: Submission) -> None:
        ...

# ❌ Неполные сигнатуры
class Repository(Protocol):
    def save(self, item):  # нет типов!
        ...
```

### Запрещённые конструкции

```python
# ❌ Any (кроме обоснованных случаев)
from typing import Any
def process(data: Any) -> Any:  # слишком широко!
    ...

# ✅ Конкретные типы
def process(data: dict[str, int]) -> list[str]:
    ...

# ❌ Неявные Optional
def get_user(id: str) -> User:  # может вернуть None?
    return None  # mypy error!

# ✅ Явный Optional
def get_user(id: str) -> User | None:
    return None  # OK
```

### Dataclasses с типами

```python
# ✅ Все поля с типами
@dataclass
class Config:
    timeout: int
    retries: int = 3
    tags: list[str] = field(default_factory=list)

# ❌ Без типов
@dataclass
class Config:
    timeout  # что это?
    retries = 3  # какой тип?
```

### Проверка в CI

```bash
# Добавь в критерии завершения WS
mypy hw_checker/module/ --strict --no-implicit-optional

# Если mypy не проходит → CHANGES REQUESTED
```

Полный список: `@sdp/PROTOCOL.md` → Quick Reference

