---
description: Autonomous feature execution with checkpoint/resume support
agent: orchestrator
model: inherit
---

# /oneshot — Autonomous Feature Execution

When called with `/oneshot {feature-id}`:

1. Load full prompt: `@.claude/skills/oneshot.md`
2. Follow autonomous execution algorithm (PR approval, checkpoint/resume)
3. Execute all WS by dependencies
4. Generate Execution Report

## Quick Reference

**Input:** Feature ID (e.g., F60)
**Output:** All WS executed + Execution Report
**Next:** `/codereview F{XX}` → Human UAT → `/deploy F{XX}`
