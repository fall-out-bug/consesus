# Workstreams: hw_checker Refactoring

**Формат:** Каждый WS — самодостаточный one-shot промпт для субагента.  
**Контекст:** Приватный репозиторий, приоритет — AI-Readiness.

---

## WS-01: Удаление дубликата DinD Executor

### Контекст
Существуют две реализации DinD executor:
- `hw_checker/infrastructure/dind/executor.py` — 1193 строки (дубликат)
- `src/hw_checker/infrastructure/dind/executor.py` — 922 строки (основная)

### Задача
Удалить дубликат, оставить только `src/hw_checker/`.

### Входные файлы
- `tools/hw_checker/hw_checker/infrastructure/dind/` — удалить
- `tools/hw_checker/src/hw_checker/` — основная реализация

### Шаги
1. Найти все импорты `from hw_checker.infrastructure.dind`
2. Заменить на `from src.hw_checker.infrastructure.dind` или убедиться что pyproject.toml правильно настроен
3. Удалить директорию `hw_checker/infrastructure/dind/`
4. Запустить `pytest -x` для проверки

### Ожидаемый результат
- Директория `hw_checker/infrastructure/dind/` удалена
- Все тесты проходят
- Нет broken imports

### Критерий завершения
```bash
# Должно вернуть пустой результат:
find tools/hw_checker -path "*hw_checker/infrastructure/dind*" -type f
# Тесты проходят:
cd tools/hw_checker && pytest -x --tb=short
```

---

## WS-02: Декомпозиция docker_cleanup.py — States & Context

### Контекст
`application/stages/docker_cleanup.py` имеет CC=81, 569 строк — невозможно безопасно редактировать AI.

### Задача
Создать базовые модули: states, context, protocol.

### Входные файлы
- `src/hw_checker/application/stages/docker_cleanup.py`

### Шаги
1. Создать директорию `application/stages/docker_cleanup/`
2. Создать `states.py`:
```python
from enum import Enum, auto

class CleanupState(Enum):
    INITIAL = auto()
    DISCOVERING_COMPOSE = auto()
    COMPOSE_DOWN_RUNNING = auto()
    FORCE_KILL_PENDING = auto()
    NETWORK_CLEANUP = auto()
    VOLUME_CLEANUP = auto()
    COMPLETED = auto()
    FAILED = auto()
```

3. Создать `context.py`:
```python
from dataclasses import dataclass, field
from pathlib import Path
import uuid

@dataclass
class CleanupContext:
    execution_root: Path
    submission_id: str
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    compose_files: list[Path] = field(default_factory=list)
    container_ids: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

@dataclass(frozen=True)
class CleanupResult:
    success: bool
    errors: list[str] = field(default_factory=list)
```

4. Создать `protocol.py`:
```python
from typing import Protocol
from .states import CleanupState
from .context import CleanupContext

class CleanupCommand(Protocol):
    def execute(self, ctx: CleanupContext) -> tuple[CleanupContext, CleanupState]:
        ...
```

5. Создать `__init__.py` с re-exports

### Ожидаемый результат
```
application/stages/docker_cleanup/
├── __init__.py
├── states.py      # < 20 строк
├── context.py     # < 40 строк
└── protocol.py    # < 15 строк
```

### Критерий завершения
```bash
python -c "from hw_checker.application.stages.docker_cleanup import CleanupState, CleanupContext, CleanupCommand"
```

---

## WS-03: Декомпозиция docker_cleanup.py — Commands

### Контекст
Продолжение WS-02. Базовые модули созданы, теперь нужны команды.

### Зависимость
WS-02 завершён.

### Входные файлы
- `application/stages/docker_cleanup.py` — исходная логика
- `application/stages/docker_cleanup/` — структура из WS-02

### Шаги
1. Создать `commands/discover.py`:
```python
from pathlib import Path
from ..context import CleanupContext
from ..states import CleanupState

class DiscoverComposeFilesCommand:
    def execute(self, ctx: CleanupContext) -> tuple[CleanupContext, CleanupState]:
        compose_files = list(ctx.execution_root.rglob("docker-compose*.y*ml"))
        if not compose_files:
            return ctx, CleanupState.NETWORK_CLEANUP
        
        new_ctx = CleanupContext(
            execution_root=ctx.execution_root,
            submission_id=ctx.submission_id,
            correlation_id=ctx.correlation_id,
            compose_files=compose_files,
        )
        return new_ctx, CleanupState.COMPOSE_DOWN_RUNNING
```

