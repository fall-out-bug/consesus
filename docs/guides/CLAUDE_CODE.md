# Claude Code Integration Guide

This guide explains how to use the Consensus Workflow with [Claude Code](https://claude.ai/code) CLI.

## Prerequisites

1. **Claude Code CLI installed:**
   ```bash
   # Via npm
   npm install -g @anthropic-ai/claude-code

   # Or via homebrew
   brew install claude-code
   ```

2. **API key configured:**
   ```bash
   export ANTHROPIC_API_KEY="your-api-key"
   ```

3. **Repository cloned:**
   ```bash
   git clone <your-consensus-repo>
   cd consensus
   ```

## Quick Start

### Running an Agent with a Prompt

```bash
# Full prompt for complex epics
claude --system-prompt prompts/analyst_prompt.md

# Quick prompt for routine tasks
claude --system-prompt prompts/quick/analyst_quick.md
```

### Selecting a Model

```bash
# High tier for Analyst/Architect/Security (see MODELS.md)
claude --model claude-opus-4-5-20251101 --system-prompt prompts/architect_prompt.md

# Medium tier for Tech Lead, complex refactoring
claude --model claude-sonnet-4-5-20250929 --system-prompt prompts/tech_lead_prompt.md

# Standard tier (DEFAULT for 80% of tasks!) - Haiku 4.5
# Developer, QA, DevOps, SRE, Documentation
claude --model claude-haiku-4-5-20241022 --system-prompt prompts/developer_prompt.md
```

**💡 Tip:** Start with Haiku 4.5 for most tasks (73% SWE-bench score, 4-5x faster, 70% cheaper)!

## Workflow Patterns

### Pattern 1: Sequential Agent Execution

Run agents one at a time in separate terminal sessions:

```bash
# Terminal 1: Analyst (High tier)
claude --model claude-opus-4-5-20251101 \
       --system-prompt prompts/analyst_prompt.md \
       "Analyze docs/specs/epic_XX/epic.md and create requirements"

# Terminal 2: Architect (High tier)
claude --model claude-opus-4-5-20251101 \
       --system-prompt prompts/architect_prompt.md \
       "Review requirements and create architecture"

# Terminal 3: Tech Lead (Medium tier)
claude --model claude-sonnet-4-5-20250929 \
       --system-prompt prompts/tech_lead_prompt.md \
       "Create implementation plan"

# Terminal 4: Developer (Standard tier - Haiku 4.5!)
claude --model claude-haiku-4-5-20241022 \
       --system-prompt prompts/quick/developer_quick.md \
       "Implement workstream 1 with TDD"

# Terminal 5: QA (Standard tier - Haiku 4.5!)
claude --model claude-haiku-4-5-20241022 \
       --system-prompt prompts/quick/qa_quick.md \
       "Verify code quality and run tests"
```

### Pattern 2: Using Claude Code in Project Context

When running Claude Code from the repository root, it automatically has access to:
- `CLAUDE.md` (project instructions)
- All prompts and documentation
- The codebase for implementation

```bash
# Run Claude Code with project context
cd /path/to/your/project
claude

# Then instruct it to act as specific agent
> Load the architect prompt from prompts/architect_prompt.md and review the requirements
```

### Pattern 3: Epic-Specific Sessions

Create focused sessions for each epic:

```bash
# Set epic context
export CURRENT_EPIC="epic_02_user_auth"

# Run agent with epic context
claude --system-prompt prompts/developer_prompt.md \
       "Work on ${CURRENT_EPIC}. Read docs/specs/${CURRENT_EPIC}/implementation.md"
```

## Advanced Configuration

### Using CLAUDE.md for Project Instructions

The `CLAUDE.md` file in repository root is automatically loaded by Claude Code. It contains:
- Consensus protocol rules
- Engineering principles
- Quality gates
- Self-verification checklist

Agents will follow these instructions automatically.

### Custom Agent Configuration

Create role-specific configurations in `.claude/`:

```bash
mkdir -p .claude/agents

# Create agent config
cat > .claude/agents/architect.json << 'EOF'
{
  "model": "claude-opus-4-5-20251101",
  "systemPrompt": "prompts/architect_prompt.md",
  "temperature": 0.3,
  "maxTokens": 4096
}
EOF
```

### Hooks for Consensus Protocol

Claude Code supports hooks for automated actions. Create hooks for consensus workflow:

```bash
mkdir -p .claude/hooks

# Hook: Validate English-only messages
cat > .claude/hooks/validate_message.sh << 'EOF'
#!/bin/bash
# Triggered when writing to consensus/messages/
FILE="$1"
if [[ "$FILE" == *"consensus/messages"* ]]; then
  # Check for non-ASCII characters (potential non-English)
  if grep -P '[^\x00-\x7F]' "$FILE" > /dev/null 2>&1; then
    echo "ERROR: Messages must be in English only"
    exit 1
  fi
fi
EOF
chmod +x .claude/hooks/validate_message.sh
```

### MCP Server Integration

For advanced orchestration, you can create an MCP server for consensus:

```python
# mcp_consensus_server.py
from mcp import Server

server = Server("consensus")

@server.tool("read_inbox")
def read_inbox(role: str, epic: str) -> list:
    """Read messages from agent's inbox"""
    import glob
    import json

    inbox_path = f"docs/specs/{epic}/consensus/messages/inbox/{role}/*.json"
    messages = []
    for file in glob.glob(inbox_path):
        with open(file) as f:
            messages.append(json.load(f))
    return messages

@server.tool("send_message")
def send_message(to_role: str, epic: str, message: dict) -> str:
    """Send message to another agent's inbox"""
    import json
    from datetime import date

    filename = f"{date.today()}-{message.get('subject', 'message')}.json"
    path = f"docs/specs/{epic}/consensus/messages/inbox/{to_role}/{filename}"

    with open(path, 'w') as f:
        json.dump(message, f, indent=2)

    return f"Message sent to {to_role}: {path}"

@server.tool("check_vetoes")
def check_vetoes(epic: str) -> list:
    """Check for any vetoes in the current iteration"""
    import glob
    import json

    vetoes = []
    for inbox in glob.glob(f"docs/specs/{epic}/consensus/messages/inbox/*/*.json"):
        with open(inbox) as f:
            msg = json.load(f)
            if msg.get("st") == "veto":
                vetoes.append(msg)
    return vetoes

if __name__ == "__main__":
    server.run()
```

Configure in Claude Code:
```bash
claude mcp add consensus python mcp_consensus_server.py
```

## Multi-Agent Orchestration

### Option 1: Manual Orchestration (Recommended for Learning)

1. Open multiple terminal windows
2. Run each agent in sequence
3. Check for vetoes between agents
4. Iterate as needed

```bash
# Orchestration script (consensus_pipeline.sh)
#!/bin/bash
EPIC=$1

echo "=== Starting Consensus Pipeline for $EPIC ==="

# Phase 1: Requirements (High tier)
echo "[1/6] Running Analyst (Opus 4.5)..."
claude --model claude-opus-4-5-20251101 \
       --system-prompt prompts/analyst_prompt.md \
       "Analyze docs/specs/$EPIC/epic.md"

# Check for vetoes
if ls docs/specs/$EPIC/consensus/messages/inbox/analyst/*veto* 2>/dev/null; then
    echo "❌ Vetoes found. Resolve before continuing."
    exit 1
fi

# Phase 2: Architecture (High tier)
echo "[2/6] Running Architect (Opus 4.5)..."
claude --model claude-opus-4-5-20251101 \
       --system-prompt prompts/architect_prompt.md \
       "Review requirements for $EPIC"

# Phase 3: Planning (Medium tier)
echo "[3/6] Running Tech Lead (Sonnet 4.5)..."
claude --model claude-sonnet-4-5-20250929 \
       --system-prompt prompts/tech_lead_prompt.md \
       "Create implementation plan for $EPIC"

# Phase 4-6: Implementation (Standard tier - Haiku 4.5!)
echo "[4/6] Running Developer (Haiku 4.5)..."
claude --model claude-haiku-4-5-20241022 \
       --system-prompt prompts/quick/developer_quick.md \
       "Implement workstream 1 for $EPIC"

echo "[5/6] Running QA (Haiku 4.5)..."
claude --model claude-haiku-4-5-20241022 \
       --system-prompt prompts/quick/qa_quick.md \
       "Verify implementation for $EPIC"

echo "[6/6] Running DevOps (Haiku 4.5)..."
claude --model claude-haiku-4-5-20241022 \
       --system-prompt prompts/quick/devops_quick.md \
       "Create deployment plan for $EPIC"

echo "✅ Pipeline complete!"
```

### Option 2: Automated Pipeline

For CI/CD integration:

```yaml
# .github/workflows/consensus.yml
name: Consensus Pipeline

on:
  push:
    paths:
      - 'docs/specs/*/epic.md'

jobs:
  analyst:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Analyst
        run: |
          claude --model claude-opus-4-5-20251101 \
                 --system-prompt prompts/analyst_prompt.md \
                 "Analyze new epic"
      - uses: actions/upload-artifact@v4
        with:
          name: requirements
          path: docs/specs/*/consensus/artifacts/requirements.json

  architect:
    needs: analyst
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
      - name: Run Architect
        run: |
          claude --model claude-opus-4-5-20251101 \
                 --system-prompt prompts/architect_prompt.md \
                 "Review requirements"
```

## Tips and Best Practices

### 1. Always Read Before Writing
```bash
# Good: Read context first
claude "First read docs/specs/epic_XX/epic.md and
        docs/specs/epic_XX/consensus/artifacts/requirements.json,
        then create architecture"

# Bad: Writing without context
claude "Create architecture for epic_XX"
```

### 2. Use Project Root
Always run Claude Code from repository root to ensure `CLAUDE.md` is loaded:
```bash
cd /path/to/consensus
claude
```

### 3. Verify Agent Output
After each agent run, verify:
```bash
# Check new artifacts
ls -la docs/specs/epic_XX/consensus/artifacts/

# Check messages
ls -la docs/specs/epic_XX/consensus/messages/inbox/*/

# Check for vetoes
grep -r '"st": "veto"' docs/specs/epic_XX/consensus/messages/
```

### 4. Use Quick Prompts for Iterations
After initial setup, switch to quick prompts:
```bash
# Iteration 1: Full prompt
claude --system-prompt prompts/analyst_prompt.md ...

# Iteration 2+: Quick prompt
claude --system-prompt prompts/quick/analyst_quick.md ...
```

### 5. Model Selection
See [MODELS.md](../../MODELS.md) for detailed model recommendations.

## Troubleshooting

### Agent Ignoring Protocol Rules
- Ensure `CLAUDE.md` is in repository root
- Check if running from correct directory
- Try loading prompt explicitly: `--system-prompt prompts/X_prompt.md`

### Messages Not in English
- Check hooks are configured
- Review agent output before committing
- Add explicit instruction in prompt if needed

### Consensus Stuck in Loop
- Check decision_log for repeated vetoes
- Escalate to human decision after iteration 3
- Consider splitting epic into smaller parts

### Model Errors
- Verify API key is set: `echo $ANTHROPIC_API_KEY`
- Check model availability
- Try fallback model (see MODELS.md)

## Example Sessions

### Example 1: Analyst Agent (High Tier)

```bash
$ cd /path/to/project
$ export ANTHROPIC_API_KEY="sk-ant-..."

$ claude --model claude-opus-4-5-20251101 \
         --system-prompt prompts/analyst_prompt.md

Claude Code> I'm the Analyst agent. What epic should I analyze?

You> Please analyze docs/specs/epic_02_api_gateway/epic.md and create requirements

Claude Code> I'll analyze the epic and create requirements.

[Reading docs/specs/epic_02_api_gateway/epic.md...]
[Reading RULES_COMMON.md for protocol rules...]
[Creating docs/specs/epic_02_api_gateway/consensus/artifacts/requirements.json...]
[Sending message to architect inbox...]
[Logging decision...]

Requirements created. Summary:
- 5 user stories defined
- 12 acceptance criteria
- 3 integrations identified
- Message sent to architect for review

You> /exit
```

### Example 2: Developer Agent (Standard Tier - Haiku 4.5)

```bash
$ claude --model claude-haiku-4-5-20241022 \
         --system-prompt prompts/quick/developer_quick.md

Claude Code> I'm the Developer agent. Ready to implement with TDD.

You> Implement the authentication middleware from docs/specs/epic_02_api_gateway/implementation.md

Claude Code> Let me start by reading the implementation plan and searching for existing auth code.

[Reading implementation.md...]
[Searching codebase for "authentication" and "middleware"...]
[Found: src/middleware/auth.py - checking for duplication...]
[Writing failing test: tests/test_auth_middleware.py...]
[Implementing: src/middleware/api_auth.py...]
[Running tests... ✅ All passing]
[Code review: checking SOLID principles...]

Implementation complete:
- New file: src/middleware/api_auth.py (85 LOC)
- Tests: tests/test_auth_middleware.py (12 test cases)
- Coverage: 92%
- No duplications found
- Ready for QA review

You> Great! Now send a message to QA's inbox

Claude Code> [Creating message in consensus/messages/inbox/qa/2025-12-29-auth-ready.json...]
Message sent to QA.

You> /exit
```

**💡 Notice:** Haiku 4.5 completed full TDD implementation with codebase search, tests, and messaging in under 2 minutes!

---

**See also:**
- [CURSOR.md](CURSOR.md) - Cursor IDE integration
- [MODELS.md](../../MODELS.md) - Model recommendations
- [QUICKSTART.md](../../QUICKSTART.md) - Quick start guide
