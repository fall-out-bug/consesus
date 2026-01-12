# /build — Execute Workstream

При вызове `/build {WS-ID}`:

1. Загрузи полный промпт: `@sdp/prompts/commands/build.md`
2. Запусти pre-build hook: `sdp/hooks/pre-build.sh {WS-ID}`
3. Прочитай WS план
4. Выполни шаги по TDD
5. Запусти post-build hook: `sdp/hooks/post-build.sh {WS-ID}`
6. Append Execution Report в WS файл

## Quick Reference

**Input:** `workstreams/backlog/WS-XXX-*.md`
**Output:** код + тесты + Execution Report
**Next:** `/build WS-XXX-02` или `/review F{XX}`