2. Создать `commands/compose_down.py` — логика docker-compose down с fallback на docker compose
3. Создать `commands/force_kill.py` — логика docker rm -f по label
4. Создать `commands/network_cleanup.py` — логика очистки сетей
5. Каждый файл < 60 строк, CC < 8

### Ожидаемый результат
```
application/stages/docker_cleanup/commands/
├── __init__.py
├── discover.py        # < 40 строк
├── compose_down.py    # < 60 строк
├── force_kill.py      # < 50 строк
└── network_cleanup.py # < 40 строк
```

### Критерий завершения
```bash
ruff check src/hw_checker/application/stages/docker_cleanup/commands/ --select=C901
# Не должно быть нарушений complexity
```

---

## WS-04: Декомпозиция docker_cleanup.py — Orchestrator

### Контекст
Продолжение WS-03. Команды созданы, нужен оркестратор.

### Зависимость
WS-03 завершён.

### Шаги
1. Создать `orchestrator.py`:
```python
from .states import CleanupState
from .context import CleanupContext, CleanupResult
from .commands import (
    DiscoverComposeFilesCommand,
    ComposeDownCommand,
    ForceKillCommand,
    NetworkCleanupCommand,
)

class CleanupOrchestrator:
    def __init__(self) -> None:
        self._commands = {
            CleanupState.INITIAL: DiscoverComposeFilesCommand(),
            CleanupState.COMPOSE_DOWN_RUNNING: ComposeDownCommand(),
            CleanupState.FORCE_KILL_PENDING: ForceKillCommand(),
            CleanupState.NETWORK_CLEANUP: NetworkCleanupCommand(),
        }

    def cleanup(self, execution_root: Path, submission_id: str) -> CleanupResult:
        ctx = CleanupContext(execution_root=execution_root, submission_id=submission_id)
        state = CleanupState.INITIAL
        
        while state not in (CleanupState.COMPLETED, CleanupState.FAILED):
            command = self._commands.get(state)
            if command is None:
                state = CleanupState.COMPLETED
                break
            ctx, state = command.execute(ctx)
        
        return CleanupResult(
            success=state == CleanupState.COMPLETED,
            errors=ctx.errors,
        )
```

2. Обновить старый `docker_cleanup.py` как thin wrapper:
```python
from .docker_cleanup.orchestrator import CleanupOrchestrator

def cleanup_docker_compose(execution_root, stage_dir, submission_id, assignment=None):
    """Legacy wrapper for backward compatibility."""
    orchestrator = CleanupOrchestrator()
    result = orchestrator.cleanup(execution_root, submission_id)
    if not result.success:
        # log errors
        pass
```

### Ожидаемый результат
- `orchestrator.py` < 80 строк
- Старый API сохранён через wrapper
- Все тесты проходят

### Критерий завершения
```bash
pytest tests/ -k cleanup -x
ruff check src/hw_checker/application/stages/docker_cleanup/ --select=C901
```

---

## WS-05: Извлечение _setup_environment — Структура

### Контекст
`executor.py:_setup_environment` — 378 строк, CC=49. Нужно извлечь в отдельный модуль.

### Входные файлы
- `src/hw_checker/infrastructure/dind/executor.py`

### Шаги
1. Создать директорию `infrastructure/dind/environment/`
2. Создать `config.py`:
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class EnvironmentConfig:
    nexus_url: str | None
    docker_registry_mirror: str | None
    pip_index_url: str | None
    maven_repo_url: str | None
    timeout_seconds: int = 300
```

3. Создать `protocol.py`:
```python
from typing import Protocol

class SetupStep(Protocol):
    def execute(self, container_id: str, config: EnvironmentConfig) -> bool:
        """Execute setup step. Returns True on success."""
        ...
