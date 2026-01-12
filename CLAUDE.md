# CLAUDE.md

Guidance for Claude Code when working with this Spec-Driven Protocol (SDP) repository.

## Quick Start

**Protocol:** Spec-Driven Protocol (SDP) v0.3.0 — Workstream-driven development for AI agents.

**First time?** Read [README.md](README.md) and [PROTOCOL.md](PROTOCOL.md).

## Repository Overview

Spec-Driven Protocol (SDP) framework for AI-assisted software development.

**Key files:**
- [PROTOCOL.md](PROTOCOL.md) - Full protocol specification
- [RULES_COMMON.md](RULES_COMMON.md) - Common rules for all work
- [README.md](README.md) - Overview and quick start
- `prompts/` - Agent instructions for different modes
- `schema/` - JSON validation schemas
- `scripts/` - Validation and utility scripts
- `templates/` - Document templates

## Terminology

| Term | Scope | Size | Example |
|------|-------|------|---------|
| **Release** | Product milestone | 10-30 Features | R1: MVP |
| **Feature** | Large feature | 5-30 Workstreams | F1: User Auth |
| **Workstream** | Atomic task | SMALL/MEDIUM/LARGE | WS-001 |

**Scope metrics:**
- **SMALL**: < 500 LOC, < 1500 tokens
- **MEDIUM**: 500-1500 LOC, 1500-5000 tokens
- **LARGE**: > 1500 LOC → split into 2+ WS

**⚠️ NO time-based estimates** — Use scope metrics (LOC/tokens) only.

## Workstream Flow

```
┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐
│  ANALYZE   │───→│    PLAN    │───→│  EXECUTE   │───→│   REVIEW   │
│  (Phase 1) │    │  (Phase 2) │    │  (Phase 3) │    │  (Phase 4) │
└────────────┘    └────────────┘    └────────────┘    └────────────┘
```

**Prompts:** Use `prompts/structured/phase-{1,2,3,4}-*.md`

## Core Concepts

### Workstream-Driven Development

- **Workstream (WS):** Self-contained task executable in one shot by AI
- **One-shot execution:** No iterative loops; AI completes WS completely
- **AI-Readiness:** Files < 200 LOC, CC < 10, full type hints, coverage ≥80%

### Structured vs Multi-Agent Mode

**Structured Mode (recommended):**
- 4 phases with human checkpoints
- Faster, less coordination
- Use for most work

**Multi-Agent Mode (advanced):**
- Parallel agents (Analyst, Architect, Tech Lead, Developer, QA, DevOps)
- For complex large-scale changes
- See `archive/` for v1.2 multi-agent prompts

## Quality Gates (Non-Negotiable)

1. **AI-Readiness:** Files < 200 LOC, CC < 10, type hints everywhere
2. **Clean Architecture:** No layer violations (Domain ← App ← Infra ← Presentation)
3. **Error Handling:** No silent failures (`except: pass` forbidden)
4. **Test Coverage:** ≥80% mandatory
5. **No TODOs:** All tasks completed or deferred to new WS

## Commands

### Create a Feature

```bash
# Phase 1: Analyze and decompose
@prompts/structured/phase-1-analyze.md
# Create workstream map from feature requirements

# Phase 2: Plan first workstream
@prompts/structured/phase-2-design.md
# Detailed implementation plan for WS-001

# Phase 3: Execute workstream
@prompts/structured/phase-3-implement.md
# Code, tests, review

# Phase 4: Review and finalize
@prompts/structured/phase-4-review.md
# Validation against spec, quality gates
```

### Validate Structure

```bash
python sdp/scripts/validate.py docs/specs/{feature}/consensus/
```

## Key Guardrails

**Forbidden:**
- ❌ `except: pass` or bare exception handling
- ❌ Default values hiding errors
- ❌ Time-based estimates ("2 hours", "3 days")
- ❌ Layer violations (Domain depending on Infrastructure)
- ❌ Files > 200 LOC without splitting
- ❌ TODO comments without followup WS

**Required:**
- ✅ Type hints (full strict mypy)
- ✅ Tests first (TDD)
- ✅ Coverage ≥80%
- ✅ Clear architecture boundaries
- ✅ Explicit error handling

## File Organization

```
sdp/
├── PROTOCOL.md                   # Full specification
├── RULES_COMMON.md              # Common rules
├── prompts/
│   └── structured/              # Phase 1-4 prompts
├── schema/                       # JSON Schema validation
├── scripts/                      # Validation tools
├── templates/                    # Document templates
└── archive/                      # v1.2 materials
```

## Integration with Your Project

Copy `prompts/` and `schema/` to your project:

```bash
cp -r sdp/prompts your-project/
cp -r sdp/schema your-project/
cp -r sdp/scripts your-project/
```

Update your `CLAUDE.md` to reference SDP rules.

## Before You Code

1. **Read RULES_COMMON.md** - Shared rules everyone follows
2. **Check PROTOCOL.md** - Full protocol details
3. **Read the phase prompt** - Understand what this phase does
4. **Run validation** - Ensure structure is correct

## Tips

- **Scope first:** Estimate LOC/tokens before starting
- **One-shot:** Complete the workstream in one execution
- **Type it:** Mypy --strict on all code
- **Test first:** Write test before implementation
- **Clean boundaries:** No layer violations
