# Spec-Driven Protocol (SDP)

Workstream-driven development protocol for AI agents with structured, one-shot execution.

## Terminology

| Term | Scope | Size | Example |
|------|-------|------|---------|
| **Release** | Product milestone | 10-30 Features | R1: MVP |
| **Feature** | Large feature | 5-30 Workstreams | F1: User Auth |
| **Workstream** | Atomic task | SMALL/MEDIUM/LARGE | WS-001: User entity |

**Scope metrics:**
- **SMALL**: < 500 LOC, < 1500 tokens
- **MEDIUM**: 500-1500 LOC, 1500-5000 tokens
- **LARGE**: > 1500 LOC → split into 2+ WS

**⚠️ NO time-based estimates** (hours/days/weeks). Use scope metrics only.

**Hierarchy:**
```
Product:      Release → Feature → Workstream
Architecture: L1 (System) → L2 (Domain) → L3 (Component) → L4 (Workstream)
```

## Quick Start

### 1. Initialize a Feature

Create feature specification:
```markdown
# Feature: User Authentication

## Overview
Users can register and login with email/password.

## Workstreams (High-level)
- WS-001: Domain entities (User, Password, Session)
- WS-002: Repository pattern
- WS-003: Auth service
- WS-004: API endpoints
- WS-005: Tests
```

### 2. Phase 1: Analyze and Decompose

Use `prompts/structured/phase-1-analyze.md`:

```
@prompts/structured/phase-1-analyze.md
Decompose feature into workstreams.
Estimate scope for each (SMALL/MEDIUM/LARGE).
Identify dependencies.
```

**Output:** Detailed workstream map with LOC/token estimates.

### 3. Phase 2: Plan Workstream

Use `prompts/structured/phase-2-design.md`:

```
@prompts/structured/phase-2-design.md
Plan WS-001: Domain entities
- Identify classes/functions needed
- Type signatures
- Tests needed
- LOC estimate
```

**Output:** Implementation plan with code skeleton.

### 4. Phase 3: Execute Workstream

Use `prompts/structured/phase-3-implement.md`:

```
@prompts/structured/phase-3-implement.md
Implement WS-001 following plan:
- Write tests first (TDD)
- Implement
- Run tests, check coverage ≥80%
- Self-review
```

**Output:** Code with tests, coverage report, self-review notes.

### 5. Phase 4: Review and Finalize

Use `prompts/structured/phase-4-review.md`:

```
@prompts/structured/phase-4-review.md
Review WS-001:
- All acceptance criteria met?
- Code follows patterns?
- Type hints complete?
- Tests adequate?
- Ready for next WS?
```

**Output:** Review checklist, issues found (or approval).

### 6. Repeat for Next Workstream

Repeat phases 2-4 for WS-002, WS-003, etc.

## File Organization

```
sdp/
├── PROTOCOL.md                   # Full specification
├── CODE_PATTERNS.md              # Code patterns & anti-patterns
├── RULES_COMMON.md              # Common rules for all work
├── README.md                     # This file
├── prompts/
│   ├── structured/              # Phase 1-4 prompts
│   │   ├── phase-1-analyze.md
│   │   ├── phase-2-design.md
│   │   ├── phase-3-implement.md
│   │   └── phase-4-review.md
│   └── commands/                # Slash command prompts (advanced)
├── schema/                       # JSON Schema validation
│   ├── feature.schema.json
│   ├── workstream.schema.json
│   └── review.schema.json
├── scripts/
│   └── validate.py              # Validate workstream structure
├── templates/
│   ├── feature-template.md
│   ├── workstream-template.md
│   └── uat-guide-template.md
└── archive/
    └── v1.2/                    # Multi-agent mode (deprecated)
```

## Core Concepts

### Workstream-Driven Development

- **Workstream (WS):** Self-contained task executable in one shot by AI agent
- **One-shot execution:** Agent completes WS entirely; no iterative loops
- **AI-Readiness:**
  - Files < 200 LOC (split larger files)
  - Cyclomatic complexity < 10
  - Full type hints (mypy --strict)
  - Coverage ≥80%

### Quality Gates (Non-Negotiable)

