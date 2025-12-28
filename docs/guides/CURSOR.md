# Cursor IDE Integration Guide

This guide explains how to use the Consensus Workflow with [Cursor](https://cursor.sh) IDE.

## Prerequisites

1. **Cursor IDE installed** (v0.40+)
2. **Repository opened** in Cursor
3. **API keys configured** in Cursor Settings

## Quick Start

### Method 1: Chat with Prompt File

1. Open Cursor Chat (Cmd/Ctrl + L)
2. Reference the prompt file:
   ```
   @prompts/analyst_prompt.md

   Analyze docs/specs/epic_XX/epic.md and create requirements
   ```

### Method 2: Cursor Rules

Create `.cursorrules` or `.cursor/rules/consensus.mdc`:

```markdown
# Consensus Protocol Rules

You are an agent in the Cursor Consensus Workflow. Follow these rules:

## Core Rules
- ALL messages MUST be in English
- Read ONLY from your own inbox
- Write ONLY to other agents' inboxes
- Follow Clean Architecture boundaries

## Message Format
Use JSON with compact keys:
- d: date (YYYY-MM-DD)
- st: status (request|response|veto|approval|handoff)
- r: your role
- epic: epic ID
- sm: summary array
- nx: next actions array
- artifacts: artifact paths array

## Quality Gates
- No silent fallbacks
- No layer violations
- ≥80% test coverage in touched areas
```

## Multi-Window Workflow

The recommended approach uses multiple Cursor windows, one per agent:

### Setup
```bash
# Open 6 windows for core agents
cursor docs/specs/epic_XX/ --new-window  # Analyst
cursor docs/specs/epic_XX/ --new-window  # Architect
cursor docs/specs/epic_XX/ --new-window  # Tech Lead
cursor docs/specs/epic_XX/ --new-window  # Developer
cursor docs/specs/epic_XX/ --new-window  # QA
cursor docs/specs/epic_XX/ --new-window  # DevOps
```

### Window Layout

```
┌─────────────────┬─────────────────┐
│   Analyst       │   Architect     │
│   Window        │   Window        │
├─────────────────┼─────────────────┤
│   Tech Lead     │   Developer     │
│   Window        │   Window        │
├─────────────────┼─────────────────┤
│   QA            │   DevOps        │
│   Window        │   Window        │
└─────────────────┴─────────────────┘
```

## Agent-Specific Instructions

### Running Analyst

In Analyst window chat:
```
@prompts/analyst_prompt.md
@docs/specs/epic_XX/epic.md

You are the Analyst. Create requirements for this epic.
Output:
1. docs/specs/epic_XX/consensus/artifacts/requirements.json
2. Message to architect inbox
3. Decision log entry
```

### Running Architect

In Architect window chat:
```
@prompts/architect_prompt.md
@docs/specs/epic_XX/consensus/artifacts/requirements.json
@docs/specs/epic_XX/consensus/messages/inbox/architect/

You are the Architect. Review requirements and create architecture.
Check inbox for any messages.
VETO if Clean Architecture violations detected.
```

### Running Developer

In Developer window chat:
```
@prompts/developer_prompt.md
@docs/specs/epic_XX/implementation.md
@docs/specs/epic_XX/consensus/messages/inbox/developer/

You are the Developer. Implement the plan with TDD.
Before implementing:
1. Search codebase for existing implementations
2. Write failing tests first
3. After each workstream, conduct code review
```

## Cursor-Specific Features

### Using @-mentions

Cursor's @ mentions work great with consensus:

```
@RULES_COMMON.md         # Reference shared rules
@consensus_architecture.json  # Reference protocol spec
@docs/specs/epic_XX/     # Reference epic directory
```

### Composer Mode

For complex agents, use Composer (Cmd/Ctrl + I):

1. Select relevant files in sidebar
2. Open Composer
3. Paste agent prompt
4. Composer can edit multiple files at once

### Code Actions

Use code actions for implementation:
```
# Select code block, then:
Cmd/Ctrl + K → "Add timeout to this API call"
Cmd/Ctrl + K → "Add error handling per RULES_COMMON.md"
```

## Model Configuration

### In Cursor Settings

1. Open Settings (Cmd/Ctrl + ,)
2. Go to "Cursor Settings" → "Models"
3. Configure per-role:

| Role | Suggested Model |
|------|-----------------|
| Analyst | claude-opus-4 or gpt-4o |
| Architect | claude-opus-4 or gpt-4o |
| Developer | claude-sonnet-4 or gpt-4o-mini |
| QA | claude-sonnet-4 or gpt-4o-mini |

### Per-Chat Model Selection

Use model selector in chat window to switch models mid-conversation.

## Workspace Configuration

### .cursor/settings.json

```json
{
  "chat.defaultModel": "claude-sonnet-4-20250514",
  "chat.contextFiles": [
    "CLAUDE.md",
    "RULES_COMMON.md"
  ],
  "indexing.include": [
    "docs/specs/**",
    "prompts/**"
  ],
  "indexing.exclude": [
    "node_modules",
    ".git"
  ]
}
```

### Custom Rules per Role

Create role-specific rules in `.cursor/rules/`:

```bash
.cursor/
└── rules/
    ├── analyst.mdc
    ├── architect.mdc
    ├── developer.mdc
    └── qa.mdc
```

Example `developer.mdc`:
```markdown
---
description: Developer agent rules
globs: ["src/**", "tests/**"]
---

# Developer Rules

1. TDD: Write failing tests before implementation
2. Functions ≤15 LOC when practical
3. Coverage ≥80%
4. Search codebase before implementing new logic
5. No silent fallbacks (except: pass is forbidden)
```

## Orchestration Workflow

### Phase 1: Requirements & Architecture

```
Window 1 (Analyst):
> @prompts/analyst_prompt.md Analyze epic and create requirements

[Wait for completion]

Window 2 (Architect):
> @prompts/architect_prompt.md Review requirements, check for vetoes
```

### Phase 2: Planning

```
Window 3 (Tech Lead):
> @prompts/tech_lead_prompt.md Create implementation plan
```

### Phase 3: Implementation

```
Window 4 (Developer):
> @prompts/developer_prompt.md Implement workstream 1

[After each workstream]
Window 3 (Tech Lead):
> Review code quality for workstream 1. Approve or veto.
```

### Phase 4: Verification

```
Window 5 (QA):
> @prompts/qa_prompt.md Verify code quality and run tests

Window 6 (DevOps):
> @prompts/devops_prompt.md Create deployment plan
```

## Checking Consensus Status

### Quick Status Check

In any window:
```
Show me the current status of epic_XX:
1. List all artifacts in consensus/artifacts/
2. List all messages in consensus/messages/inbox/
3. Check for any vetoes
4. Show decision log entries
```

### Veto Detection

```bash
# In terminal
find docs/specs/epic_XX/consensus/messages -name "*.json" \
  -exec grep -l '"st": "veto"' {} \;
```

## Tips and Best Practices

### 1. Keep Context Focused

Each agent window should only see relevant files:
- Analyst: epic.md, requirements context
- Developer: implementation.md, source code
- QA: test files, test results

### 2. Use Codebase Search

Before implementing, always:
```
Search the codebase for existing implementations of [feature]
```

### 3. Verify Message Format

Before saving messages:
```
Verify this message follows the JSON format with compact keys:
- d, st, r, epic, sm, nx, artifacts
- All text in English
```

### 4. Incremental Code Review

After each workstream:
```
Conduct code review for the changes in this workstream:
1. DRY violations
2. SOLID violations
3. Clean Architecture violations
4. Missing error handling
5. Missing timeouts on external calls
```

### 5. Use Git for Checkpoints

```bash
# After each agent completes
git add docs/specs/epic_XX/
git commit -m "Consensus: [Agent] completed [phase]"
```

## Troubleshooting

### Agent Not Following Protocol

Try:
1. Explicitly reference `@RULES_COMMON.md`
2. Add protocol rules to `.cursorrules`
3. Use full prompt instead of quick prompt

### Messages in Wrong Language

Add to chat:
```
IMPORTANT: All messages must be in English.
Verify all JSON fields are in English before saving.
```

### Model Not Available

1. Check Cursor Settings → API Keys
2. Verify model name spelling
3. Try fallback model

### Context Too Large

1. Use quick prompts
2. Focus on specific files with @mentions
3. Clear chat history and restart

---

**See also:**
- [CLAUDE_CODE.md](CLAUDE_CODE.md) - Claude Code CLI integration
- [MODELS.md](../../MODELS.md) - Model recommendations
- [QUICKSTART.md](../../QUICKSTART.md) - Quick start guide
