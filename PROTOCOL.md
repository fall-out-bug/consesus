# Spec-Driven Protocol (SDP) v0.3.0

Workstream-driven development protocol for AI agents with structured, one-shot execution.

---

## Navigation

```
Need to...                            →  Use Command
─────────────────────────────────────────────────────
Gather requirements                   →  /idea or @idea
Design workstreams                    →  /design or @design
Execute a workstream                  →  /build or @build
Review quality                        →  /review or @review
Deploy to production                  →  /deploy or @deploy
Fix bugs                              →  /bugfix or @bugfix
Emergency fix (P0)                    →  /hotfix or @hotfix
Debug and route issues                →  /issue or @issue
Autonomous execution                  →  /oneshot or @oneshot
See code patterns                     →  CODE_PATTERNS.md
Check the rules                       →  Guardrails (below)
Understand principles                 →  docs/PRINCIPLES.md
Project-specific rules                →  PROJECT_CONVENTIONS.md
```

---

## Command Workflow

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  /idea   │──→│ /design  │──→│  /build  │──→│ /review  │──→│ /deploy  │
│  @idea   │   │ @design  │   │  @build  │   │ @review  │   │ @deploy  │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
     │              │              │              │              │
     ▼              ▼              ▼              ▼              ▼
  Draft         Workstreams      Code         Quality      Production
```

**Commands:**
- `/idea` — Requirements gathering → `docs/drafts/`
- `/design` — Create workstreams → `docs/workstreams/backlog/`
- `/build` — Execute workstream → code + tests
- `/review` — Quality check → APPROVED/CHANGES_REQUESTED
- `/deploy` — Production deployment → Docker, CI/CD, release notes

**Alternative:**
- `/oneshot` — Autonomous execution of entire feature (executes all workstreams)

---

## Terminology

| Term | Scope | Size | Example |
|------|-------|------|---------|
| **Release** | Product milestone | 10-30 Features | R1: MVP |
| **Feature** | Large capability | 5-30 Workstreams | F1: User Auth |
| **Workstream (WS)** | Atomic task | SMALL/MEDIUM/LARGE | WS-001: Domain entities |

**Scope metrics for Workstream:**
- **SMALL**: < 500 LOC, < 1500 tokens
- **MEDIUM**: 500-1500 LOC, 1500-5000 tokens
- **LARGE**: > 1500 LOC → split into 2+ WS

### NO TIME-BASED ESTIMATES

**FORBIDDEN to use time for estimation:**
- "This will take 2 hours"
- "Need 3 days"
- "Won't finish this week"
- "No time for this"
- "This takes too long"

**USE scope metrics:**
- "This is MEDIUM workstream (1000 LOC, 3000 tokens)"
- "Scope exceeded, need to split into 2 WS"
- "By scope this is SMALL task"

#### Permitted Time References (Exceptions)

Time **is allowed** only in these cases (and **is not a scope estimate**):

- **Telemetry / measurements**: elapsed time, timestamps in logs, execution metrics (e.g., `"elapsed": "1h 23m"`)
- **SLA / operational targets**: hotfix/bugfix target windows (e.g., "P0 hotfix: <2h", "P1/P2 bugfix: <24h")
- **Human Verification (UAT)**: guidance for human testers ("Smoke test: 30 sec", "Scenarios: 5-10 min")

In all other contexts **time is forbidden** — use only LOC/tokens and sizing (SMALL/MEDIUM/LARGE).

**Why NOT time:**
1. AI agents work at different speeds (Sonnet ≠ Haiku ≠ GPT)
2. Scope is objective (LOC, tokens), time is subjective
3. Time creates false pressure ("running out of time" → rushing → bugs)
4. One-shot execution: agent completes WS in one pass, regardless of "time"

### Hierarchy (Product)

```
VISION.md (product vision)
    ↓
RELEASE_PLAN.md (releases)
    ↓
Feature (F01-F99) — large capabilities
    ↓
Workstream (WS-001-WS-999) — atomic tasks
```

### Deprecated Terms

- ~~Epic (EP)~~ → **Feature (F)** (since 2026-01-07)
- ~~Sprint~~ → not used
- ~~Phase 1-4 workflow~~ → **Slash commands** (since 2026-01-12)

---

## Guardrails

### AI-Readiness (BLOCKING)

| Rule | Threshold | Check |
|------|-----------|-------|
| File size | < 200 LOC | `wc -l` |
| Complexity | CC < 10 | `ruff --select=C901` |
| Type hints | 100% public | mypy --strict |
| Nesting | ≤ 3 levels | Visual |

### Clean Architecture (BLOCKING)

```
Domain      →  Does NOT import from other layers
Application →  Does NOT import infrastructure directly
```

```bash
# Check for violations
grep -r "from infrastructure" domain/ application/
# Should be empty
```

**See**: [docs/PRINCIPLES.md](docs/PRINCIPLES.md) | [docs/concepts/clean-architecture/](docs/concepts/clean-architecture/README.md)

### Error Handling (BLOCKING)

```python
# FORBIDDEN
except:
    pass

