# Changelog

Все заметные изменения SDP задокументированы в этом файле.

## [0.4.0] - 2026-01-27

### Добавлено

#### F011: PRD Command
- Команда `/prd` для управления PRD
- Авто-генерация architecture diagrams из аннотаций в коде
- Парсер `@prd:` аннотаций для обновления документации
- Валидатор длины строк для документов
- Генератор диаграмм (формат Mermaid)
- Поддержка профилей для разных форматов проектов

#### F003: Two-Stage Code Review
- Stage 1: Проверка соответствия spec (цели, покрытие AC)
- Stage 2: Качество кода (покрытие, типизация, AI-readiness)
- Stage 2 запускается только если прошёл Stage 1 — не полируем неправильное
- Обновлён skill `/codereview`

#### F004: Platform Adapters
- Интерфейс `PlatformAdapter` для унифицированного API
- `detect_platform()` для автоопределения IDE
- Адаптер Claude Code (`.claude/`)
- Адаптер Cursor (`.codex/`)
- Адаптер OpenCode (`.opencode/`)

#### F005: Extension System
- Поддержка `sdp.local/` и `~/.sdp/extensions/{name}/`
- Формат манифеста `extension.yaml`
- Автообнаружение и загрузка расширений
- Компоненты: hooks, patterns, skills, integrations

#### F007: Oneshot & Hooks
- Команда `/oneshot` для автономного выполнения feature
- Git hooks: pre-commit, post-commit, pre-push
- Quality gates
- Интеграция с Cursor agents
- Команды `/debug` и `/test`
- Skills `/idea` и `/design`

#### F008: Contract-Driven WS Tiers
- Уровни: Starter, Standard, Advanced
- Валидатор capability tiers
- Реестр моделей
- Авто-повышение tier
- Метрики эскалации

#### F010: SDP Infrastructure
- Поддержка submodule
- Соглашение именования PP-FFF-SS
- Синхронизация контента

### Изменено

- Обновлён формат именования workstreams на PP-FFF-SS
- Улучшена структура документации
- Обновлены определения skills

### Статистика

- **Всего workstreams:** 58
- **Завершено:** 48 (83%)
- **Features:** 8 (F003, F004, F005, F006, F007, F008, F010, F011)

## [0.3.0] - Предыдущий релиз

- Начальная реализация протокола SDP
- Базовый workstream framework
- Базовые CLI команды
- Настройка quality gates

---

**Формат:** На основе [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
