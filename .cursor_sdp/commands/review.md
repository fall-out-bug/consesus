# /review — Review Feature

При вызове `/review {feature}`:

1. Загрузи полный промпт: `@sdp/prompts/commands/review.md`
2. Найди все WS фичи в INDEX.md
3. Проверь каждый WS по чеклисту (Check 0-11)
4. Выполни cross-WS проверки
5. Append Review Results в каждый WS файл
6. Выведи Feature Summary

## Quick Reference

**Input:** все WS фичи
**Output:** Review Results в каждом WS + Feature Summary
**Verdict:** APPROVED или CHANGES REQUESTED
**Next:** `/deploy F{XX}` (если APPROVED)