```

4. Создать `__init__.py`

### Ожидаемый результат
```
infrastructure/dind/environment/
├── __init__.py
├── config.py      # < 30 строк
└── protocol.py    # < 15 строк
```

### Критерий завершения
```bash
python -c "from hw_checker.infrastructure.dind.environment import EnvironmentConfig, SetupStep"
```

---

## WS-06: Извлечение _setup_environment — Steps

### Контекст
Продолжение WS-05. Извлечь конкретные шаги настройки.

### Зависимость
WS-05 завершён.

### Входные файлы
- `executor.py:_setup_environment` — исходная логика

### Шаги
1. Создать `steps/daemon_config.py` — настройка daemon.json
2. Создать `steps/nexus_discovery.py` — обнаружение Nexus
3. Создать `steps/package_managers.py` — настройка pip/apt/maven
4. Создать `steps/verification.py` — проверка Docker daemon

Каждый step:
- < 80 строк
- CC < 10
- Использует `EnvironmentConfig`
- Возвращает bool success

### Пример `steps/daemon_config.py`:
```python
from dataclasses import dataclass
from ..config import EnvironmentConfig

@dataclass
class DaemonConfigStep:
    docker_client: DockerClientPort
    
    def execute(self, container_id: str, config: EnvironmentConfig) -> bool:
        if not config.docker_registry_mirror:
            return True  # No config needed
        
        daemon_json = {
            "registry-mirrors": [config.docker_registry_mirror],
            "insecure-registries": [config.docker_registry_mirror],
        }
        # Write to container...
        return True
```

### Ожидаемый результат
```
infrastructure/dind/environment/steps/
├── __init__.py
├── daemon_config.py     # < 80 строк
├── nexus_discovery.py   # < 60 строк
├── package_managers.py  # < 100 строк
└── verification.py      # < 50 строк
```

### Критерий завершения
```bash
ruff check src/hw_checker/infrastructure/dind/environment/steps/ --select=C901
```

---

## WS-07: Извлечение _setup_environment — Orchestrator

### Контекст
Продолжение WS-06. Создать оркестратор и интегрировать в executor.

### Зависимость
WS-06 завершён.

### Шаги
1. Создать `orchestrator.py`:
```python
from .config import EnvironmentConfig
from .steps import DaemonConfigStep, NexusDiscoveryStep, PackageManagersStep, VerificationStep

class EnvironmentSetupOrchestrator:
    def __init__(self, docker_client: DockerClientPort) -> None:
        self._steps = [
            NexusDiscoveryStep(docker_client),
            DaemonConfigStep(docker_client),
            PackageManagersStep(docker_client),
            VerificationStep(docker_client),
        ]
    
    def setup(self, container_id: str, config: EnvironmentConfig) -> bool:
        for step in self._steps:
            if not step.execute(container_id, config):
                return False
        return True
```

2. Обновить `executor.py`:
```python
def _setup_environment(self, container_id: str, network_name: str) -> None:
    from .environment import EnvironmentSetupOrchestrator, EnvironmentConfig
    
    config = EnvironmentConfig(
        nexus_url=os.environ.get("NEXUS_URL"),
        docker_registry_mirror=os.environ.get("DOCKER_REGISTRY_MIRROR"),
        # ...
    )
    orchestrator = EnvironmentSetupOrchestrator(self._docker_client)
    if not orchestrator.setup(container_id, config):
        raise EnvironmentSetupError("Failed to setup environment")
```

### Ожидаемый результат
- `executor.py` уменьшен на ~300 строк
- Новый код в `environment/` модуле
- Все тесты проходят

### Критерий завершения
```bash
wc -l src/hw_checker/infrastructure/dind/executor.py
# Должно быть < 650 строк
pytest tests/test_dind_executor.py -x
```

---

## WS-08: Inline Scripts → Static Files

### Контекст
`executor.py` генерирует Python-скрипты через f-strings — хрупко и нетестируемо.

### Входные файлы
- `executor.py` — места генерации скриптов через строки

### Шаги
1. Создать `infrastructure/dind/scripts/setup_env.py` — статический скрипт настройки
2. Создать `infrastructure/dind/scripts/verify_docker.py` — проверка Docker
3. Обновить executor чтобы читать скрипты из файлов вместо генерации
4. Добавить скрипты в package data (pyproject.toml)

### Пример `scripts/setup_env.py`:
```python
#!/usr/bin/env python3
"""Environment setup script for DinD container.

This script is executed inside the DinD container.
Configuration passed via environment variables.
"""
import os
import subprocess
import sys

def setup_pip():
    index_url = os.environ.get("PIP_INDEX_URL")
    if not index_url:
        return
    # Configure pip...

def setup_apt():
    # Configure apt mirrors...
    pass

