---
ws_id: PP-FFF-SS
feature: FFFF
status: backlog|active|completed|blocked
size: SMALL|MEDIUM|LARGE
project_id: PP
github_issue: null
assignee: null
depends_on:
  - PP-FFF-SS  # Optional: list of dependent WS IDs
---

## WS-PP-FFF-SS: Title

### 🎯 Цель (Goal)

**Что должно РАБОТАТЬ после завершения WS:**
- [First specific outcome]
- [Second specific outcome]

**Acceptance Criteria:**
- [ ] AC1: [First criterion - specific, measurable]
- [ ] AC2: [Second criterion - specific, measurable]
- [ ] AC3: [Third criterion - specific, measurable]

**⚠️ WS НЕ завершён, пока Goal не достигнута (все AC ✅).**

---

### Контекст

[Background information about the workstream]

### Зависимость

[List dependencies or write "Независимый" for no dependencies]

### Входные файлы

[List input files or sections to read]

### Шаги

1. **[Step 1 title]**

   [Detailed instructions for step 1]

2. **[Step 2 title]**

   [Detailed instructions for step 2]

### Ожидаемый результат

[Description of expected outcome]

### Scope Estimate

- Файлов: ~[number]
- Строк: ~[number] ([SMALL|MEDIUM|LARGE])
- Токенов: ~[number]

### Критерий завершения

```bash
# Verification commands
test -f path/to/file
grep "expected content" path/to/file
echo "✅ Verification passed"
```

### Ограничения

- НЕ [constraint 1]
- НЕ [constraint 2]

---

## Execution Report

**Executed by:** [Name/Agent]
**Date:** YYYY-MM-DD

### Goal Status
- [x] AC1: [description] — ✅
- [x] AC2: [description] — ✅
- [x] AC3: [description] — ✅

**Goal Achieved:** ✅ YES

### Files Changed
| File | Action | LOC |
|------|--------|-----|
| `path/to/file.py` | created | 120 |
| `path/to/test.py` | created | 80 |

### Self-Check Results
```bash
$ pytest tests/unit/test_module.py -v
===== 15 passed in 0.5s =====

$ pytest --cov=module --cov-fail-under=80
===== Coverage: 85% =====
```

### Commit
{commit_hash} - {commit_message}
