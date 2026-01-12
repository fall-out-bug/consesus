# Spec Driven Protocol (SDP)

Протокол разработки на основе воркстримов для AI-агентов с one-shot выполнением.

[English version](README.md)

---

## Основная идея

**Workstream** = атомарная задача, которую AI выполняет за один проход, без итеративных циклов.

```
Feature → Workstreams → One-shot выполнение → Готово
```

## Терминология

| Термин | Scope | Размер | Пример |
|--------|-------|--------|--------|
| **Release** | Продуктовая веха | 10-30 Features | R1: MVP |
| **Feature** | Крупная фича | 5-30 Workstreams | F1: User Auth |
| **Workstream** | Атомарная задача | SMALL/MEDIUM/LARGE | WS-001: Domain entities |

**Метрики scope:**
- **SMALL**: < 500 LOC, < 1500 токенов
- **MEDIUM**: 500-1500 LOC, 1500-5000 токенов
- **LARGE**: > 1500 LOC → **разбить на 2+ WS**

**НЕ используем временные оценки.** Только LOC/токены.

## Workflow

```
┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐
│  ANALYZE   │───→│    PLAN    │───→│  EXECUTE   │───→│   REVIEW   │
│  (Фаза 1)  │    │  (Фаза 2)  │    │  (Фаза 3)  │    │  (Фаза 4)  │
└────────────┘    └────────────┘    └────────────┘    └────────────┘
```


## Быстрый старт

### 1. Создать спецификацию Feature

```markdown
# Feature: User Authentication

## Overview
Пользователи могут регистрироваться и логиниться по email/паролю.

## Workstreams
- WS-001: Domain entities (User, Password, Session)
- WS-002: Repository pattern
- WS-003: Auth service
- WS-004: API endpoints
- WS-005: Tests
```

### 2. Фаза 1: Analyze

```
Проверить WS-001:
- Критерии приёмки выполнены?
- Код соответствует паттернам?
- Тесты адекватны?
```

### 6. Повторить

Повторить фазы 2-4 для оставшихся workstreams.

## Quality Gates

| Gate | Требования |
|------|------------|
| **AI-Readiness** | Файлы < 200 LOC, CC < 10, type hints |
| **Clean Architecture** | Нет нарушений слоёв |
| **Error Handling** | Нет `except: pass` |
| **Test Coverage** | ≥ 80% |
| **No TODOs** | Все выполнены или новый WS |

## Базовые принципы

| Принцип | Суть |
|---------|------|
| **SOLID** | SRP, OCP, LSP, ISP, DIP |
| **DRY** | Don't Repeat Yourself |
| **KISS** | Keep It Simple |
| **YAGNI** | Строй только нужное |
| **TDD** | Сначала тесты (Red → Green → Refactor) |
| **Clean Code** | Читаемый, поддерживаемый |
| **Clean Architecture** | Зависимости направлены внутрь |

Подробнее: [docs/PRINCIPLES.md](docs/PRINCIPLES.md)

## Структура файлов

```
sdp/
├── PROTOCOL.md              # Полная спецификация
├── CODE_PATTERNS.md         # Паттерны реализации
├── RULES_COMMON.md          # Общие правила
├── docs/
│   ├── PRINCIPLES.md        # SOLID, DRY, KISS, YAGNI
│   └── concepts/            # Clean Architecture, Artifacts, Roles
├── prompts/
│   ├── structured/          # Промпты фаз 1-4
│   └── commands/            # Slash-команды
├── schema/                  # JSON валидация
├── scripts/                 # Утилиты
└── templates/               # Шаблоны документов
```

## Ресурсы

| Ресурс | Назначение |
|--------|------------|
| [PROTOCOL.md](PROTOCOL.md) | Полная спецификация |
| [docs/PRINCIPLES.md](docs/PRINCIPLES.md) | SOLID, DRY, KISS, YAGNI |
| [docs/concepts/](docs/concepts/) | Архитектурные концепции |
| [CODE_PATTERNS.md](CODE_PATTERNS.md) | Паттерны кода |
| [CLAUDE.md](CLAUDE.md) | Интеграция с Claude Code |

## Интеграция

```bash
# Скопировать в свой проект
cp -r prompts/ your-project/
cp -r schema/ your-project/
cp CLAUDE.md your-project/
```

---

**Версия:** 0.3.0 | **Статус:** Активен
