# Development Workflow

This document describes how we develop the Consensus Workflow framework using the framework itself (dogfooding).

## Process Overview

```
1. GitHub Issue → 2. Local Epic → 3. Consensus Workflow → 4. Commit Artifacts
   (planning)       (work)          (AI agents)            (completed)
```

## Step 1: Create GitHub Issue

For each new epic, create a GitHub issue using the Epic template:

```bash
# On GitHub: Issues → New Issue → Epic template
```

The issue serves as:
- Public tracking and discussion
- Planning and scoping
- Progress updates
- Link to final artifacts

## Step 2: Work Locally

Create epic directory locally (gitignored during development):

```bash
# Create epic structure
mkdir -p docs/specs/epic_XX_name/consensus/{artifacts,decision_log,messages/inbox/{analyst,architect,tech_lead,developer,qa,devops}}

# Copy issue description to epic.md
vim docs/specs/epic_XX_name/epic.md
```

**Note:** `docs/specs/epic_*/` is in `.gitignore` - work stays local until completion.

## Step 3: Follow Consensus Workflow

Run agents following the protocol:

### Phase 1: Requirements (Analyst)
```bash
claude --provider anthropic \
       --model claude-opus-4-5-20251101 \
       --system-prompt prompts/analyst_prompt.md \
       "@docs/specs/epic_XX_name/epic.md Analyze and create requirements.json"

# Save to: consensus/artifacts/requirements.json
# Document decisions in: consensus/decision_log/
```

### Phase 2: Architecture (Architect)
```bash
claude --provider anthropic \
       --model claude-opus-4-5-20251101 \
       --system-prompt prompts/architect_prompt.md \
       "@consensus/artifacts/requirements.json Design architecture"

# Save to: consensus/artifacts/architecture.json
# Check for veto! If architect vetoes, go back to analyst
```

### Phase 3: Planning (Tech Lead)
```bash
claude --provider google \
       --model gemini-3.0-flash \
       --system-prompt prompts/tech_lead_prompt.md \
       "@consensus/artifacts/architecture.json Create implementation plan"

# Save to: implementation.md
```

### Phase 4: Implementation (Developer)
```bash
claude --provider google \
       --model gemini-3.0-flash \
       --system-prompt prompts/developer_prompt.md \
       "Implement workstream X with TDD"

# Write code + tests
# Send message to QA inbox when ready
```

### Phase 5: Quality Assurance (QA)
```bash
claude --provider google \
       --model gemini-3.0-flash \
       --system-prompt prompts/qa_prompt.md \
       "@consensus/messages/inbox/qa/* Review and test"

# Run tests, verify coverage
# Save to: testing.md
```

### Phase 6: Deployment (DevOps, if applicable)
```bash
claude --provider ollama \
       --model qwen2.5-coder:32b \
       --system-prompt prompts/devops_prompt.md \
       "Create deployment configuration"

# Save to: deployment.md
```

## Step 4: Commit Completed Artifacts

When epic is complete and tested:

```bash
# Stage epic artifacts
git add docs/specs/epic_XX_name/

# Commit with detailed message
git commit -m "feat(epic XX): [title]

[Description of what was built]

Consensus artifacts:
- requirements.json (Analyst)
- architecture.json (Architect)
- implementation.md (Tech Lead)
- [code files] (Developer)
- testing.md (QA)
- deployment.md (DevOps)

Models used:
- Strategic: Claude Opus 4.5
- Implementation: Gemini 3 Flash
- Automation: Qwen3-Coder

Lessons learned: [key insights]"

# Push to remote
git push

# Close GitHub issue with link to artifacts
```

## Benefits of This Approach

✅ **Private iteration**: Work locally without exposing incomplete work
✅ **Public tracking**: GitHub issues for transparency and discussion
✅ **Clean history**: Only completed artifacts in repo
✅ **Reference examples**: Users see finished epics, not WIP
✅ **Flexibility**: Can abandon epics without polluting repo

## What Gets Committed

### ✅ Always Commit:
- Completed `epic.md` with final scope
- All consensus artifacts (JSON files)
- All decision logs explaining choices
- Final implementation (code, tests, docs)
- Lessons learned document

### ❌ Never Commit:
- Work-in-progress iterations
- Failed experiments
- Draft messages
- API keys or secrets

## Tracking Metrics

In each epic's final decision log, document:

```markdown
## Metrics (Approximate)

### Models Used
- Analyst: Claude Opus 4.5 (~X input, ~Y output tokens)
- Architect: Claude Opus 4.5 (~X input, ~Y output tokens)
- [etc]

(Token counts from actual API responses, not fabricated)

### What Worked
- [Specific successes]

### What Didn't Work
- [Specific failures]
- [Prompt issues]

### Lessons Learned
- [Framework improvements identified]
- [Protocol clarifications needed]
```

## Example Epic Flow

```
Day 1:
  - Create GitHub issue #42: "Epic 01: Protocol Validation CLI"
  - Create local epic_01_validation_cli/ directory
  - Run Analyst → requirements.json
  - Run Architect → architecture.json (approved)

Day 2:
  - Run Tech Lead → implementation.md
  - Run Developer → implement CLI with tests
  - Run QA → verify tests pass

Day 3:
  - Run DevOps → package for distribution
  - Document lessons learned
  - Commit all artifacts to repo
  - Close issue #42 with link to docs/specs/epic_01_validation_cli/
```

## Tips

- **Use decision logs**: Document why you made choices, not just what you built
- **Track problems**: If prompts fail, document it - this improves the framework
- **Be honest**: Don't hide failures or fabricate metrics
- **Update framework**: If you find protocol issues, fix them based on real experience

## Questions?

See [CONTRIBUTING.md](CONTRIBUTING.md) or open a discussion on GitHub.
