---
description: Deploy feature - generates DevOps configs, CI/CD, release notes, creates PR
agent: deployer
---

# /deploy — Deploy Feature

При вызове `/deploy {feature}`:

1. Загрузи полный промпт: `@sdp/prompts/commands/deploy.md`
2. Проверь что все WS APPROVED
3. Выполни Mandatory Dialogue (scope, environments)
4. Проверь GitHub sync (см. Pre-deploy Check)
5. Сгенерируй:
   - docker-compose updates
   - CI/CD pipeline updates
   - CHANGELOG.md entry
   - Release notes
   - Deployment plan

## Quick Reference

**Input:** APPROVED feature
**Output:** DevOps configs + docs + release notes
**Next:** Execute deployment plan

## Pre-deploy Check: GitHub Sync

Before creating PR, verify all WS are synced:

```bash
# Check all feature WS have github_issue set
grep -l "^github_issue: null" \
  tools/hw_checker/docs/workstreams/*/WS-{feature_num}*.md

# If any found, sync them first
cd sdp
poetry run sdp-github sync-all --ws-dir ../tools/hw_checker/docs/workstreams
```
