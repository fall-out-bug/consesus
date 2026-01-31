---
description: Contract-driven workflow for model-agnostic WS (generates/approves tests as contract)
agent: builder
---

# /test — Generate/Approve Tests as Contract

Generate or approve tests as contract for workstream implementation. T0 tier only (architectural decisions, contract creation).

## When to Use

- User types `/test {WS-ID}`
- After `/design` is complete (Interface section exists)
- Before `/build` (implementation phase)
- Need to create/validate test contract for WS

## Workflow

**IMPORTANT:** This command delegates to master prompt.

### Load Master Prompt

```bash
cat .claude/skills/test.md
```

**This file contains:**
- Contract-driven WS methodology
- Capability tier rules (T0-T3)
- Test generation algorithm
- Contract principle (tests = contract)
- Completeness verification

### Execute Instructions

Follow `.claude/skills/test.md`:

**Step 1: Read Context**
```bash
# Read WS file
cat tools/hw_checker/docs/workstreams/backlog/WS-{ID}-*.md

# Read architecture decisions
cat tools/hw_checker/docs/PROJECT_MAP.md
```

**Step 2: Verify /design Complete**
- Check Interface section exists in WS
- Verify function signatures with types
- Check docstrings with Args/Returns/Raises

**Step 3: Create/Approve Tests**
- If no tests exist → create full test set
- If tests exist → verify completeness, supplement if needed
- Ensure tests cover all edge cases

**Step 4: Update WS File**
- Add "Tests (DO NOT MODIFY)" section to WS
- Ensure tests are executable (fail with `NotImplementedError`)
- Mark contract as read-only for T2/T3 models

**Step 5: Verify Completion Criteria**
- Tests are executable
- Tests fail before implementation (RED)
- Tests pass after implementation (GREEN)
- Coverage targets defined

## Contract Principle

**Tests = Single Source of Truth for Behavior**

### Contract Rules:

1. **Tests NOT changed in /build** — only implementation bodies
2. **Tests define behavior** — if test requires X, implementation must do X
3. **Tests are executable** — `pytest path/to/test.py` must run
4. **Tests fail before implementation** — `NotImplementedError` in functions → RED
5. **Tests green after implementation** — /build makes them GREEN

## Capability Tiers

This command enforces **T0 tier only**:

| Tier | Capabilities | When to Use |
|-------|-------------|-------------|
| **T0** | Architectural decisions, contract creation | /test command (always T0) |
| T1 | Basic implementation | Strong models |
| T2 | Refactoring with constraints | Medium models |
| T3 | Fills in implementation | Weak models |

**For T2/T3:**
- Contract (Tests section) is READ-ONLY
- Cannot modify Interface or Tests
- Only implement function bodies to satisfy contract

## Master Prompt Location

📄 **.claude/skills/test.md` (12,767 bytes)

**Why reference?**
- Complete contract-driven methodology
- Test generation algorithm
- Capability tier rules
- Verification commands
- Single source of truth

## Quick Reference

**Input:** WS ID (e.g., WS-060-01)
**Output:** Test contract in WS file (executable, failing with NotImplementedError)
**Next:** `/build {WS-ID}` to implement (tests will turn GREEN)
