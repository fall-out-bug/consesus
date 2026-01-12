# Phase 4: Review

## Mission

Review the completed Workstream for quality, safety, and standards compliance.

## Input

- Execution Report from Phase 3
- Changed files
- **Goal + Acceptance Criteria from WS plan**
- Completion criteria from plan

## Output

Review is recorded **directly in the WS file** (append to end):

```markdown
### Review Results

#### 2026-01-06 | reviewer_name
**Verdict:** APPROVED / CHANGES REQUESTED

**Goal Achieved:** ✅ / ❌
**Completion Criteria:** ✅ / ❌
**AI-Readiness:** ✅ / ❌
**Clean Architecture:** ✅ / ❌
**Tests & Coverage:** ✅ (XX%) / ❌
**Regression:** ✅ (XX/XX fast tests) / ❌
**No Tech Debt:** ✅ / ❌
**100% Complete:** ✅ / ❌

**If CHANGES REQUESTED — issue list:**
- [CRITICAL/HIGH/MEDIUM/LOW] Description → how to fix
```

**DO NOT create a separate file for review.**
**No "Notes" section — everything is either ✅ or gets fixed.**

---

## Review Checklist

### 0. Goal Achievement (BLOCKING)

**FIRST check — is the Goal achieved?**

```bash
# Run commands from Acceptance Criteria (if there are bash commands)
# Manually verify each AC

# Example AC:
# - [ ] API endpoint /api/runs/{id} returns run status
#   → curl http://localhost:8000/api/runs/test-id
#   → Should return 200 + JSON with fields

# - [ ] Coverage ≥ 80%
#   → pytest --cov (already checked in Execute)
```

**Check each Acceptance Criterion:**
- [ ] AC1 ✅ (works as expected)
- [ ] AC2 ✅
- [ ] AC3 ✅

**If AT LEAST ONE AC ❌ → CHANGES REQUESTED (CRITICAL)**

**Forbidden excuses:**
- "Code written but doesn't work — closing"
- "Main part works"
- "Almost ready"

**Rule:** If Goal not achieved → WS NOT complete.

---

### 1. Completion Criteria

```bash
# Execute ALL commands from plan
# All must pass
```

### 2. AI-Readiness

| Check | Command |
|-------|---------|
| Files < 200 lines | `wc -l {files}` |
| Complexity < 10 | `ruff check --select=C901` |
| Type hints (strict) | `mypy src/module/ --strict --no-implicit-optional` |
| No deep nesting | Max 3 levels |

### 3. Clean Architecture

```bash
# Domain doesn't import other layers
grep -r "from application" domain/
grep -r "from infrastructure" domain/
# Should be empty
```

```bash
# Application doesn't import infrastructure directly
grep -r "from infrastructure" application/
# Should be empty (or only port imports)
```

### 4. Error Handling

```bash
# No bare except
grep -rn "except:" src/ --include="*.py"
grep -rn "except Exception:" src/ --include="*.py" | grep -v "exc_info"
# Should be empty or justified
```

### 5. Tests & Coverage

```bash
# Run tests
pytest tests/unit/test_XXX.py -v

# Coverage ≥ 80%
pytest tests/unit/test_XXX.py -v \
  --cov=src/module \
  --cov-report=term-missing \
  --cov-fail-under=80
```

### 6. Regression

```bash
# All fast tests pass
pytest tests/unit/ -m fast -v

# Zero failures expected
```

### 7. No Tech Debt

```bash
# No TODO/FIXME
grep -rn "TODO\|FIXME" src/ --include="*.py" | grep -v "# NOTE"
# Should be empty
```

### 8. 100% Completion

- [ ] ALL steps from plan executed
- [ ] ALL Acceptance Criteria ✅
- [ ] NO partial completion ("main work done")
- [ ] NO deferred tasks

---

## Severity Levels

| Level | Description | Example |
|-------|-------------|---------|
| **CRITICAL** | Goal not achieved, blocking issue | AC not met, tests fail |
| **HIGH** | Quality gates violated | Coverage < 80%, TODO in code |
| **MEDIUM** | Standards violation | Missing type hints, CC > 10 |
| **LOW** | Style issue | Naming, formatting |

---

## Verdict Rules

### APPROVED

All checks pass:
- Goal achieved (all AC ✅)
- Completion criteria ✅
- AI-Readiness ✅
- Clean Architecture ✅
- Tests & Coverage ✅ (≥80%)
- Regression ✅
- No Tech Debt ✅
- 100% Complete ✅

### CHANGES REQUESTED

At least one issue found:
- Provide specific issue description
- Provide how to fix
- Assign severity level

---

## Review Report Format

```markdown
### Review Results

#### 2026-01-06 | claude

**Verdict:** APPROVED

**Goal Achieved:** ✅
**Completion Criteria:** ✅
**AI-Readiness:** ✅
**Clean Architecture:** ✅
**Tests & Coverage:** ✅ (87%)
**Regression:** ✅ (42/42 fast tests)
**No Tech Debt:** ✅
**100% Complete:** ✅

WS-{ID} ready for merge.
```

Or if issues found:

```markdown
### Review Results

#### 2026-01-06 | claude

**Verdict:** CHANGES REQUESTED

**Goal Achieved:** ❌
**Completion Criteria:** ✅
**AI-Readiness:** ✅
**Clean Architecture:** ❌
**Tests & Coverage:** ✅ (82%)
**Regression:** ✅ (42/42 fast tests)
**No Tech Debt:** ✅
**100% Complete:** ❌

**Issues:**
- [CRITICAL] Goal not achieved: API endpoint returns 500 instead of expected data
  → Debug `service.py:45`, check database connection
- [HIGH] Clean Architecture violation: `application/service.py` imports `infrastructure/db.py` directly
  → Use port injection, see CODE_PATTERNS.md Repository pattern
```

---

## After Review

### If APPROVED

1. Mark WS as `completed` in INDEX.md
2. Move WS file to `workstreams/completed/`
3. Ready for next WS

### If CHANGES REQUESTED

1. Return to Phase 3
2. Fix issues listed
3. Re-run Phase 4

---

## Human UAT (After All WS Approved)

After all feature WS are APPROVED, generate UAT Guide:

```markdown
# UAT Guide: F{XX}

## Quick Smoke Test (30 sec)
1. [Basic operation check]
2. [Verify no errors in logs]

## Detailed Scenarios (5-10 min)
1. Happy Path: [steps]
2. Error Case: [steps]
3. Edge Case: [steps]

## Red Flags Check (2 min)
- [ ] No unhandled exceptions in logs
- [ ] No performance degradation
- [ ] No security warnings

## Sign-off
- [ ] Tested by: ___
- [ ] Date: ___
- [ ] Approved: Yes / No
```

**Without human Sign-off → Deploy blocked.**