def main():
    setup_pip()
    setup_apt()
    print("✅ Environment setup completed")

if __name__ == "__main__":
    main()
```

### Ожидаемый результат
- Скрипты как отдельные .py файлы
- Можно линтить и тестировать отдельно
- Executor читает из файлов

### Критерий завершения
```bash
ruff check src/hw_checker/infrastructure/dind/scripts/
python src/hw_checker/infrastructure/dind/scripts/setup_env.py --help  # No syntax errors
```

---

## WS-09: Ruff CI Integration

### Контекст
Нет автоматической проверки качества кода в CI.

### Шаги
1. Обновить `pyproject.toml`:
```toml
[tool.ruff]
line-length = 120
target-version = "py310"
select = [
    "E",      # pycodestyle errors
    "F",      # pyflakes
    "W",      # pycodestyle warnings
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "C901",   # mccabe complexity
]

[tool.ruff.mccabe]
max-complexity = 15
```

2. Создать/обновить `.github/workflows/lint.yml` или CI config
3. Запустить локально и исправить критичные ошибки

### Ожидаемый результат
- Ruff настроен в pyproject.toml
- CI проверяет код на каждый PR/push
- Локальная команда `ruff check` работает

### Критерий завершения
```bash
cd tools/hw_checker && ruff check src/hw_checker/ --statistics
# Должен завершиться без фатальных ошибок
```

---

## WS-10: Exception Handling Cleanup

### Контекст
Широкие `except Exception` скрывают ошибки и ломают debugging.

### Входные файлы
- `worker_service.py` — 5 мест
- `grading_router.py` — 4 места

### Шаги
1. Найти все `except Exception`:
```bash
grep -n "except Exception" src/hw_checker/**/*.py
```

2. Для каждого случая:
   - Определить какие исключения реально ожидаются
   - Заменить на специфичные типы
   - Добавить `exc_info=True` в логирование

### Пример замены:
```python
# БЫЛО:
try:
    result = run_grading()
except Exception as e:
    logger.error(f"Grading failed: {e}")
    return None

# СТАЛО:
try:
    result = run_grading()
except (DockerError, TimeoutError) as e:
    logger.error("Grading failed", exc_info=True, extra={"error_type": type(e).__name__})
    raise GradingError(f"Grading failed: {e}") from e
```

### Ожидаемый результат
- Нет `except Exception` без `exc_info=True`
- Специфичные типы исключений где возможно
- Ошибки не теряются

### Критерий завершения
```bash
grep -c "except Exception:" src/hw_checker/**/*.py
# Должно вернуть 0 или минимум с обоснованием
```

---

## WS-11: run_homework.py — Stage Extraction Review

### Контекст
`run_homework.py` (1260 строк) уже имеет начатую декомпозицию в `run_homework/`. Нужно проверить и завершить.

### Входные файлы
- `application/run_homework.py` — текущий монолит
- `application/run_homework/` — начатая декомпозиция

### Шаги
1. Проанализировать что уже извлечено в `run_homework/`
2. Идентифицировать оставшуюся логику в монолите
3. Завершить миграцию stages
4. Обновить `run_homework.py` как thin re-export wrapper

### Ожидаемый результат
- `run_homework.py` < 100 строк (только re-exports)
- Вся логика в `run_homework/` submodule
- Публичный API не изменён

### Критерий завершения
```bash
wc -l src/hw_checker/application/run_homework.py
# Должно быть < 150 строк
pytest tests/ -k run_homework -x
```

---

## WS-12: sampling_validators.py — Protocol & Registry

### Контекст
`sampling_validators.py` (986 строк) содержит логику для HW2/HW3/HW4. Нужно разделить.

### Шаги
1. Создать `validators/protocol.py`:
```python
from typing import Protocol
from ..domain.models import SamplingResult

class ValidatorProtocol(Protocol):
    assignment: str
    
    def validate(self, container_id: str, submission_path: Path) -> SamplingResult:
        ...
```

2. Создать `validators/registry.py`:
```python
class ValidatorRegistry:
    _validators: dict[str, ValidatorProtocol] = {}
    
    @classmethod
    def register(cls, validator: ValidatorProtocol) -> None:
        cls._validators[validator.assignment] = validator
    
    @classmethod
    def get(cls, assignment: str) -> ValidatorProtocol | None:
        return cls._validators.get(assignment)
