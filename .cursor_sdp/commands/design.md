# /design — Analyze + Plan

При вызове `/design {slug}`:

1. Загрузи полный промпт: `@sdp/prompts/commands/design.md`
2. Прочитай PROJECT_MAP.md и INDEX.md
3. Прочитай draft: `docs/drafts/idea-{slug}.md`
4. Создай все WS файлы в `workstreams/backlog/`
5. Обнови INDEX.md
6. Выведи summary

## Quick Reference

**Input:** `docs/drafts/idea-{slug}.md`
**Output:** `docs/workstreams/backlog/WS-XXX-*.md`
**Next:** `/build WS-XXX-01`
