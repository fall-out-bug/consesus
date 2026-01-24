---
description: Analyze + Plan - creates workstreams from feature draft
agent: planner
---

# /design — Analyze + Plan

При вызове `/design {slug}`:

1. Загрузи полный промпт: `@sdp/prompts/commands/design.md`
2. Прочитай PROJECT_MAP.md и INDEX.md
3. Прочитай draft: `tools/hw_checker/docs/drafts/idea-{slug}.md`
4. Создай все WS файлы в `workstreams/backlog/`
5. Обнови INDEX.md
6. Синхронизируй с GitHub (см. Step 7)
7. Выведи summary

## Quick Reference

**Input:** `tools/hw_checker/docs/drafts/idea-{slug}.md`
**Output:** `tools/hw_checker/docs/workstreams/backlog/WS-XXX-*.md`
**Next:** `/build WS-XXX-01`

## Step 7: Sync to GitHub

After creating all WS files, sync to GitHub:

```bash
# Set environment (if not set)
export GITHUB_TOKEN="${GITHUB_TOKEN:-}"
export GITHUB_REPO="${GITHUB_REPO:-fall-out-bug/msu_ai_masters}"

# Sync all created WS files
cd sdp
poetry run sdp-github sync-all --ws-dir ../tools/hw_checker/docs/workstreams

# Or sync a single WS file (explicit path)
poetry run sdp-github sync-ws \
  ../tools/hw_checker/docs/workstreams/backlog/WS-{XX}-01-your-title.md
```

**If GITHUB_TOKEN not set:**
- Skip sync with warning
- WS files still created locally
- Sync will happen on git push via GitHub Actions

**Expected output:**
```
Syncing backlog...
  WS-{XX}-01: created (#123)
  WS-{XX}-02: created (#124)
Syncing active...
Done!
```
