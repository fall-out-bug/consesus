# Unified Progressive Consensus Protocol v2.0

## Overview

The UPC Protocol enables multi-agent collaboration through file-based communication. Agents read and write files to coordinate work on software development tasks.

**Core Principle:**
```
Files are the only required interface.
Everything else is optional enhancement.
```

## Quick Start

### Initialize a New Epic

```bash
# Standard tier (recommended)
python consensus/scripts/init.py EP-001 --title "My Feature" --tier standard

# Starter tier (minimal structure)
python consensus/scripts/init.py EP-001 --title "Bug Fix" --tier starter --mode fast_track
```

### Run an Agent

1. Open `consensus/prompts/{role}.md` as context
2. Point agent to `docs/specs/{epic}/`
3. Agent reads `status.json`, performs work, updates `status.json`

### Validate

```bash
python consensus/scripts/validate.py docs/specs/EP-001 --tier standard
```

## Protocol Tiers

| Tier | Use Case | Validation | Agent Chain |
|------|----------|------------|-------------|
| **Starter** | Bug fixes, prototypes | JSON syntax only | Optional |
| **Standard** | Features | Full schema validation | Required |
| **Enterprise** | Large systems | Schema + custom rules | Required + custom |

## Execution Modes

| Mode | Agent Chain | Use Case |
|------|-------------|----------|
| `full` | analyst → architect → tech_lead → developer → qa → devops | New features |
| `fast_track` | developer → qa | Bug fixes (≤50 LOC) |
| `hotfix` | developer → devops | Critical production issues |

## Directory Structure

### Standard Tier

```
docs/specs/{epic}/
├── epic.md                    # Problem description
└── consensus/
    ├── status.json            # State machine (required)
    ├── artifacts/             # Agent deliverables
    │   ├── requirements.json
    │   ├── architecture.json
    │   ├── plan.json
    │   ├── implementation.json
    │   └── test_results.json
    ├── messages/
    │   └── inbox/{role}/      # Agent communication
    └── decision_log/          # Audit trail
```

## State Machine (`status.json`)

The `status.json` file is the single source of truth for epic state.

```json
{
  "epic_id": "EP-001",
  "tier": "standard",
  "phase": "implementation",
  "mode": "full",
  "iteration": 1,
  "approvals": ["analyst", "architect", "tech_lead"],
  "blockers": [],
  "workstreams": [
    { "id": "WS-01", "title": "Domain Layer", "status": "done" },
    { "id": "WS-02", "title": "API Layer", "status": "in_progress" }
  ],
  "updated_at": "2025-12-31T14:30:00Z",
  "updated_by": "developer"
}
```

### Phase Flow

```
requirements → architecture → planning → implementation → testing → deployment → done
                                ↑                                        ↓
                                └────────────── blocked ←────────────────┘
```

### Field Definitions

| Field | Description |
|-------|-------------|
| `tier` | Validation strictness (starter/standard/enterprise) |
| `phase` | Current lifecycle phase |
| `mode` | Agent topology (full/fast_track/hotfix) |
| `iteration` | Increment on veto cycles |
| `approvals` | Roles that approved current phase |
| `blockers` | Active vetoes or questions |
| `workstreams` | Micro-tasks for granular tracking |

## Agent Rules

### Reading

- **Only read your own inbox**: `messages/inbox/{your_role}/`
- **Always read `status.json` first** before acting

### Writing

- **Never write to your own inbox**
- **Always update `status.json`** after completing work
- **Validate before writing** against schema

### Phase Ownership

Only the phase owner can advance `phase`:
- `requirements` → analyst
- `architecture` → architect
- `planning` → tech_lead
- `implementation` → developer
- `testing` → qa
- `deployment` → devops

## Message Format

Messages are JSON files in `messages/inbox/{role}/`:

```json
{
  "d": "2025-12-31",
  "st": "handoff",
  "r": "analyst",
  "epic": "EP-001",
  "sm": ["Requirements ready for architecture review"],
  "nx": ["Review and design architecture"],
  "artifacts": ["consensus/artifacts/requirements.json"]
}
```

| Key | Description |
|-----|-------------|
| `d` | Date (YYYY-MM-DD) |
| `st` | Status (request/response/veto/approval/handoff) |
| `r` | Sender role |
| `sm` | Summary points |
| `nx` | Next actions |

## Veto Protocol

### Cannot Override (Blocking)

| Veto | Authority | Trigger |
|------|-----------|---------|
| `layer_violation` | architect | Dependencies pointing outward |
| `critical_security_issue` | security | Security vulnerability |
| `no_rollback_plan` | devops | Missing rollback strategy |
| `failed_acceptance` | qa | Acceptance criteria not met |

### Can Negotiate

| Veto | Authority | Trigger |
|------|-----------|---------|
| `scope_creep` | analyst | Exceeds original scope |
| `untestable_plan` | tech_lead | Plan cannot be verified |

## Validation

### Run Validator

```bash
# Standard validation
python consensus/scripts/validate.py docs/specs/EP-001

# Starter (syntax only)
python consensus/scripts/validate.py docs/specs/EP-001 --tier starter

# Enterprise (strict)
python consensus/scripts/validate.py docs/specs/EP-001 --tier enterprise
```

### Validation Gates

Before phase transition:
1. **Schema gate**: JSON validates against schema
2. **Phase gate**: Required artifacts exist
3. **Ownership gate**: Correct role advancing phase
4. **Language gate**: Protocol JSON in English

## Schemas

All schemas are in `consensus/schema/`:

| Schema | Purpose |
|--------|---------|
| `status.schema.json` | State machine |
| `message.schema.json` | Agent communication |
| `requirements.schema.json` | Analyst deliverable |
| `architecture.schema.json` | Architect deliverable |
| `plan.schema.json` | Tech Lead deliverable |

## Platform Adapters

The protocol works with any tool. Platform-specific guides are in `docs/guides/adapters/`:

| Platform | Config |
|----------|--------|
| Cursor | `.cursorrules` |
| Claude Code | `CLAUDE.md` |
| Aider | `.aider.conf.yml` |

See [docs/guides/](docs/guides/) for setup instructions.

## Migration from v1.2

```bash
# Move existing epic to new structure
python consensus/scripts/init.py EP-001 --base-dir docs/specs

# Copy existing artifacts
cp old/requirements.json docs/specs/EP-001/consensus/artifacts/

# Validate
python consensus/scripts/validate.py docs/specs/EP-001
```

## References

- [ADR-0004: Unified Progressive Consensus](docs/adr/0004-unified-progressive-consensus.md)
- [Agent Prompts](consensus/prompts/)
- [JSON Schemas](consensus/schema/)
