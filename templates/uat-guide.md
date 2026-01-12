# UAT Guide: {Feature Name}

**Feature:** F{XX}
**Version:** {X.Y.Z}
**Date:** {YYYY-MM-DD}

---

## Overview

{What the feature does in 2-3 sentences for human tester}

---

## Prerequisites

Before testing, ensure:

- [ ] Docker running (`docker ps`)
- [ ] `poetry install` executed
- [ ] Configuration file set up
- [ ] Database accessible (if needed)
- [ ] Redis running (if needed)

### Quick Environment Check

```bash
# Verify environment
poetry run python -c "import project; print(f'Version: {project.__version__}')"
```

---

## Quick Verification (5 minutes)

### Smoke Test

```bash
# Start services
docker-compose up -d

# Basic check
poetry run app {main_command}

# Expected result:
# {description of what should happen}
```

### Visual Check

- [ ] Open {what to open: logs/UI/API}
- [ ] Verify {what should display}
- [ ] Ensure {no errors/warnings}

---

## Detailed Scenarios

### Scenario 1: Happy Path

**Description:** {main use case}

**Steps:**
1. {step 1}
2. {step 2}
3. {step 3}

**Expected Result:**
- {outcome 1}
- {outcome 2}

---

### Scenario 2: Error Handling

**Description:** {how system handles errors}

**Steps:**
1. {trigger error condition}
2. {observe response}

**Expected Result:**
- Graceful error message (not stack trace)
- Error logged
- System continues working

---

### Scenario 3: Edge Cases

**Description:** {boundary cases}

**Test Cases:**
| Input | Expected Output |
|-------|-----------------|
| {edge case 1} | {expected} |
| {edge case 2} | {expected} |

---

## 🔴 Red Flags

**❌ If you see any of these — agent made a mistake:**

| # | Red Flag | Where to Check | Severity |
|---|----------|----------------|----------|
| 1 | Stack trace in output | Logs, stderr | 🔴 HIGH |
| 2 | Empty response | API response body | 🔴 HIGH |
| 3 | Timeout (>30s) | Network, DB connection | 🟡 MEDIUM |
| 4 | Warning in logs | Log files | 🟡 MEDIUM |
| 5 | Unexpected data format | Response structure | 🟡 MEDIUM |
| 6 | Deprecated warnings | Console output | 🟢 LOW |

**What to do if Red Flag found:**
1. Copy error message / screenshot
2. Check corresponding WS Execution Report
3. Create issue or return to `/review`

---

## Code Sanity Checks

Quick check that code is in order:

```bash
# 1. No TODO/FIXME
grep -rn "TODO\|FIXME" src/{feature_module}/
# Expected: empty

# 2. File sizes reasonable
wc -l src/{feature_module}/*.py
# Expected: all < 200 lines

# 3. Clean Architecture followed
grep -r "from project.infrastructure" src/domain/
# Expected: empty

# 4. Tests pass
poetry run pytest tests/unit/test_{feature}*.py -v
# Expected: all passed

# 5. Coverage sufficient
poetry run pytest tests/unit/test_{feature}*.py --cov=src/{feature_module} --cov-report=term-missing
# Expected: >= 80%
```

---

## Performance Baseline (if applicable)

| Operation | Expected | Acceptable | Measured |
|-----------|----------|------------|----------|
| {operation 1} | < Xms | < Yms | ___ms |
| {operation 2} | < Xms | < Yms | ___ms |

---

## Sign-off Checklist

### Tester Checklist

- [ ] All scenarios passed
- [ ] Red flags absent
- [ ] Code sanity checks passed
- [ ] Performance within baseline

### Approval

| Role | Name | Date | Status |
|------|------|------|--------|
| Developer (agent) | {agent} | {date} | ✅ |
| Reviewer | {reviewer} | {date} | ⬜ |
| Human Tester | ___________ | ___________ | ⬜ |

### Final Decision

⬜ **APPROVED** — ready to deploy
⬜ **NEEDS WORK** — fixes required (see comments below)

---

## Comments

```
{comments from human tester}
```

---

## Related Documents

- Feature spec: `docs/specs/feature_{XX}/`
- Workstreams: `docs/workstreams/backlog/WS-{XX}-*.md`
- Review Results: see each WS file
