---
description: Code review with metrics-based quality checks. Reviews entire features, enforces quality gates, generates UAT guide.
agent: reviewer
---

# /codereview - Code Review

Comprehensive code review for features or workstreams with **Two-Stage Review Protocol**.

## When to Use

- After all WS in a feature are completed
- Before human UAT
- Part of `/oneshot` flow
- To verify quality standards

## Invocation

```bash
/codereview F60         # Review entire feature
/codereview WS-060      # Review all WS-060-XX
```

## Workflow

**IMPORTANT:** This skill uses **Two-Stage Review Protocol**.

### Load Master Prompt

```bash
cat .claude/skills/codereview.md
```

**This file contains:**
- Two-Stage Review Protocol (Stage 1: Spec Compliance → Stage 2: Code Quality)
- Stage 1 checklist (Goal, spec alignment, AC coverage, over/under-engineering)
- Stage 2 checklist (tests, coverage, clean code, security, maintainability)
- Review loop logic (fail → fix → re-review same stage)
- Metrics-based validation (coverage, complexity, LOC)
- Cross-WS consistency checks
- UAT guide generation
- Delivery notification template
- Verdict rules (APPROVED / CHANGES_REQUESTED only)

### Execute Instructions

Follow `.claude/skills/codereview.md`:

1. Find all WS in scope
2. For each WS (Two-Stage Review):
   - **Stage 1: Spec Compliance**
     - Goal achieved? (CRITICAL)
     - Specification alignment
     - AC coverage
     - No over-engineering
     - No under-engineering
     - If FAIL → CHANGES REQUESTED → Fix → Re-review Stage 1
   - **Stage 2: Code Quality** (only if Stage 1 passes)
     - Tests & Coverage
     - Regression
     - AI-Readiness
     - Clean Architecture
     - Type Hints
     - Error Handling
     - Security
     - No Tech Debt
     - Documentation
     - Git History
     - If FAIL → CHANGES REQUESTED → Fix → Re-review Stage 2
3. Cross-WS checks
4. Generate UAT guide
5. Send notification (if blockers)
6. Output verdict

## Key Checks

### Stage 1: Spec Compliance (BLOCKING)

- Goal achieved (100% AC passed)
- Specification alignment (matches spec exactly)
- AC coverage (each AC has implementation + tests)
- No over-engineering (no extra features)
- No under-engineering (no missing features)

### Stage 2: Code Quality (Only if Stage 1 passes)

- Coverage ≥ 80%
- No TODO/FIXME
- Type hints everywhere
- Clean Architecture compliance
- Regression tests pass
- Conventional commits per WS

## Review Loop

**Rule:** If a stage fails, fix and re-review the **same stage only** (not both stages).

- Stage 1 FAIL → Fix → Re-review Stage 1 → if PASS → proceed to Stage 2
- Stage 2 FAIL → Fix → Re-review Stage 2 only (Stage 1 already passed)

## Completion Requirements

**IMPORTANT:** Before marking codereview complete, verify ALL requirements:

📋 **Completion Protocol:** `sdp/docs/completion-protocol.md`

Quick checklist:
- [ ] All WS reviewed (both stages)
- [ ] Review Results appended to each WS file
- [ ] Verdict determined (APPROVED or CHANGES REQUESTED)
- [ ] UAT Guide created (if APPROVED)
- [ ] Feature Summary output to user
- [ ] GitHub issues updated (if configured)
- [ ] Blockers listed (if CHANGES REQUESTED)
