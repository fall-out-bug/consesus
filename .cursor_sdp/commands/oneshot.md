# /oneshot — Autonomous Feature Execution

При вызове `/oneshot F{XX}`:

1. Загрузи полный промпт: `@sdp/prompts/commands/oneshot.md`
2. Создай PR и дождись approval
3. Выполни все WS feature автономно
4. Сохраняй checkpoints
5. Обрабатывай ошибки (auto-fix или escalate)
6. Запусти `/review` в конце
7. Выведи summary

## Quick Reference

**Input:** Feature ID (F60)
**Output:** All WS executed + Review + UAT guide
**Features:**
- PR approval gate
- Checkpoint/resume support
- Progress tracking JSON
- Auto-fix MEDIUM/HIGH errors
- Telegram notifications

**Next:** Human UAT → `/deploy F{XX}`

## Checkpoint Files

- `.oneshot/F{XX}-checkpoint.json` - Resume state
- `.oneshot/F{XX}-progress.json` - Real-time metrics
