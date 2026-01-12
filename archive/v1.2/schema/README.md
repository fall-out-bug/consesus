# Archived v1.2 Multi-Agent Schemas

These JSON Schemas were used in UPC Protocol v1.2 multi-agent workflow.

**Archived:** 2026-01-07  
**Reason:** Migration to v2.0 structured mode (4-phase workflow)

## Schemas in Archive

| Schema | Lines | Purpose (v1.2) |
|--------|-------|----------------|
| message.schema.json | 64 | Agent-to-agent communication validation |
| requirements.schema.json | 76 | Analyst output validation (requirements.json) |
| architecture.schema.json | 99 | Architect output validation (architecture.json) |
| plan.schema.json | 88 | Tech Lead output validation (plan.json) |

**Total:** 327 lines of JSON Schema

## Why Archived?

**v1.2 Multi-Agent Workflow:**
- Analyst → requirements.json (validated)
- Architect → architecture.json (validated)
- Tech Lead → plan.json (validated)
- Agents communicate via message.json

**v2.0 Structured Workflow:**
- Phase 1-4: All outputs in markdown
- No JSON artifacts
- No inter-agent messages

## Active Schemas (v2.0)

Only status.schema.json remains active in ../../../schema/

## Restoration

If needed:
```bash
cp consensus/archive/v1.2/schema/*.schema.json consensus/schema/
# Update index.json
```
