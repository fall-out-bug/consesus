---
description: Execute workstream with TDD - implements code, tests, and execution report
agent: builder
---

# /build — Execute Workstream

При вызове `/build {WS-ID}`:

1. Загрузи полный промпт: `@sdp/prompts/commands/build.md`
2. Запусти pre-build hook: `sdp/hooks/pre-build.sh {WS-ID}`
3. Прочитай WS план
4. Выполни шаги по TDD
5. Запусти post-build hook: `sdp/hooks/post-build.sh {WS-ID}`
6. Append Execution Report в WS файл
7. Обнови статус в GitHub (см. Step 8)

## Quick Reference

**Input:** `workstreams/backlog/WS-XXX-*.md`
**Output:** код + тесты + Execution Report
**Next:** `/build WS-XXX-02` или `/codereview F{XX}`

## Step 8: Update GitHub Status

After completing WS implementation:

```bash
# Update WS file status to "completed"
# (Already done in Step 7 - Execution Report)

# Sync status change to GitHub
cd sdp
poetry run sdp-github sync-ws ../tools/hw_checker/docs/workstreams/active/WS-{ID}.md
```

This will:
- Update GitHub issue labels (status/completed)
- Close the GitHub issue
- Move project board card to "Done" column
