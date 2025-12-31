# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Consensus Workflow** - a file-based multi-agent coordination framework for software development. It enables autonomous agents (Analyst, Architect, Tech Lead, Developer, QA, DevOps) to collaborate through structured JSON messages and shared artifacts.

**Protocol Version:** 2.0 (Unified Progressive Consensus)

## Core Architecture

### UPC Protocol v2.0

Agents communicate through file-based protocol:
- **State**: `docs/specs/{epic}/consensus/status.json` (single source of truth)
- **Artifacts**: Deliverables in `docs/specs/{epic}/consensus/artifacts/`
- **Messages**: JSON files in `docs/specs/{epic}/consensus/messages/inbox/{agent}/`
- **Schemas**: Validation schemas in `consensus/schema/`

### Protocol Tiers

| Tier | Validation | Use Case |
|------|------------|----------|
| Starter | JSON syntax | Bug fixes, prototypes |
| Standard | Full schema | Features |
| Enterprise | Schema + custom | Large systems |

### Execution Modes

| Mode | Flow | Use Case |
|------|------|----------|
| `full` | All agents | New features |
| `fast_track` | dev → qa | Bug fixes |
| `hotfix` | dev → devops | Emergencies |

## Key Commands

```bash
# Initialize epic
python consensus/scripts/init.py EP-001 --title "Feature" --tier standard

# Validate epic
python consensus/scripts/validate.py docs/specs/EP-001
```

## Agent Workflow

When acting as an agent:
1. Read `consensus/prompts/{role}.md` for instructions
2. Read `status.json` to verify phase
3. Perform work, create artifacts
4. Validate against schema
5. Update `status.json`
6. Send messages to next agent

## Critical Rules

### Language
- **Protocol JSON**: English only
- **User docs** (`epic.md`): Any language

### Inbox Rules
- **READ**: Only your own inbox
- **WRITE**: Only to OTHER agents' inboxes

### Validation
- All artifacts must validate against `consensus/schema/`
- Use `python consensus/scripts/validate.py` before completing

### Clean Architecture
Dependencies MUST point inward:
```
Presentation → Infrastructure → Application → Domain
```

### Forbidden Patterns
- `except: pass` (silent failures)
- Default values masking exceptions
- Catch-all handlers hiding errors

## Key Files

| File | Purpose |
|------|---------|
| `PROTOCOL.md` | Full protocol specification |
| `consensus/prompts/` | Agent instruction files |
| `consensus/schema/` | JSON validation schemas |
| `consensus/scripts/` | Validation and init tools |
| `docs/adr/` | Architecture decisions |

## Self-Verification

Before completing work:
- [ ] Clean Architecture boundaries respected
- [ ] Artifacts validated against schema
- [ ] `status.json` updated
- [ ] All text in protocol JSON is English