except Exception:
    return None

# REQUIRED
except SpecificError as e:
    log.error("operation.failed", error=str(e), exc_info=True)
    raise
```

### Security

- [ ] No `privileged: true`
- [ ] No `/var/run/docker.sock` mounts
- [ ] Resource limits defined
- [ ] No string interpolation in shell commands

---

## Quality Gates

### Gate 1: idea → design
- [ ] Requirements clear and complete
- [ ] Success criteria defined
- [ ] Non-goals identified

### Gate 2: design → build
- [ ] **WS does not exist** in INDEX (verified)
- [ ] **Scope estimated**, not exceeding MEDIUM
- [ ] Dependencies identified
- [ ] Acceptance criteria include: tests + coverage + regression
- [ ] **NO time estimates** (hours/days)
- [ ] DO/DON'T rules defined (from PROJECT_CONVENTIONS.md)

### Gate 3: build → review
- [ ] All acceptance criteria met
- [ ] **Coverage ≥ 80%** for changed files
- [ ] **Regression passed** (all tests)
- [ ] **No TODO/FIXME** in code
- [ ] Execution report filled

### Gate 4: review → deploy
- [ ] AI-Readiness: ✅
- [ ] Clean Architecture: ✅
- [ ] Error Handling: ✅
- [ ] Tests & Coverage: ✅ (≥80%)
- [ ] Regression: ✅ (all tests)
- [ ] DO/DON'T rules followed: ✅

### Gate 5: deploy → production (Human UAT)

**UAT (User Acceptance Testing)** — human verification before deploy:

| Step | Description | Time |
|------|-------------|------|
| 1 | Quick Smoke Test | 30 sec |
| 2 | Detailed Scenarios (happy path + errors) | 5-10 min |
| 3 | Red Flags Check | 2 min |
| 4 | Sign-off | 1 min |

**UAT Guide created automatically** after `/review` returns APPROVED:
- Feature-level: `docs/uat/F{XX}-uat-guide.md`
- WS-level: "Human Verification (UAT)" section in WS file

**Without human Sign-off → Deploy blocked.**

---

## WS Scope Control

**Size metrics (instead of time):**

| Size | Lines of Code | Tokens | Action |
|------|---------------|--------|--------|
| **SMALL** | < 500 | < 1500 | ✅ Optimal |
| **MEDIUM** | 500-1500 | 1500-5000 | ✅ Acceptable |
| **LARGE** | > 1500 | > 5000 | ❌ **SPLIT** |

**Rule:** All WS must be SMALL or MEDIUM.

**If scope exceeded during /build:**
→ STOP, use `/design` to split into WS-XXX-01, WS-XXX-02

---

## Test Coverage Gate

**Minimum:** 80% for changed/created files

```bash
pytest tests/unit/test_module.py -v \
  --cov=src/module \
  --cov-report=term-missing \
  --cov-fail-under=80
```

**If coverage < 80% → CHANGES REQUESTED (HIGH)**

---

## Regression Gate

**After each /build:**

```bash
# All tests MUST pass
pytest tests/
```

**If regression broken → CHANGES REQUESTED (CRITICAL)**

---

## TODO/Later Gate

**STRICTLY FORBIDDEN in code:**
- `# TODO: ...`
- `# FIXME: ...`
- Comments like "will do later", "temporary solution"

**Exception:** `# NOTE:` — only for clarifications

**If found → CHANGES REQUESTED (HIGH)**

---

## NO TECH DEBT

**The Tech Debt concept is FORBIDDEN in this protocol.**

- "This is tech debt, we'll do it later"
- "Temporary solution, will return later"
- "Dirty code but it works"
- "Postpone refactoring"

✅ **Rule: fix all issues immediately.**

**If code doesn't meet standards:**
1. Fix in current WS
2. If scope exceeded → split into substreams (see below)
3. DO NOT leave "for later"

**Philosophy:** Every WS leaves code in ideal state. No accumulating debt.

---

## Substreams: Splitting Rules

**If WS needs to be split:**

### Numbering Format (STRICT)

```
WS-{PARENT_ID}-{SEQ}

Where:
- PARENT_ID = parent WS ID (3 digits with leading zeros)
- SEQ = substream sequence number (2 digits: 01, 02, ... 99)
```

**Examples:**
```
WS-050         ← parent (being split)
├── WS-050-01  ← first substream
├── WS-050-02  ← second substream
├── WS-050-03  ← third substream
├── ...
├── WS-050-10  ← tenth (sorting works!)
└── WS-050-15  ← fifteenth
```

