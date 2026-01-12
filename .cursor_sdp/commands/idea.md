# /idea — Requirements Gathering

При вызове `/idea {description}`:

1. Загрузи полный промпт: `@sdp/prompts/commands/idea.md`
2. Выполни Mandatory Initial Dialogue
3. Создай draft в `docs/drafts/idea-{slug}.md`
4. Выведи summary для пользователя

## Quick Reference

**Input:** описание фичи от пользователя
**Output:** `docs/drafts/idea-{slug}.md`
**Next:** `/design idea-{slug}`
