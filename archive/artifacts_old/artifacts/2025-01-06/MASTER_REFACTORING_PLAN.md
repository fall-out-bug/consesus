# Master Refactoring Plan: hw_checker

**Дата:** 2026-01-06  
**Контекст:** Приватный репозиторий single-developer  
**Формат работы:** Workstreams для субагентов (см. `WORKSTREAMS.md`)

---

## Консолидированная оценка

| Метрика | Оценка | Комментарий |
|---------|--------|-------------|
| **Overall Quality** | 6/10 | Solid foundation, technical debt в modularity |
| **AI-Readiness** | 4.5/10 | Файлы >200 строк, CC>30 — Haiku hallucinations |
| **Security** | VULNERABLE | Приемлемо для private single-dev |
| **Production Ready** | NO | После Tier 1 workstreams |

---

## Приоритеты

### Tier 1: AI-Readiness (блокер)
Код должен быть редактируемым AI-агентами без потери контекста.

| Проблема | Файл | Строки | CC | Workstream |
|----------|------|--------|-----|------------|
| Дубликат кода | `hw_checker/infrastructure/dind/executor.py` | 1193 | — | WS-01 |
| God function | `docker_cleanup.py` | 569 | 81 | WS-02,03,04 |
| God function | `executor.py:_setup_environment` | 378 | 49 | WS-05,06,07,08 |
| No linting | — | — | — | WS-09 |
| Silent errors | Multiple | — | — | WS-10 |

### Tier 2: Maintainability
Структурные улучшения после Tier 1.

| Проблема | Файл | Строки | Workstream |
|----------|------|--------|------------|
| Monolith | `run_homework.py` | 1260 | WS-11 |
| Monolith | `sampling_validators.py` | 986 | WS-12,13 |
| Monolith | `publisher.py` | 920 | WS-14 |

### Tier 3: Architecture
Clean Architecture compliance.

| Проблема | Файл | Workstream |
|----------|------|------------|
| Domain uses os.environ | `domain/dind.py` | WS-15 |

### Tier 4: Security (отложено)
При K8s миграции или добавлении пользователей.

- Docker socket mount removal
- DinD hardening (no privileged)
- Git history cleanup
- Network isolation

---

## Workstreams Summary

```
Tier 1 (критично):
├── WS-01: Удаление дубликата executor
├── WS-02: docker_cleanup — states & context
├── WS-03: docker_cleanup — commands
├── WS-04: docker_cleanup — orchestrator
└── WS-09: Ruff CI

Tier 2 (maintainability):
├── WS-05: environment setup — structure
├── WS-06: environment setup — steps
├── WS-07: environment setup — orchestrator
├── WS-08: inline scripts → static files
├── WS-10: exception handling
├── WS-11: run_homework completion
├── WS-12: validators — protocol
├── WS-13: validators — HW split
└── WS-14: publishers — strategy

Tier 3 (architecture):
└── WS-15: domain cleanup
```

---

## Зависимости

```
WS-01 ← независимый (НАЧАТЬ ЗДЕСЬ)

WS-02 → WS-03 → WS-04 (chain)
WS-05 → WS-06 → WS-07 → WS-08 (chain)
WS-12 → WS-13 (chain)

WS-09, WS-10, WS-11, WS-14, WS-15 ← независимые
```

---

## Критерии успеха

### После Tier 1
- [ ] Нет файлов > 600 строк в application/infrastructure
- [ ] CC < 20 для всех функций
- [ ] Ruff check проходит
- [ ] AI-Readiness ≥ 6/10

### После Tier 2
- [ ] Все файлы < 400 строк
- [ ] CC < 15 для всех функций
- [ ] Тесты проходят
- [ ] AI-Readiness ≥ 7/10

### После Tier 3
- [ ] Нет os.environ в domain layer
- [ ] Clean Architecture compliance
- [ ] AI-Readiness ≥ 8/10

---

## Источники

- `CODE_AUDIT_2026-01-06.md` — детальный аудит кода
- `STRATEGIC_CODE_REVIEW_2026-01-06.md` — security findings (для Tier 4)
- `strategic_audit_2026.md` — architecture analysis
- `WORKSTREAMS.md` — детальные спецификации WS

---

*Консолидированный план для hw_checker refactoring*