```

### Ожидаемый результат
```
application/validators/
├── __init__.py
├── protocol.py    # < 30 строк
└── registry.py    # < 40 строк
```

### Критерий завершения
```bash
python -c "from hw_checker.application.validators import ValidatorProtocol, ValidatorRegistry"
```

---

## WS-13: sampling_validators.py — HW Validators Split

### Контекст
Продолжение WS-12. Извлечь конкретные валидаторы.

### Зависимость
WS-12 завершён.

### Шаги
1. Создать `validators/hw2_airflow.py` — Airflow-специфичная валидация
2. Создать `validators/hw3_mlflow.py` — MLflow-специфичная валидация
3. Создать `validators/hw4_pipeline.py` — Pipeline-специфичная валидация
4. Зарегистрировать в registry
5. Обновить `sampling_validators.py` как facade

### Ожидаемый результат
- Каждый валидатор < 300 строк
- CC < 15 для каждой функции
- Старый API сохранён через facade

### Критерий завершения
```bash
wc -l src/hw_checker/application/validators/hw*.py
# Каждый < 300 строк
pytest tests/ -k sampling -x
```

---

## WS-14: publisher.py — Strategy Pattern

### Контекст
`publisher.py` (920 строк) содержит логику для Sheets/Drive/Local publishing.

### Шаги
1. Создать `publishers/protocol.py`:
```python
from typing import Protocol

class PublisherProtocol(Protocol):
    def publish(self, results: GradingResults) -> bool:
        ...
```

2. Создать `publishers/sheets.py` — Google Sheets publishing
3. Создать `publishers/drive.py` — Google Drive publishing  
4. Создать `publishers/local.py` — Local file publishing
5. Создать `publishers/composite.py` — Композитный publisher

### Ожидаемый результат
- Каждый publisher < 200 строк
- Чистый Protocol для DI
- Старый API сохранён

### Критерий завершения
```bash
wc -l src/hw_checker/infrastructure/publishers/*.py
# Каждый < 250 строк
```

---

## WS-15: Domain Layer Cleanup

### Контекст
`domain/dind.py` использует `os.environ` — нарушение Clean Architecture.

### Входные файлы
- `src/hw_checker/domain/dind.py`

### Шаги
1. Найти все `os.environ` в domain layer:
```bash
grep -r "os.environ" src/hw_checker/domain/
```

2. Заменить на инжекцию через конструктор:
```python
# БЫЛО:
@dataclass
class DinDResourceLimits:
    @classmethod
    def from_env(cls) -> DinDResourceLimits:
        return cls(
            cpu_limit=int(os.environ.get("HW_CHECKER_DIND_CPU_LIMIT", 2)),
            # ...
        )

# СТАЛО:
@dataclass(frozen=True)
class DinDResourceLimits:
    cpu_limit: int = 2
    memory_limit_mb: int = 4096
    # No from_env — inject from infrastructure
```

3. Обновить места использования чтобы инжектировать конфигурацию

### Ожидаемый результат
- Нет `os.environ` в domain layer
- Domain — pure value objects
- Конфигурация инжектируется из infrastructure

### Критерий завершения
```bash
grep -c "os.environ" src/hw_checker/domain/*.py
# Должно вернуть 0
```

---

## Зависимости между Workstreams

```
WS-01 (dedup) ← независимый, выполнить первым

WS-02 → WS-03 → WS-04 (docker_cleanup chain)

WS-05 → WS-06 → WS-07 → WS-08 (environment setup chain)

WS-09 (Ruff) ← независимый

WS-10 (exceptions) ← независимый

WS-11 (run_homework) ← после WS-04

WS-12 → WS-13 (validators chain)

WS-14 (publishers) ← независимый

WS-15 (domain cleanup) ← независимый
```

---

## Приоритет выполнения

### Tier 1 (критично для AI-readiness)
- WS-01: Удаление дубликата
- WS-02, WS-03, WS-04: docker_cleanup chain
- WS-09: Ruff

### Tier 2 (улучшение maintainability)
- WS-05, WS-06, WS-07, WS-08: environment setup chain
- WS-10: Exception handling

### Tier 3 (архитектурная чистота)
- WS-11: run_homework completion
- WS-12, WS-13: validators
- WS-14: publishers
- WS-15: domain cleanup

