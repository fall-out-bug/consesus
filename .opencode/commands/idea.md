---
description: Requirements gathering - creates feature draft from user description
agent: planner
---

# /idea — Requirements Gathering

При вызове `/idea {description}`:

1. Загрузи полный промпт: `@.claude/skills/idea.md`
2. Выполни Mandatory Initial Dialogue
3. Создай draft в `tools/hw_checker/docs/drafts/idea-{slug}.md`
4. Выведи summary для пользователя

## Quick Reference

**Input:** описание фичи от пользователя
**Output:** `tools/hw_checker/docs/drafts/idea-{slug}.md`
**Next:** `/design idea-{slug}`
