# Phase 2: Plan

## Mission

Take one Workstream from the map and create a detailed plan for one-shot execution.

## Input

- Workstream map from Phase 1
- Instruction: which WS to plan
- **Documentation hierarchy (for context):**
  - L1: `docs/SYSTEM_OVERVIEW.md`
  - L2: `docs/domains/{domain}/DOMAIN_MAP.md`
  - L3: `docs/domains/{domain}/components/{comp}/SPEC.md`
  - L4: `docs/workstreams/INDEX.md`
- Feature specs: `docs/specs/feature_XX/feature.md`

## Pre-Flight Checks

**REQUIRED before planning:**

### 1. Check for Duplicates

```bash
# Read INDEX
cat docs/workstreams/INDEX.md

# Check: does WS-{ID} already exist?
# - If in backlog/ → can plan
# - If in active/ or completed/ → STOP
# Clarify with human: supplement existing or create new
```

### 2. Check Dependencies + Clarify Requirements

**Dependencies:**
- All dependent WS completed? (status in INDEX)
- Input files exist? (use `ls` to verify)

**Clarifying Requirements (CRITICAL):**

Before planning, ASK user if:
- **Goal unclear:** "What exactly should work after WS?"
- **Acceptance Criteria vague:** "How to verify task is complete?"
- **Multiple implementation options:** "Use pattern X or Y?"
- **Architecture decision not obvious:** "Create new component or extend existing?"
- **Scope too large:** "Split into 3 parts or do minimal MVP first?"

**Question format:**
```markdown
### Clarification for WS-{ID}

**Context:** [what I understood from specification]

**Questions:**
1. [Specific question 1]
2. [Specific question 2]

**Options (if applicable):**
- Option A: [description + pros/cons]
- Option B: [description + pros/cons]

**My recommendation:** [if there's a preferred option]
```

**Better to ask BEFORE starting than redo AFTER.**

### 3. Check Scope

- Estimate approximate task size (see "Scope Estimate" below)
- If task > MEDIUM → **MUST split** (see below)

### 4. If Need to Split WS

**CRITICAL: cannot reference non-existent WS!**

#### Substream Numbering Format (STRICT)

```
WS-{PARENT}-{SEQ}

- PARENT = 3 digits (050)
- SEQ = 2 digits (01, 02, ... 99)

Example: WS-050 → WS-050-01, WS-050-02, WS-050-03
```

**Correct:** `WS-050-01`, `WS-050-02`, `WS-050-10`, `WS-050-15`
**Wrong:** `WS-050-1` (need 01), `WS-050-A`, `WS-050-part1`, `WS-24-1`, `24.1`

If scope > MEDIUM, you MUST:

1. **FIRST create ALL substream files** in `workstreams/backlog/`:
   ```bash
   # Create ALL files IMMEDIATELY, then fill
   touch docs/workstreams/backlog/WS-050-01-domain-entities.md
   touch docs/workstreams/backlog/WS-050-02-application-layer.md
   touch docs/workstreams/backlog/WS-050-03-infrastructure.md
   ```

2. **THEN fill EACH substream completely** (not stub, not "TODO"):
   - Goal + Acceptance Criteria
   - Context, Dependencies, Input files
   - Steps (atomic)
   - Code (copy-paste ready)
   - Scope Estimate
   - Completion criteria (bash)

3. **Update INDEX.md** with new WS

4. **VERIFY files exist:**
   ```bash
   # Required check before completion!
   ls -la docs/workstreams/backlog/WS-050-*.md
   # Should show ALL substream files
   ```

#### FORBIDDEN

- "This will be in WS-050-02" (without creating file `WS-050-02-*.md`)
- Empty stubs or placeholders
- "Details in next WS"
- Format `24.1`, `WS-24-1`, `WS-050-part1`
- Partial completion ("rest later")
- Time estimates ("0.5 days", "3 days")

## Output

Detailed WS plan — ready prompt for executor (Cursor Agent / Claude Code).

---

## Plan Format

