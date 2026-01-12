# Spec Driven Development v0.3.0

Workstream-driven development for AI agents.

---

## Navigation

```
Need to...                            →  Go to
─────────────────────────────────────────────────────
Understand what to do                 →  Phase 1: Analyze
Plan a workstream                     →  Phase 2: Plan
Execute a workstream                  →  Phase 3: Execute
Verify the result                     →  Phase 4: Review
Make an architectural decision        →  ADR Template
See code patterns                     →  CODE_PATTERNS.md
Check the rules                       →  Guardrails
Understand principles                 →  docs/PRINCIPLES.md
```

---

## Workstream Flow

```
┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐
│  ANALYZE   │───→│    PLAN    │───→│  EXECUTE   │───→│   REVIEW   │
│  (Phase 1) │    │  (Phase 2) │    │  (Phase 3) │    │  (Phase 4) │
└────────────┘    └────────────┘    └────────────┘    └────────────┘
     │                  │                  │                  │
     ▼                  ▼                  ▼                  ▼
  WS Map           WS Plan              Code            APPROVED/FIX
```


---

## Terminology

| Term | Scope | Size | Example |
|------|-------|------|---------|
| **Release** | Product milestone | 10-30 Features | R1: MVP |
| **Feature** | Large capability | 5-30 Workstreams | F1: User Auth |
| **Workstream** | Atomic task | SMALL/MEDIUM/LARGE | WS-001: Domain entities |

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
VISION.md (product)
    ↓
RELEASE_PLAN.md (releases)
    ↓
Feature (F01-F99) — large features
    ↓
Workstream (WS-001-WS-999) — atomic tasks
```

### Deprecated Terms

- ~~Epic (EP)~~ → **Feature (F)** (since 2026-01-07)
- ~~Sprint~~ → not used

---

## Guardrails

### AI-Readiness (BLOCKING)

| Rule | Threshold | Check |
|------|-----------|-------|
| File size | < 200 LOC | `wc -l` |
| Complexity | CC < 10 | `ruff --select=C901` |
| Type hints | 100% public | Visual |
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

### Gate 1: Analyze → Plan
- [ ] WS map formed
- [ ] Dependencies identified
- [ ] AI-Readiness estimated for each WS

### Gate 2: Plan → Execute
- [ ] **WS does not exist** in INDEX (verified)
- [ ] **Scope estimated**, not exceeding MEDIUM
- [ ] All file paths specified
- [ ] Code ready for copy-paste
- [ ] Completion criteria include: tests + coverage + regression
- [ ] Constraints explicit
- [ ] **NO time estimates** (hours/days)

### Gate 3: Execute → Review
- [ ] All steps completed
- [ ] Completion criteria passed
- [ ] **Coverage ≥ 80%** for changed files
- [ ] **Regression passed** (fast tests)
- [ ] **No TODO/Later** in code
- [ ] Report generated

### Gate 4: Review → Done
- [ ] AI-Readiness: ✅
- [ ] Clean Architecture: ✅
- [ ] Error Handling: ✅
- [ ] Tests & Coverage: ✅ (≥80%)
- [ ] Regression: ✅ (all fast tests)
- [ ] Review recorded **at the end of WS file** (not separate file)

### Gate 5: Done → Deploy (Human UAT)

**UAT (User Acceptance Testing)** — human verification before deploy:

| Step | Description | Time |
|------|-------------|------|
| 1 | Quick Smoke Test | 30 sec |
| 2 | Detailed Scenarios (happy path + errors) | 5-10 min |
| 3 | Red Flags Check | 2 min |
| 4 | Sign-off | 1 min |

**UAT Guide created automatically** after `/review APPROVED`:
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

**If scope exceeded during Execute:**
→ STOP, return to Phase 2 to split into WS-XXX-01, WS-XXX-02

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

**After each WS:**

```bash
# All fast tests MUST pass
pytest tests/unit/ -m fast -v
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

**The Tech Debt concept is FORBIDDEN in this project.**

- "This is tech debt, we'll do it later"
- "Temporary solution, will return later"
- "Dirty code but it works"
- "Postpone refactoring"

✅ **Rule: fix all issues immediately.**

**If code doesn't meet standards:**
1. Fix in current WS
2. If scope exceeded → split into WS (see below)
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

1. **Create ALL substream files** in `workstreams/backlog/`:
   ```
   WS-050-01-domain-entities.md
   WS-050-02-application-layer.md
   WS-050-03-infrastructure.md
   ```

2. **Fill each substream** completely (not stub):
   - Context
   - Dependencies (WS-XXX-01 → WS-XXX-02 → ...)
   - Input files
   - Steps
   - Code
   - Completion criteria

3. **Update INDEX.md** with new WS

4. **Delete or mark parent WS** as "Split → WS-XXX-01, WS-XXX-02"

### FORBIDDEN:

- Referencing non-existent WS ("see WS-050-02" without creating file)
- Leaving empty stubs ("TODO: fill in")
- Splitting without creating files
- Partial execution ("did part, rest in another WS")
- Formats: `24.1`, `WS-24-1`, `WS-050-1`, `WS-050-part1`
- Time estimates: "0.5 days", "3 days" — only LOC/tokens
- Creating separate `-ANALYSIS.md` files (analysis → directly into WS files)

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

```markdown
## WS-{ID}: {Title}

### Context
[Why needed]

### Dependency
[WS-XX / Independent]

### Input Files
- `path/to/file.py` — what's there

### Steps
1. [Atomic action]
2. ...

### Code
```python
# Ready code
```

### Expected Result
- [What should happen]

### Completion Criteria
```bash
pytest ...
ruff check ...
```

### Constraints
- DO NOT: ...
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

L4: Workstream  docs/workstreams/WS-XXX.md
    ↓ Specific task for execution
```

### Navigation Flow

**Phase 1 (Analyze):**
1. Read L1 (`SYSTEM_OVERVIEW.md`) for general context
2. Choose relevant domain, read L2 (`domains/{domain}/DOMAIN_MAP.md`)
3. If touching component, read L3 (component SPEC)
4. Generate L4 (workstream map)

**Phase 2 (Plan):**
1. Read L4 (`workstreams/INDEX.md`) — check for duplicates
2. Read L1/L2/L3 for context of specific WS
3. Create detailed WS plan

**Phase 3 (Execute):**
1. Work according to WS plan (L4)

**Phase 4 (Review):**
1. Check code quality
2. If WS changed domain boundaries → update L2
3. If WS changed component → update L3

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

## Quick Reference

```bash
# AI-Readiness check
find src -name "*.py" -exec wc -l {} + | awk '$1 > 200'
ruff check src --select=C901

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

# Regression (fast tests)
pytest tests/unit/ -m fast -v

# TODO/Later check
grep -rn "TODO\|FIXME" src/ --include="*.py" | grep -v "# NOTE"

# Full test suite
pytest -m fast -x --tb=short
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

## Resources

| Resource | Purpose |
|----------|---------|
| [docs/PRINCIPLES.md](docs/PRINCIPLES.md) | SOLID, DRY, KISS, YAGNI, Clean Code |
| [docs/concepts/](docs/concepts/README.md) | Clean Architecture, Artifacts, Roles |
| [CODE_PATTERNS.md](CODE_PATTERNS.md) | Implementation patterns |
| [RULES_COMMON.md](RULES_COMMON.md) | Common rules for all work |
| [prompts/structured/](prompts/structured/) | Phase 1-4 prompts |

---

**Version:** 0.3.0
**Last Updated:** 2026-01-12
