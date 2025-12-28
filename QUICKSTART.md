# Quickstart Guide

Get your first consensus workflow running in 10 minutes.

## 1. Setup (2 min)

```bash
# Clone the repository
git clone https://github.com/your-org/consensus.git
cd consensus

# Create your first epic
mkdir -p docs/specs/epic_01_hello_world/consensus/{artifacts,messages/inbox/{analyst,architect,tech_lead,developer,qa,devops},decision_log}
```

## 2. Define Your Epic (2 min)

Create `docs/specs/epic_01_hello_world/epic.md`:

```markdown
## Summary
Add a "Hello World" API endpoint to the application.

## Goals
- Create GET /api/hello endpoint
- Return JSON: {"message": "Hello, World!"}
- Add unit tests with ≥80% coverage

## Non-Goals
- Authentication
- Internationalization
- Caching

## Success Metrics
- Endpoint responds in <100ms
- All tests pass
- No lint errors
```

## 3. Run Analyst (2 min)

Using Claude Code:
```bash
claude --model claude-opus-4-5-20251101 \
       --system-prompt prompts/analyst_prompt.md \
       "Analyze docs/specs/epic_01_hello_world/epic.md and create requirements"
```

Or using Cursor:
```
@prompts/analyst_prompt.md
@docs/specs/epic_01_hello_world/epic.md

Create requirements for this epic.
```

**Expected output:**
- `docs/specs/epic_01_hello_world/consensus/artifacts/requirements.json`
- Message in `consensus/messages/inbox/architect/`

## 4. Run Architect (2 min)

```bash
claude --model claude-opus-4-5-20251101 \
       --system-prompt prompts/architect_prompt.md \
       "Review requirements for epic_01_hello_world and create architecture"
```

**Expected output:**
- `docs/specs/epic_01_hello_world/consensus/artifacts/architecture.json`
- Message in `consensus/messages/inbox/tech_lead/`

**Check for vetoes:**
```bash
grep -r '"st": "veto"' docs/specs/epic_01_hello_world/consensus/messages/
```

## 5. Continue the Flow (2 min)

Run remaining agents in sequence:

```bash
# Tech Lead → creates implementation plan
claude --system-prompt prompts/tech_lead_prompt.md "Create plan for epic_01_hello_world"

# Developer → implements with TDD
claude --system-prompt prompts/developer_prompt.md "Implement epic_01_hello_world"

# QA → verifies
claude --system-prompt prompts/qa_prompt.md "Verify epic_01_hello_world"

# DevOps → deployment
claude --system-prompt prompts/devops_prompt.md "Create deployment for epic_01_hello_world"
```

## What's Next?

### Understand the Protocol
Read these files:
- `PROTOCOL.md` - Full consensus protocol
- `RULES_COMMON.md` - Rules all agents follow
- `MODELS.md` - Model selection guide

### See a Full Example
Check `docs/examples/sample_epic/` for a complete worked example.

### Integration Guides
- `docs/guides/CLAUDE_CODE.md` - Claude Code CLI
- `docs/guides/CURSOR.md` - Cursor IDE

### Customize for Your Project
1. Modify prompts in `prompts/` for your domain
2. Add project-specific rules to `.cursorrules` or `CLAUDE.md`
3. Create custom roles if needed

## Quick Reference

### Directory Structure
```
docs/specs/epic_XX/
├── epic.md                 # Epic definition
├── architecture.md         # Architecture docs
├── implementation.md       # Implementation plan
├── testing.md              # Testing strategy
├── deployment.md           # Deployment plan
└── consensus/
    ├── artifacts/          # Agent outputs (JSON)
    ├── messages/inbox/     # Agent communication
    │   ├── analyst/
    │   ├── architect/
    │   ├── tech_lead/
    │   ├── developer/
    │   ├── qa/
    │   └── devops/
    └── decision_log/       # Decision history (MD)
```

### Message Format
```json
{
  "d": "2025-12-27",
  "st": "request",
  "r": "analyst",
  "epic": "EP01",
  "sm": ["Requirements ready"],
  "nx": ["Review architecture"],
  "artifacts": ["consensus/artifacts/requirements.json"]
}
```

### Agent Sequence
```
1. Analyst    → requirements.json
2. Architect  → architecture.json (may VETO)
3. Tech Lead  → implementation.md, testing.md, deployment.md
4. Developer  → code + tests (incremental review)
5. QA         → test_results.md
6. DevOps     → deployment complete
```

### Veto Rules (Cannot Override)
- Architecture violations (architect)
- Security issues (security)
- Missing rollback plan (devops)
- Code review violations (tech_lead, qa)

---

**Problems?** Check `USER_GUIDE.md` for detailed troubleshooting.
