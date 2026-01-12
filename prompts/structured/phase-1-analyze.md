# Phase 1: Analyze

## Mission

Read project specifications and form a Workstream map with dependencies.

## Input

- **Documentation hierarchy** (read before analysis):
  - **L1 (System):** `docs/SYSTEM_OVERVIEW.md` — general context
  - **L2 (Domain):** `docs/domains/{domain}/DOMAIN_MAP.md` — domain structure
  - **L3 (Component):** `docs/domains/{domain}/components/{comp}/SPEC.md` — component specs
  - **L4 (Workstream):** `docs/workstreams/INDEX.md` — current WS
- **Product specifications:**
  - `docs/specs/VISION.md` — product strategy
  - `docs/specs/RELEASE_PLAN.md` — release plan
  - `docs/specs/FEATURE_INDEX.md` — features (F01-F99)
  - `docs/specs/feature_XX/feature.md` — specific feature details
- User instruction: which area/feature to analyze

## Output

**DO NOT create separate analysis files (like `WS-XXX-ANALYSIS.md`)!**

Analysis result → **directly into workstream files** in `workstreams/backlog/`:

```
workstreams/backlog/
├── WS-050-feature-name.md        ← if scope ≤ MEDIUM
├── WS-051-01-domain-layer.md     ← if scope > MEDIUM, split into substreams
├── WS-051-02-application-layer.md
└── WS-051-03-infrastructure.md
```

**Format for each WS file** (per TEMPLATE.md):

```markdown
## WS-{ID}: {Title}

### Goal
**What should WORK after WS completion:**
- [Specific functionality]

**Acceptance Criteria:**
- [ ] [Verifiable condition 1]
- [ ] [Verifiable condition 2]

### Context
[Why needed, current state]

### Dependency
[WS-XX / Independent]

### Input Files
- `path/to/file.py` — what's there

### Steps
1. [Atomic action]
2. ...

### Scope Estimate
- Files: ~N
- Lines: ~N (SMALL/MEDIUM/LARGE)
- Tokens: ~N

### Completion Criteria
```bash
pytest tests/... -v
```
```

**Update INDEX.md** with new WS.

---

### Dependency Graph (in INDEX.md or separate section)

```
WS-050 ──→ WS-052
WS-051-01 ──→ WS-051-02 ──→ WS-051-03

WS-053 (independent)
```

### Priorities
1. **Tier 1 (critical):** WS-050, WS-051-01
2. **Tier 2 (important):** WS-051-02, WS-052
3. **Tier 3 (improvements):** WS-053

---

## How to Form Workstreams

### Analysis Order

1. **L1 (System):** Read `SYSTEM_OVERVIEW.md` for general context
2. **L2 (Domain):** Identify relevant domain, read `domains/{domain}/DOMAIN_MAP.md`
3. **L3 (Component):** If WS touches specific component, read its SPEC
4. **L4 (Workstream):** Check `workstreams/INDEX.md` for duplicates
5. **Product:** Read `feature_XX/feature.md` for feature requirements

### WS Size
- **One-shot executable** — small model (Haiku/Flash) should handle in one pass
- **Scope metrics:**
  - **SMALL**: < 500 lines of code, < 1500 tokens
  - **MEDIUM**: 500-1500 lines, 1500-5000 tokens
  - **LARGE**: > 1500 lines → **SPLIT** into multiple WS
- **Atomic result** — completion verifiable by bash command

### AI-Readiness Criteria
WS is AI-Ready if:
- [ ] Affected files < 200 lines (or will be after refactoring)
- [ ] No complex dependencies between files
- [ ] Clear inputs and outputs
- [ ] Completion criteria can be a bash command
- [ ] Coverage ≥ 80% achievable for changed files

### Decomposing Large Tasks
If task is too large (> MEDIUM):
1. **Structure** — create files/directories, protocols, dataclasses
2. **Logic** — implement in parts (commands, steps)
3. **Integration** — orchestrator, update existing code
4. **Cleanup** — remove old code, update imports

### Dependencies
- **Hard:** WS-02 uses code from WS-01
- **Soft:** WS-02 can be done in parallel, but better after WS-01
- **Independent:** Can be done in any order

---

## Checklist Before Completing Phase 1

### Files Created (REQUIRED)

```bash
# Verify ALL WS files exist
ls docs/workstreams/backlog/WS-*.md

# If split into substreams — ALL files must exist
# Example: WS-050 split into 3 parts
ls docs/workstreams/backlog/WS-050-01-*.md
ls docs/workstreams/backlog/WS-050-02-*.md
ls docs/workstreams/backlog/WS-050-03-*.md
```

### INDEX Updated

```bash
# All new WS added to INDEX
grep "WS-050" docs/workstreams/INDEX.md
```

### WS Quality

- [ ] Each WS — one-shot executable (scope ≤ MEDIUM)
- [ ] Dependencies explicitly stated
- [ ] AI-Readiness evaluated
- [ ] Completion criteria — bash commands
- [ ] Priorities set
- [ ] **NO time estimates** (days/hours/weeks) — only scope (LOC, tokens)
- [ ] **NO separate -ANALYSIS.md files** — everything directly in WS files

### FORBIDDEN

- Creating `WS-XXX-ANALYSIS.md` (analysis goes directly to WS files)
- Referencing `WS-XXX-01` without creating file `WS-XXX-01-*.md`
- Estimates in days/hours ("0.5 days", "3 days")
- Leaving scope > MEDIUM without splitting
