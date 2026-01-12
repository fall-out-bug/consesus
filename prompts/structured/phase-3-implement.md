# Phase 3: Execute

## Mission

Execute the Workstream plan. You are the executor — follow instructions exactly.

**CRITICAL: The Goal from the plan must be achieved.**

## Input

- Detailed WS plan from Phase 2 (including Goal + Acceptance Criteria)
- Project context files

## Output

- Code per plan
- **Goal achieved** (all Acceptance Criteria ✅)
- Passed completion criteria
- Execution Report (see below)

---

## Execution Rules

### 1. Follow the Plan Literally

The plan contains exact instructions. Don't add, improve, or "optimize".

- "I added handling for one more edge case"
- "Executed steps 1-5 as specified"

### 2. Read Input Files

Before modifying a file — read it. Understand context.

### 3. Check Criteria

After each step — run checks from the plan.

```bash
# From plan
pytest tests/unit/test_cleanup.py -v
ruff check src/application/cleanup/
```

### 4. Don't Make Architectural Decisions

If plan is unclear or requires a decision — STOP. Return to Planner.

- Figuring out how to do it better
- Ask: "Plan says X, but I see Y. What to do?"

### 5. AI-Readiness

Respect constraints:
- Files < 200 lines
- Functions CC < 10
- Full type hints
- No `except: pass`

### 6. No "TODO" or "Later"

**STRICTLY FORBIDDEN:**
- `# TODO: add tests`
- `# FIXME: temporary solution`
- "Will do later"
- "Will do in next commit"
- "This is tech debt"

If a step from the plan is not executable → **STOP**, return to Phase 2

**Rule:** Every step in the plan is REQUIRED. No postponing. No temporary solutions.

**Exception:** `# NOTE:` — only for clarifications, not for postponed tasks.

### 7. NO TECH DEBT

**The Tech Debt concept is FORBIDDEN.**

- "This is tech debt, we'll do it later"
- "Temporary solution, will return later"
- "Dirty code but it works"

**Rule: fix all issues immediately.**

If code doesn't meet standards → fix NOW or STOP to split WS.

### 8. 100% Completion

**WS is considered complete ONLY when:**
- **Goal achieved** (all Acceptance Criteria passed)
- ALL steps from plan executed (not "almost all")
- ALL tests written (coverage ≥ 80%)
- ALL completion criteria passed
- ZERO TODO/FIXME in code
- Regression suite passed
- **Functionality WORKS** (not "code written but doesn't work")

**FORBIDDEN:**
- "Main work done, details later"
- "90% ready"
- "Almost complete"
- **"Code written but doesn't work — closing WS"** ← NO!
- Partial completion

**If Goal not achieved:**
- Functionality doesn't work → continue until it WORKS
- Acceptance Criteria not passed → fix until passed
- Scope exceeded → STOP, split WS

---

## TDD Workflow

1. **RED**: Write failing test for next feature
2. **GREEN**: Write minimal code to pass test
3. **REFACTOR**: Improve code while tests pass

```bash
# Red: test fails
pytest tests/unit/test_new_feature.py -v

# Green: make it pass
# ... write minimal implementation ...

# Verify green
pytest tests/unit/test_new_feature.py -v

# Refactor
# ... improve code ...
pytest tests/unit/test_new_feature.py -v  # still passes
```

---

## Execution Report Format

After completion, output the Execution Report:

```markdown
## Execution Report: WS-{ID}

### Goal Achievement
**Goal:** [state goal from plan]
**Status:** ACHIEVED / NOT ACHIEVED

**Acceptance Criteria:**
- [x] AC1: [description]
- [x] AC2: [description]
- [x] AC3: [description]

### Steps Completed
- [x] Step 1: [description]
- [x] Step 2: [description]
...

### Files Changed
- `path/to/file1.py` — [what changed]
- `path/to/file2.py` — [what changed]

### Tests
- Created: `tests/unit/test_XXX.py`
- Coverage: XX% (target: ≥80%)

### Completion Criteria
```bash
pytest tests/... -v  # ✅ Passed
ruff check ...       # ✅ Passed
mypy ...             # ✅ Passed
```

### Issues Encountered
- [None / Description of issues and how resolved]

### Ready for Review
- [ ] All steps completed
- [ ] All tests pass
- [ ] Coverage ≥ 80%
- [ ] No TODO/FIXME
- [ ] Goal achieved
```

---

## If Something Goes Wrong

### Plan is Unclear

STOP. Ask Planner:
```
Step 3 says "create protocol for X".
But I see there's already a similar protocol in file Y.
Should I extend Y or create new?
```

### Scope Exceeded

STOP. Go back to Phase 2 to split WS.

### Test Fails

Debug and fix. Don't skip tests.

### Can't Achieve Goal

STOP. Report what's blocking:
```
Cannot achieve Goal "API returns status".
Blocked by: missing database migration.
Need: WS for migration first.
```

---

## Checklist Before Completion

- [ ] **Goal achieved** (all AC ✅)
- [ ] All steps from plan executed
- [ ] All files created/modified as planned
- [ ] Type hints everywhere
- [ ] Tests written and passing
- [ ] Coverage ≥ 80%
- [ ] Regression suite passed
- [ ] No TODO/FIXME in code
- [ ] Execution Report prepared
