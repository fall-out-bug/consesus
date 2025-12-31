# Consensus Workflow

A file-based multi-agent coordination framework for AI-assisted software development.

## What is Consensus?

Consensus enables autonomous AI agents (Analyst, Architect, Developer, QA, etc.) to collaborate on software projects through structured JSON messages and shared artifacts. It works with **any AI coding tool** (Cursor, Claude Code, Aider, etc.) and **any LLM** (Claude, GPT, Gemini, etc.).

**Core Principle:**
```
Files are the only required interface.
No special APIs, no vendor lock-in.
```

## Quick Start

### 1. Initialize an Epic

```bash
# Create a new feature epic (Standard tier)
python consensus/scripts/init.py EP-AUTH-001 --title "User Authentication" --tier standard

# Or a quick bug fix (Starter tier)
python consensus/scripts/init.py EP-FIX-001 --title "Fix login bug" --tier starter --mode fast_track
```

### 2. Run Agents

Open your AI tool (Cursor, Claude Code, etc.) and give it the agent prompt:

```
Read consensus/prompts/analyst.md and apply it to docs/specs/EP-AUTH-001/
```

Each agent:
1. Reads `status.json` to check phase
2. Performs its work
3. Creates artifacts
4. Updates `status.json`
5. Sends messages to next agent

### 3. Validate

```bash
python consensus/scripts/validate.py docs/specs/EP-AUTH-001
```

## Protocol Tiers

| Tier | Best For | Validation |
|------|----------|------------|
| **Starter** | Bug fixes, prototypes | JSON syntax only |
| **Standard** | Features, typical work | Full schema validation |
| **Enterprise** | Large systems | Schema + custom rules |

## Execution Modes

| Mode | Agent Chain | Use When |
|------|-------------|----------|
| `full` | analyst → architect → tech_lead → developer → qa → devops | New features |
| `fast_track` | developer → qa | Bug fixes (≤50 LOC) |
| `hotfix` | developer → devops | Production emergencies |

## Agent Roles

| Role | Mission | Deliverable |
|------|---------|-------------|
| **Analyst** | Define requirements | `requirements.json` |
| **Architect** | Design system | `architecture.json` |
| **Tech Lead** | Plan implementation | `plan.json` |
| **Developer** | Write code | Implementation |
| **QA** | Verify quality | `test_results.json` |
| **DevOps** | Deploy safely | `deployment.json` |

## Directory Structure

```
docs/specs/{epic}/
├── epic.md                    # Problem description
└── consensus/
    ├── status.json            # State machine
    ├── artifacts/             # Agent deliverables
    ├── messages/inbox/{role}/ # Agent communication
    └── decision_log/          # Audit trail
```

## Key Files

| File | Purpose |
|------|---------|
| [PROTOCOL.md](PROTOCOL.md) | Full protocol specification |
| [consensus/prompts/](consensus/prompts/) | Agent instruction files |
| [consensus/schema/](consensus/schema/) | JSON validation schemas |
| [consensus/scripts/](consensus/scripts/) | Validation and init tools |
| [docs/adr/](docs/adr/) | Architecture Decision Records |

## Platform Integration

Works with any AI coding tool:

| Platform | Guide |
|----------|-------|
| Cursor | [docs/guides/CURSOR.md](docs/guides/CURSOR.md) |
| Claude Code | [docs/guides/CLAUDE_CODE.md](docs/guides/CLAUDE_CODE.md) |

## Model Recommendations

See [MODELS.md](MODELS.md) for LLM selection guidance:
- **Strategic roles** (Analyst, Architect): Most capable model
- **Implementation roles** (Developer, QA): Faster models work well

## Architecture Principles

The protocol enforces Clean Architecture:
- Dependencies point **inward**
- No layer violations
- Explicit contracts at boundaries

## Example Flow

```
1. User creates epic.md with problem description

2. Analyst reads epic.md
   → Creates requirements.json
   → Updates status.json (phase: architecture)

3. Architect reads requirements.json
   → Creates architecture.json
   → Updates status.json (phase: planning)

4. Tech Lead reads architecture.json
   → Creates plan.json with workstreams
   → Updates status.json (phase: implementation)

5. Developer executes workstreams
   → Implements code with TDD
   → Updates status.json (phase: testing)

6. QA validates acceptance criteria
   → Creates test_results.json
   → Updates status.json (phase: deployment)

7. DevOps deploys with rollback plan
   → Updates status.json (phase: done)
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

[MIT](LICENSE)
