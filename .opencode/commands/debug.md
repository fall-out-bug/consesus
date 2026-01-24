---
description: Systematic debugging workflow (5-phase: Symptom → Hypothesis → Test → Root Cause → Impact)
agent: debug
---

# /debug — Systematic Debugging

Execute systematic debugging workflow for bug analysis and resolution.

## When to Use

- User types `/debug "{bug description}"`
- Bug symptoms observed, need systematic diagnosis
- Unknown root cause, need structured investigation

## Workflow

**IMPORTANT:** This command delegates to debugging workflow in issue master prompt.

### Load Debugging Workflow

```bash
cat sdp/prompts/commands/issue.md
```

**Section 4.0: Systematic Debugging Workflow contains:**
- Phase 1: Symptom Documentation
- Phase 2: Hypothesis Formation
- Phase 3: Systematic Elimination
- Phase 4: Root Cause Isolation
- Phase 5: Impact Chain Analysis

### Execute Instructions

Follow **Section 4.0 Systematic Debugging Workflow** from `sdp/prompts/commands/issue.md`:

**Phase 1: Symptom Documentation**
- Document observed behavior precisely
- Note when/how consistently it occurs
- State expected vs actual behavior
- Collect evidence (logs, stack traces, recent changes)

**Phase 2: Hypothesis Formation**
- List possible root causes (3+ hypotheses)
- Rank by probability (HIGH/MEDIUM/LOW)
- Provide supporting evidence for each
- Suggest quick test for each hypothesis

**Phase 3: Systematic Elimination**
- Test each hypothesis systematically
- Use specific verification commands
- Document test results (CONFIRMED/REJECTED)
- Collect evidence from each test

**Phase 4: Root Cause Isolation**
- Once confirmed, document precisely:
  - What: root cause description
  - Where: file, line, function
  - Why: step-by-step failure chain
  - Why Not Caught: missing tests, race condition, edge case

**Phase 5: Impact Chain Analysis**
- Analyze affected components
- Determine severity (P0 CRITICAL, P1 HIGH, P2 MEDIUM, P3 LOW)
- Assess business impact

### Failsafe Rule (3 Strikes)

Track debugging attempts:

| Attempt | Outcome | Notes |
|---------|---------|-------|
| 1 | Fix Attempt #1 | {description} |
| 2 | Fix Attempt #2 | {description} |
| 3 | Fix Attempt #3 | {description} |

**After 3 failed fix attempts:**
- Create bug report in `tools/hw_checker/docs/issues/issue-{ID}.md`
- Document all attempts and their outcomes
- Escalate to human developer
- Route to `/hotfix` (if P0) or `/bugfix` (if P1/P2)

## Master Prompt Location

📄 **sdp/prompts/commands/issue.md` → Section 4.0 (Systematic Debugging Workflow)

**Why reference?**
- Complete 5-phase debugging methodology
- Hypothesis testing framework
- Root cause isolation techniques
- Impact analysis
- Single source of truth for debugging

## Quick Reference

**Input:** Bug description (e.g., "API returns 500 on /submissions")
**Output:** Bug analysis + root cause + fix attempt + verification
**Next:** `/hotfix` (P0) or `/bugfix` (P1/P2) if fix needs permanent implementation