```markdown
## WS-{ID}: {Title}

### Goal
**What should WORK after WS completion:**
- [Specific functionality — what user/system can do]
- [Measurable outcome — how to verify]

**Acceptance Criteria:**
- [ ] [Verifiable condition 1 — what works]
- [ ] [Verifiable condition 2]
- [ ] [Verifiable condition 3]

**Rule:** WS NOT complete until Goal achieved (all AC ✅).

---

### Context
[Why this task is needed, current state, problem]

### Dependency
[WS-XX completed / Independent]

### Input Files
- `path/to/file1.py` — what's in it, why read
- `path/to/file2.py` — what's in it

### Steps
1. [Atomic action with exact path]
2. [Next action]
...

### Code
```python
# Exact code to insert/create
# Full type hints, docstrings
```

### Expected Result
- [Specific measurable outcome]
- [File structure if creating new files]

### Scope Estimate
- Files: ~N created + ~M modified = ~X total
- Lines of code: ~N (new: ~X, changes: ~Y)
- Tests: ~N files, ~X lines
- Context tokens: ~N (files × 500)

**Size assessment:** SMALL / MEDIUM / LARGE
- **SMALL**: < 500 lines of code, < 1500 tokens
- **MEDIUM**: 500-1500 lines, 1500-5000 tokens
- **LARGE**: > 1500 lines → **SPLIT INTO 2+ WS**

### Completion Criteria
```bash
# Verification commands
pytest tests/... -x

# Coverage ≥ 80% for changed/created files
pytest tests/unit/test_XXX.py -v \
  --cov=src/module \
  --cov-report=term-missing \
  --cov-fail-under=80

# Regression check (fast tests)
pytest tests/unit/ -m fast -v

# Code quality
ruff check path/to/...

# Type checking (strict)
mypy src/module/ --strict --no-implicit-optional

# Import check
python -c "from module import Class"
```

### Constraints
- DO NOT: [what executor should not do]
- DO NOT CHANGE: [what not to touch]
```

---

## Generation Rules

### Atomicity
- "Refactor module"
- "Create file `application/cleanup/states.py` with enum `CleanupState`"

### Exact Paths
- "In validators directory"
- "`src/application/validators/protocol.py`"

### Code Instead of Descriptions
- "Create dataclass for configuration"
- See `CODE_PATTERNS.md` → copy ready structures

### Full Signatures
- "Method execute"
- Full signature with type hints (see examples in CODE_PATTERNS.md)

### Verifiable Criteria
- "Code works"
- See `CODE_PATTERNS.md` → bash commands for verification

---

## Checklist Before Delivering Plan

### Required Checks

- [ ] **WS-{ID} doesn't exist** in INDEX (checked: backlog/active/completed)
- [ ] **Dependencies available** (all dependent WS completed)
- [ ] **Scope estimated**, not exceeding MEDIUM (otherwise split)
- [ ] **Goal + Acceptance Criteria** explicitly defined
- [ ] Each step — one action
- [ ] All paths from project root (`src/...`)
- [ ] Code ready for copy-paste
- [ ] Type hints everywhere
- [ ] Completion criteria — bash commands (including coverage + regression)
- [ ] Constraints explicitly stated
- [ ] No decisions left to executor

### FORBIDDEN (verify NOT present)

- [ ] **NO time mentions** (hours/days/weeks)
- [ ] **NO tech debt** (no "do later", "temporary solution", "tech debt")
- [ ] **NO references to non-existent WS**

### If Split into Substreams

```bash
# REQUIRED CHECK: all substream files exist
ls -la docs/workstreams/backlog/WS-{PARENT}-*.md

# Example for WS-050:
ls docs/workstreams/backlog/WS-050-01-*.md  # must exist
ls docs/workstreams/backlog/WS-050-02-*.md  # must exist
ls docs/workstreams/backlog/WS-050-03-*.md  # must exist

# Check numbering format (2 digits for SEQ)
ls docs/workstreams/backlog/ | grep -E "WS-[0-9]{3}-[0-9]{2}-"
# Should be WS-050-01-*, WS-050-02-*, NOT WS-050-1-*
```

**If `ls` shows "No such file" → FIRST create file, then reference!**