**FORBIDDEN formats:**
```
❌ WS-050-A, WS-050-B      (letters)
❌ WS-050-part1            (words)
❌ WS-050.1, WS-050.2      (dots)
❌ WS-50-1                 (no leading zeros in PARENT)
❌ WS-050-1                (single-digit SEQ — always 01, 02...)
```

### REQUIRED when splitting:

1. **Create ALL substream files** in `docs/workstreams/backlog/`:
   ```
   WS-050-01-domain-entities.md
   WS-050-02-application-layer.md
   WS-050-03-infrastructure.md
   ```

2. **Fill each substream** completely (not stub):
   - Goal
   - Context
   - Dependencies (WS-XXX-01 → WS-XXX-02 → ...)
   - Acceptance criteria
   - DO/DON'T rules (from PROJECT_CONVENTIONS.md)
   - Test plan

3. **Update INDEX.md** with new WS

4. **Delete or mark parent WS** as "Split → WS-XXX-01, WS-XXX-02"

### FORBIDDEN:

- Referencing non-existent WS ("see WS-050-02" without creating file)
- Leaving empty stubs ("TODO: fill in")
- Splitting without creating files
- Partial execution ("did part, rest in another WS")
- Formats: `24.1`, `WS-24-1`, `WS-050-1`, `WS-050-part1`
- Time estimates: "0.5 days", "3 days" — only LOC/tokens

---

## ADR Template

When making an architectural decision, create:

`docs/adr/YYYY-MM-DD-{title}.md`

```markdown
# ADR: {Title}

## Status
Proposed / Accepted / Deprecated

## Context
[What is the problem? What constraints?]

## Decision
[What did we decide to do?]

## Alternatives Considered
1. [Alternative 1] — why not
2. [Alternative 2] — why not

## Consequences
- [+] Benefit
- [-] Drawback
- [!] Risk
```

---

## Workstream Format

See `templates/workstream.md` for complete template with DO/DON'T blocks.

**Essential sections:**
```markdown
# Workstream: {Title}

**ID:** WS-XXX-YY
**Feature:** F-XXX
**Status:** READY/EXECUTING/DONE
**Complexity:** SMALL/MEDIUM/LARGE

## Goal
[Clear, one-sentence goal]

## Context
[Why this workstream exists]

## Dependencies
- [ ] WS-XXX-YY: [Description]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Coverage ≥ 80%
- [ ] Type hints complete
- [ ] No TODO/FIXME
- [ ] Clean Architecture followed

## DO / DON'T
### Architecture
✅ DO: ...
❌ DON'T: ...

### Code Quality
✅ DO: ...
❌ DON'T: ...

[See templates/workstream.md for full template]
```

---

## Documentation Hierarchy (C4-like)

```
L1: System      docs/SYSTEM_OVERVIEW.md
    ↓ General system context, boundaries, main domains

L2: Domain      docs/domains/{domain}/DOMAIN_MAP.md
    ↓ Domain structure, components, integrations

L3: Component   docs/domains/{domain}/components/{comp}/SPEC.md
    ↓ Detailed component specification

L4: Workstream  docs/workstreams/{status}/WS-XXX.md
    ↓ Specific task for execution
```

### Navigation Flow

**Using /idea:**
1. User describes feature
2. AI reads L1 (`SYSTEM_OVERVIEW.md`) for context
3. AI generates draft in `docs/drafts/idea-{slug}.md`

**Using /design:**
1. AI reads idea draft
2. AI reads L1/L2 for architecture context
3. AI reads `docs/workstreams/INDEX.md` to avoid duplicates
4. AI generates workstreams (L4) in `docs/workstreams/backlog/`

**Using /build:**
1. AI reads workstream file (L4)
2. AI reads L1/L2/L3 for context
3. AI executes workstream according to plan
4. AI moves WS to `docs/workstreams/completed/`

**Using /review:**
1. AI reads all completed WS for feature
2. AI checks quality gates
3. AI generates review report

### Product vs Architecture Hierarchy

**Product (feature planning):**
```
VISION.md → RELEASE_PLAN.md → Feature (F) → Workstream (WS)
```

**Architecture (code/documentation structure):**
```
L1 (System) → L2 (Domain) → L3 (Component) → L4 (Workstream)
```

**Intersection:**
- Feature F24 → creates/modifies L2 (content domain)
- Workstream WS-140 → creates L3 (vault component)

---

## Core Principles

All work must follow these principles. See [docs/PRINCIPLES.md](docs/PRINCIPLES.md) for details.

