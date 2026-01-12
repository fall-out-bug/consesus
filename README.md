# Spec Driven Protocol (SDP)

Workstream-driven development protocol for AI agents with structured, one-shot execution.

[Русская версия](README_RU.md)

---

## Core Idea

**Workstream** = atomic task that AI completes in one shot, without iterative loops.

```
Feature → Workstreams → One-shot execution → Done
```

## Terminology

| Term | Scope | Size | Example |
|------|-------|------|---------|
| **Release** | Product milestone | 10-30 Features | R1: MVP |
| **Feature** | Large capability | 5-30 Workstreams | F1: User Auth |
| **Workstream** | Atomic task | SMALL/MEDIUM/LARGE | WS-001: Domain entities |

**Scope metrics:**
- **SMALL**: < 500 LOC, < 1500 tokens
- **MEDIUM**: 500-1500 LOC, 1500-5000 tokens
- **LARGE**: > 1500 LOC → **split into 2+ WS**

**NO time-based estimates.** Use LOC/tokens only.

## Workflow

```
┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐
│  ANALYZE   │───→│    PLAN    │───→│  EXECUTE   │───→│   REVIEW   │
│  (Phase 1) │    │  (Phase 2) │    │  (Phase 3) │    │  (Phase 4) │
└────────────┘    └────────────┘    └────────────┘    └────────────┘
```


## Quick Start

### 1. Create Feature Spec

```markdown
# Feature: User Authentication

## Overview
Users can register and login with email/password.

## Workstreams
- WS-001: Domain entities (User, Password, Session)
- WS-002: Repository pattern
- WS-003: Auth service
- WS-004: API endpoints
- WS-005: Tests
```

### 2. Phase 1: Analyze

```
Review WS-001:
- Acceptance criteria met?
- Code follows patterns?
- Tests adequate?
```

### 6. Repeat

Repeat phases 2-4 for remaining workstreams.

## Quality Gates

| Gate | Requirements |
|------|--------------|
| **AI-Readiness** | Files < 200 LOC, CC < 10, type hints |
| **Clean Architecture** | No layer violations |
| **Error Handling** | No `except: pass` |
| **Test Coverage** | ≥ 80% |
| **No TODOs** | All completed or new WS |

## Core Principles

| Principle | Summary |
|-----------|---------|
| **SOLID** | SRP, OCP, LSP, ISP, DIP |
| **DRY** | Don't Repeat Yourself |
| **KISS** | Keep It Simple |
| **YAGNI** | Build only what's needed |
| **TDD** | Tests first (Red → Green → Refactor) |
| **Clean Code** | Readable, maintainable |
| **Clean Architecture** | Dependencies point inward |

See [docs/PRINCIPLES.md](docs/PRINCIPLES.md) for details.

## File Structure

```
sdp/
├── PROTOCOL.md              # Full specification
├── CODE_PATTERNS.md         # Implementation patterns
├── RULES_COMMON.md          # Common rules
├── docs/
│   ├── PRINCIPLES.md        # SOLID, DRY, KISS, YAGNI
│   └── concepts/            # Clean Architecture, Artifacts, Roles
├── prompts/
│   ├── structured/          # Phase 1-4 prompts
│   └── commands/            # Slash commands
├── schema/                  # JSON validation
├── scripts/                 # Utilities
└── templates/               # Document templates
```

## Resources

| Resource | Purpose |
|----------|---------|
| [PROTOCOL.md](PROTOCOL.md) | Full specification |
| [docs/PRINCIPLES.md](docs/PRINCIPLES.md) | SOLID, DRY, KISS, YAGNI |
| [docs/concepts/](docs/concepts/) | Architecture concepts |
| [CODE_PATTERNS.md](CODE_PATTERNS.md) | Code patterns |
| [CLAUDE.md](CLAUDE.md) | Claude Code integration |

## Integration

```bash
# Copy to your project
cp -r prompts/ your-project/
cp -r schema/ your-project/
cp CLAUDE.md your-project/
```

---

**Version:** 0.3.0 | **Status:** Active
