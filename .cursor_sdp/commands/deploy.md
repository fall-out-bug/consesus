# /deploy — Deploy Feature

При вызове `/deploy {feature}`:

1. Загрузи полный промпт: `@sdp/prompts/commands/deploy.md`
2. Проверь что все WS APPROVED
3. Выполни Mandatory Dialogue (scope, environments)
4. Сгенерируй:
   - docker-compose updates
   - CI/CD pipeline updates
   - CHANGELOG.md entry
   - Release notes
   - Deployment plan

## Quick Reference

**Input:** APPROVED feature
**Output:** DevOps configs + docs + release notes
**Next:** Execute deployment plan