1. **AI-Readiness:** Files < 200 LOC, CC < 10, type hints everywhere
2. **Clean Architecture:** No layer violations
3. **Error Handling:** No silent failures (`except: pass` forbidden)
4. **Test Coverage:** ≥80% mandatory
5. **No TODOs:** All tasks completed or deferred to new WS

### Code Patterns

See [CODE_PATTERNS.md](CODE_PATTERNS.md) for:
- 8 recommended patterns (Domain-Driven Design, Repository, SAGA, etc.)
- 5 anti-patterns to avoid (God Object, Silent Failures, etc.)
- Detailed code examples for each

## Validation

```bash
# Validate workstream structure
python sdp/scripts/validate.py docs/specs/feature/WS-001/

# Expected output:
# ✓ JSON Syntax Check
# ✓ Schema Validation
# ✓ Phase Requirements
# ✓ All checks passed
```

## Metrics

Track these for continuous improvement:

| Metric | Target |
|--------|--------|
| WS completion scope | SMALL/MEDIUM/LARGE as planned |
| Coverage | ≥ 80% |
| Type checking | 0 mypy --strict errors |
| Code complexity | CC < 10 |
| File size | < 200 LOC (per file) |

## Execution Modes

### Structured Mode (Recommended)

4-phase workflow (Analyze → Plan → Execute → Review) with human checkpoints.
- Best for: Most features, clear requirements
- Time: ~1-2 hours per workstream
- Coordination: Minimal (single developer + AI)

### Multi-Agent Mode (Advanced)

Parallel agents (Analyst, Architect, Tech Lead, Developer, QA, DevOps).
- Best for: Large systems, many workstreams
- Time: ~4-8 hours per epic
- Coordination: Higher (multiple roles)
- See: `archive/v1.2/` for multi-agent prompts

## Best Practices

1. **Scope first**: Estimate LOC/tokens before starting
2. **One-shot**: Complete the workstream in one execution (no iterative feedback loops)
3. **Type everything**: Use mypy --strict
4. **Test first**: Write tests before implementation
5. **Clean architecture**: No layer violations
6. **No time estimates**: Use LOC/tokens instead

## Guardrails

**Forbidden:**
- ❌ `except: pass` or bare exception handling
- ❌ Default values hiding errors
- ❌ Time-based estimates ("2 hours", "this week")
- ❌ Layer violations (Domain depending on Infrastructure)
- ❌ Files > 200 LOC without splitting
- ❌ TODO comments without followup WS

**Required:**
- ✅ Type hints everywhere (mypy --strict)
- ✅ Tests first (Red-Green-Refactor)
- ✅ Coverage ≥80%
- ✅ Clear architecture boundaries
- ✅ Explicit error handling
- ✅ Self-review checklist completed

## Integration with Your Project

To use SDP in your project:

```bash
# Copy SDP framework files
cp -r sdp/prompts your-project/
cp -r sdp/schema your-project/
cp -r sdp/scripts your-project/

# Create your CLAUDE.md
cat > your-project/CLAUDE.md <<EOF
# CLAUDE.md for Your Project

This project uses Spec-Driven Protocol (SDP) for workstream-driven development.

See /sdp/CLAUDE.md for detailed guidance.

## Project-Specific Commands
[Add your custom commands here]
EOF
```

## Resources

| Resource | Purpose |
|----------|---------|
| [PROTOCOL.md](PROTOCOL.md) | Full protocol specification |
| [CODE_PATTERNS.md](CODE_PATTERNS.md) | Recommended patterns & anti-patterns |
| [RULES_COMMON.md](RULES_COMMON.md) | Common rules for all work |
| [CLAUDE.md](CLAUDE.md) | Claude Code integration guide |
| [docs/guides/](docs/guides/) | IDE integration guides |

## Support

For questions or issues:
1. Check [PROTOCOL.md](PROTOCOL.md) for detailed specifications
2. Review [CODE_PATTERNS.md](CODE_PATTERNS.md) for examples
3. Validate your structure with `scripts/validate.py`
4. Review [prompts/](prompts/) for phase instructions

## License

MIT License - see [LICENSE](LICENSE)

---

**Protocol Version:** v0.3.0
**Last Updated:** 2026-01-12
**Status:** ✅ Active
