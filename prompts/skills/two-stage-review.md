# Two-Stage Code Review Protocol

**Purpose:** Catch "well-written but wrong" bugs by separating spec compliance from code quality.

**Key Insight:** Don't polish wrong code. First verify correctness, then quality.

---

## Review Flow

```
Stage 1: Spec Compliance
         │
    ✅ Pass? ─── NO → Fix & Re-review
         │
        YES
         ↓
Stage 2: Code Quality
```

**Rule:** Stage 2 only runs if Stage 1 passes.

---

## Stage 1: Spec Compliance (BLOCKING)

**Question:** Does the code match the specification exactly?

### Checklist

1. **Goal Achievement** — All Acceptance Criteria pass?
   - Target: 100% AC passed
   - If ANY AC ❌ → **CHANGES REQUESTED**

2. **Specification Alignment**
   - [ ] All required features implemented?
   - [ ] No missing functionality?

3. **AC Coverage**
   - [ ] Each AC has corresponding test?
   - [ ] Tests verify actual AC requirements?

4. **No Over-Engineering**
   - [ ] No extra features beyond spec?

5. **No Under-Engineering**
   - [ ] Not simplified beyond spec?

### Output

```markdown
## Stage 1: Spec Compliance

**AC Status:** X/Y passed (Z%)
**Verdict:** PASS / CHANGES REQUESTED
```

**If Stage 1 FAIL → Stop. Fix issues, Re-review Stage 1.**

---

## Stage 2: Code Quality (only if Stage 1 PASS)

**Question:** Is the implementation well-engineered?

### Checklist

1. **Tests & Coverage** — Coverage ≥80%?
2. **Regression** — Existing tests still pass?
3. **AI-Readiness** — Files <200 LOC?
4. **Clean Architecture** — No layer violations?
5. **Type Hints** — All functions typed?
6. **Error Handling** — No `except: pass`?
7. **Security** — No vulnerabilities?
8. **No Tech Debt** — No TODOs without WS?
9. **Documentation** — Functions documented?
10. **Git History** — Clean commits?

### Output

```markdown
## Stage 2: Code Quality

**Coverage:** X%
**Verdict:** APPROVED / CHANGES REQUESTED
```

---

## Review Loop Logic

```
Submit → Stage 1 → FAIL → Fix → Re-review
                 → PASS → Stage 2 → FAIL → Fix → Re-review
                                  → PASS → APPROVED → Merge
```

**Max iterations:** 3. If 3 reviews fail → escalate to pair programming.

---

## Final Verdicts

| Verdict | Meaning | Next Step |
|---------|---------|-----------|
| **APPROVED** | Ready to merge | Deploy |
| **CHANGES REQUESTED** | Issues found | Fix and Re-review |

---

**Version:** 2.0.0  
**Related:** `@review`, `@build`
