# Systematic Debugging — 4-Phase Root Cause Analysis

**Purpose:** Replace trial-and-error with scientific method. Evidence-based, not assumption-based.

## Core Principles

1. **Evidence First** — Collect facts before guessing
2. **One Hypothesis** — Test one thing at a time
3. **Minimal Change** — Smallest possible fix
4. **Failsafe Rule** — 3 failed fixes → STOP, question architecture

---

## 4-Phase Process

### Phase 1: Evidence Collection

**Goal:** Gather all observable facts.

**Checklist:**
- [ ] **Error Messages** — Stack traces, logs
- [ ] **Reproduce the Issue** — Exact steps, consistency (always/sometimes)
- [ ] **Recent Changes** — `git log --since="7 days ago"`
- [ ] **Environment State** — Versions, dependencies

**Output:**
```markdown
**Error:** [message]
**Steps:** 1... 2... 3...
**Expected:** [X] **Actual:** [Y]
**Recent changes:** [files changed]
```

---

### Phase 2: Pattern Analysis

**Goal:** Find working examples and compare.

**Checklist:**
- [ ] **Find working cases** — Similar code that works
- [ ] **Compare** — Working vs broken

| Aspect | Working | Broken | Difference |
|--------|---------|--------|------------|
| Input | [value] | [value] | [diff] |

**Pattern identified:** [What changed between working and broken]

---

### Phase 3: Hypothesis Testing

**Rules:**
1. ONE hypothesis at a time
2. Minimal change for test
3. Clear pass/fail outcome

**Format:**
```markdown
**Hypothesis:** [Clear statement]
**Test:** [Minimal code]
**Result:** PASS/FAIL
**Conclusion:** Confirmed/Rejected
```

---

### Phase 4: Implementation

**Goal:** Fix root cause with TDD.

1. **Write failing test** — Reproduce the bug
2. **Implement minimal fix** — No refactoring, just fix
3. **Verify** — Unit + regression + integration tests

**Output:**
```markdown
**Root Cause:** [Explanation]
**Fix:** [What changed]
**Verification:** Unit ✅ Regression ✅ Integration ✅
```

---

## Root-Cause Tracing

Trace from symptom to root cause:

```
Symptom (Error)
    ↓
Function A (receives bad data)
    ↓
Function B (passes bad data)
    ↓
Function C (creates bad data) ← ROOT CAUSE
```

---

## Failsafe Rule: 3 Strikes

**After 3 failed fix attempts → STOP, escalate to architecture review.**

```markdown
**Attempt #1:** [hypothesis] → ❌ FAIL
**Attempt #2:** [hypothesis] → ❌ FAIL
**Attempt #3:** [hypothesis] → ❌ FAIL

🚨 FAILSAFE TRIGGERED
→ Question architecture, create refactoring WS
```

---

## Quick Reference

| Phase | Goal | Key Action |
|-------|------|------------|
| 1. Evidence | Gather facts | Logs, repro steps |
| 2. Pattern | Find working case | Compare working vs broken |
| 3. Hypothesis | Test one theory | Minimal isolated test |
| 4. Implementation | Fix with TDD | Failing test → fix → verify |

---

**Version:** 2.0.0  
**Related:** `/issue`, `/hotfix`, `/bugfix`