| Principle | Summary |
|-----------|---------|
| **SOLID** | SRP, OCP, LSP, ISP, DIP |
| **DRY** | Don't Repeat Yourself |
| **KISS** | Keep It Simple, Stupid |
| **YAGNI** | You Ain't Gonna Need It |
| **TDD** | Tests first (Red → Green → Refactor) |
| **Clean Code** | Readable, maintainable, testable |
| **Clean Architecture** | Dependencies point inward |

---

## Project Conventions

**Every project must define:**

`PROJECT_CONVENTIONS.md` — Project-specific DO/DON'T rules

**Sections:**
- Language & Communication
- Code Style (formatters, linters)
- Architecture (layer boundaries)
- Naming Conventions
- Testing (coverage, mocking)
- Error Handling
- Git Workflow
- Documentation
- Security
- Performance
- Project-Specific DO/DON'T

See `templates/PROJECT_CONVENTIONS.md` for template.

---

## Quick Reference

```bash
# AI-Readiness check
find src -name "*.py" -exec wc -l {} + | awk '$1 > 200'
ruff check src --select=C901
mypy src --strict

# Clean Architecture check
grep -r "from infrastructure" domain/ application/

# Error handling check
grep -rn "except:" src/
grep -rn "except Exception" src/ | grep -v "exc_info"

# Test coverage (≥80%)
pytest tests/unit/test_module.py -v \
  --cov=src/module \
  --cov-report=term-missing \
  --cov-fail-under=80

# Regression (all tests)
pytest tests/

# TODO/Later check
grep -rn "TODO\|FIXME" src/ --include="*.py" | grep -v "# NOTE"

# Full test suite with coverage
pytest --cov=src --cov-report=term-missing
```

---

## Observability

### Telegram Notifications

Automated notifications for critical events:

```bash
# Setup
export TELEGRAM_BOT_TOKEN="..."
export TELEGRAM_CHAT_ID="..."

# Events: oneshot_started, oneshot_completed, oneshot_blocked,
#         ws_failed, review_failed, breaking_changes, e2e_failed,
#         deploy_success, hotfix_deployed
```

See: `notifications/TELEGRAM.md`

### Audit Log

Centralized logging of all workflow events:

```bash
# Configuration
export AUDIT_LOG_FILE="/var/log/sdp-audit.log"

# Format: ISO8601|EVENT_TYPE|USER|GIT_BRANCH|EVENT_DATA
# Example:
# 2026-01-11T00:30:15+03:00|WS_START|user|feature/lms|ws=WS-060-01

# Query
grep "feature=F60" /var/log/sdp-audit.log
grep "WS_FAILED" /var/log/sdp-audit.log
```

See: `notifications/AUDIT_LOG.md`

### Breaking Changes Detection

Automatic detection and documentation:

```bash
# Runs in pre-commit hook
python scripts/detect_breaking_changes.py --staged

# Generates:
# - BREAKING_CHANGES.md
# - MIGRATION_GUIDE.md (template)
```

---

## Git Hooks

Automatic validation via hooks (see `hooks/`):

| Hook | Purpose |
|------|---------|
| `pre-commit.sh` | Linting, tests, no secrets |
| `commit-msg.sh` | Conventional commit format |
| `pre-build.sh` | WS exists, dependencies satisfied |
| `post-build.sh` | Tests pass, coverage ≥80%, no TODO |
| `pre-deploy.sh` | All tests pass, UAT signed-off |
| `post-oneshot.sh` | Session quality, checkpoint saved |

Install: `python scripts/init.py` (interactive setup)

---

## Resources

| Resource | Purpose |
|----------|---------|
| [README.md](README.md) | Quick start and overview |
| [CLAUDE.md](CLAUDE.md) | Claude Code integration |
| [docs/guides/CURSOR.md](docs/guides/CURSOR.md) | Cursor IDE integration |
| [docs/guides/CLAUDE_CODE.md](docs/guides/CLAUDE_CODE.md) | Claude Code detailed guide |
| [docs/PRINCIPLES.md](docs/PRINCIPLES.md) | SOLID, DRY, KISS, YAGNI, Clean Code |
| [docs/concepts/](docs/concepts/README.md) | Clean Architecture, Artifacts, Roles |
| [CODE_PATTERNS.md](CODE_PATTERNS.md) | Implementation patterns |
| [MODELS.md](MODELS.md) | AI model recommendations |
| [RULES_COMMON.md](RULES_COMMON.md) | Common rules for all work |
| [PROJECT_CONVENTIONS.md](PROJECT_CONVENTIONS.md) | Project-specific DO/DON'T (fill this!) |
| [prompts/commands/](prompts/commands/) | Slash command instructions |
| [templates/](templates/) | Document templates |

---

**Version:** 0.3.0  
**Last Updated:** 2026-01-12  
**Status:** Active
