---
title: "GitHub Agent Orchestrator - Spec"
description: "Bidirectional sync between GitHub Issues and SDP workstreams with autonomous agent execution"
---

# GitHub Agent Orchestrator

**Status:** Draft
**Created:** 2025-01-25
**Feature ID:** F012 (proposed)

## Executive Summary

Autonomous task orchestration system that bridges GitHub Issues with AI coding agents (Claude Code, Cursor, OpenCode) via SDP workstreams. Agents self-assign tasks from a queue, execute them following TDD workflow, and report results back to GitHub.

**Inspired by:** [vibe-kanban](https://github.com/BloopAI/vibe-kanban) task management system

---

## Context & Problem

### Current State (SDP)
- Workstreams are local markdown files (`docs/workstreams/backlog/*.md`)
- GitHub sync is unidirectional (WS → GitHub Issues via `sdp github sync`)
- Agent execution is manual (`/oneshot`, `/build` commands)
- No task queue or multi-agent coordination

### Desired State
- **Bidirectional sync:** GitHub Issues ↔ WS files ↔ Agent Queue
- **Autonomous execution:** Agents self-assign from queue
- **Multi-agent support:** Claude, Cursor, OpenCode work in parallel
- **Rich observability:** TUI + GitHub comments + logs

### Problem Being Solved
1. **Manual workflow:** Creating issues, assigning to agents, tracking progress is manual
2. **No coordination:** Multiple agents can't work together without conflicts
3. **Poor visibility:** No centralized view of what agents are doing
4. **GitHub integration:** Issues are separate from WS execution

---

## Goals & Non-Goals

### Goals ✅
1. **Bidirectional sync** between GitHub Issues and WS files
2. **Local daemon** (`sdp daemon --watch`) that manages task queue
3. **Queue-based multi-agent orchestration** (agents self-assign)
4. **Rich TUI** for monitoring agent activity (kanban-style)
5. **GitHub Project Fields** for status mapping (not labels)
6. **Git-backed storage** (WS files = source of truth)
7. **Smart conflict resolution** (GitHub ↔ local state)
8. **All three ways to create tasks:** Manual GitHub, CLI, Auto from WS

### Non-Goals ❌
1. **Replacing GitHub Issues** with custom task storage
2. **Real-time collaboration** (multiple humans editing same task)
3. **Complex dependencies** between tasks (keep it simple for MVP)
4. **Mobile apps** or web UI (TUI only for MVP)
5. **付费 features** or enterprise integrations

---

## User Stories

### As a Developer
- I want to create a GitHub Issue and have it automatically appear in SDP
- I want agents to automatically pick up tasks and execute them
- I want to see what agents are doing in a rich TUI
- I want to monitor agent progress in real-time

### As a Tech Lead
- I want to control which agents run on which tasks
- I want to review agent work before it's merged
- I want audit logs of all agent actions
- I want to enforce pre-execution checks (tests pass, branch clean)

### As an AI Agent
- I want to self-assign tasks from a queue
- I want to report my progress back to GitHub
- I want to know if another agent is already working on a task
- I want to fail gracefully and report errors

---

## Technical Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Repository                        │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ GitHub Issues│  │ Project Board│  │   Webhooks   │       │
│  └──────┬──────┘  └──────┬───────┘  └──────┬───────┘       │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          │ API              │ Fields           │ Events
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   SDP Daemon (sdp daemon --watch)           │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │Sync Service │  │Task Queue    │  │Agent Manager │       │
│  │(bidirectional│  │(priority    │  │(spawn/pool)  │       │
│  │ GH ↔ WS)    │  │ FIFO)       │  │              │       │
│  └──────┬──────┘  └──────┬───────┘  └──────┬───────┘       │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                  Local Storage (Git-backed)                  │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │WS Files     │  │State Cache   │  │Audit Log     │       │
│  │(markdown)   │  │(SQLite/JSON) │  │(agent actions│       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
          │
          │ Task Assignment
          ▼
┌─────────────────────────────────────────────────────────────┐
│                    AI Agents (via Platform Adapters)         │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │Claude Code  │  │Cursor/Codex  │  │OpenCode      │       │
│  │Adapter      │  │Adapter       │  │Adapter       │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

#### 1. Task Creation (3 ways)

**Way A: Manual in GitHub**
```bash
# User creates issue in GitHub
gh issue create --title "Add user auth" --body "Implement..."

# Daemon webhook detects new issue
# Sync Service creates WS file
# Task Queue adds to backlog
```

**Way B: CLI Command**
```bash
sdp task create "Add user auth" --description "Implement..."

# Sync Service creates GitHub issue
# WS file created
# Added to queue
```

**Way C: Auto from WS**
```bash
sdp parse-features

# All backlog WS files synced to GitHub
# Added to queue if not already
```

#### 2. Agent Assignment

```python
# Daemon loop:
while True:
    task = queue.get_next_ready()  # Priority-based
    if task and can_assign(task):
        agent = select_agent(task)  # Based on config/labels
        agent.assign(task)
        update_github_status(task, "In Progress")
        execute_agent(agent, task)
```

#### 3. Agent Execution

```bash
# Agent (via Platform Adapter):
sdp agent execute --task-id=123 --agent=claude-code

# Equivalent to:
# /oneshot FXXX (for feature tasks)
# /build WS-XXX-YY (for workstream tasks)
```

#### 4. Progress Reporting

```bash
# Agent updates GitHub via comments:
gh issue comment 123 --body "### Step 1/5: Domain layer ✅"

# Daemon detects comment, updates local state
# TUI reflects progress in real-time
```

---

## Status Mapping

### GitHub Project Fields → Kanban Columns

```
┌──────────────┬──────────────────┬─────────────────┐
│ Kanban Column│ GitHub Field     │ WS Status       │
├──────────────┼──────────────────┼─────────────────┤
│ To Do        │ Status: "Todo"   | backlog         │
│ In Progress  │ Status: "In Prog"│ in-progress     │
│ In Review    │ Status: "Review" │ completed       │
│ Done         │ Status: "Done"   | completed+merged│
└──────────────┴──────────────────┴─────────────────┘
```

**Implementation:** GitHub Projects v2 API (GraphQL)

---

## Multi-Agent Orchestration

### Queue-Based System

```python
@dataclass
class Task:
    id: str  # GitHub issue number or WS ID
    title: str
    priority: int  # 1-10 (higher = more important)
    status: TaskStatus
    assigned_agent: Optional[str] = None
    dependencies: list[str] = field(default_factory=list)
    github_issue: int
    ws_file: Optional[Path] = None
```

### Agent Selection Logic

```python
def select_agent(task: Task) -> AgentType:
    # Config-based or label-based
    if task.labels.contains("agent:claude"):
        return AgentType.CLAUDE_CODE
    elif task.labels.contains("agent:cursor"):
        return AgentType.CURSOR
    else:
        return DEFAULT_AGENT  # From config
```

### Parallel Execution

```python
# Daemon can spawn multiple agents in parallel
async def process_queue():
    running = []

    while task := queue.get_next_ready():
        # Respect concurrency limit
        if len(running) >= MAX_CONCURRENT_AGENTS:
            await wait_for_one(running)

        agent = spawn_agent(task)
        running.append(agent)

    await asyncio.gather(*running)
```

---

## CLI Interface

### New Commands

```bash
# Daemon management
sdp daemon start [--config PATH]    # Start daemon
sdp daemon stop                     # Stop daemon
sdp daemon status                   # Check if running
sdp daemon logs [--tail]            # View logs

# Task management (creates WS + GitHub issue)
sdp task create "Title" [-d DESC] [-p PRIORITY] [--agent TYPE]
sdp task list [--status STATUS]     # List tasks (TUI table)
sdp task take <id>                  # Manually assign to self
sdp task status <id>                # Show task details
sdp task logs <id> [--tail]         # Show agent logs

# TUI
sdp tui                             # Rich kanban board
sdp tui --watch                     # Auto-refresh

# Sync
sdp sync github                    # Force bidirectional sync
sdp sync issues                    # Pull issues → WS
sdp sync workstreams               # Push WS → issues
```

### Rich TUI (textual or rich)

```
┌─────────────────────────────────────────────────────────────┐
│  SDP Task Board                            [sdp daemon: ●]  │
├─────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   To Do     │  │ In Progress │  │   Done      │          │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤          │
│  │#123 Auth    │  │#124 API     │  │#120 Tests   │          │
│  │  Prio: 8    │  │  Agent: CC  │  │  Agent: Csr │          │
│  │  Labels:bug │  │  45% done   │  │  Merged ✅  │          │
│  │             │  │             │  │             │          │
│  │#125 Logging │  │             │  │#121 Docs    │          │
│  │  Prio: 5    │  │             │  │  Agent: CC  │          │
│  │             │  │             │  │  Merged ✅  │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                                  │
│  [c]reate  [t]ake  [r]efresh  [q]uit  [?] help                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Configuration

### `~/.config/sdp/config.toml`

```toml
[daemon]
# Daemon settings
poll_interval = "30s"           # GitHub polling interval
max_concurrent_agents = 3       # Max parallel agents
auto_execute = false            # Auto-start agents or manual?
watch_repos = []                # Repos to watch (default: all)

[agents]
# Agent-specific settings
default = "claude-code"

[agents.claude-code]
enabled = true
priority_boost = 0              # Prefer this agent (+N priority)
max_concurrent = 2              # Max parallel tasks

[agents.cursor]
enabled = true
priority_boost = -1             # Slightly prefer less
max_concurrent = 1

[agents.opencode]
enabled = false                  # Disabled for now

[queue]
# Task queue settings
max_size = 100
default_priority = 5
respect_dependencies = true      # Don't assign if deps not done

[github]
# GitHub integration
token_cmd = "gh auth token"      # How to get token
default_project = "SDP"         # Project board for status
webhook_secret = ""             # Optional: for webhook auth
```

---

## Security

### Token Security
- Store in `~/.config/sdp/credentials` (not in Git)
- Use `gh auth token` (GitHub CLI) if available
- File permissions: `0600` (owner read/write only)

### Pre-Execution Checks
```bash
# Before agent starts:
1. Verify git working tree is clean
2. Ensure on correct branch
3. Run tests pass (if configured)
4. Check no uncommitted changes
```

### Sandboxing
```python
# Agent execution constraints:
- Only write to allowed directories
- Max execution time (configurable)
- Resource limits (CPU, memory)
- Git hooks for validation
```

### Audit Logging
```json
{
  "timestamp": "2025-01-25T10:00:00Z",
  "event": "agent_assigned",
  "task_id": "123",
  "agent": "claude-code",
  "triggered_by": "daemon",
  "git_sha": "abc123"
}
```

---

## Testing Strategy

### 1. Unit Tests (Core Logic)
- Queue management (priority, dependencies)
- Status mapping (GitHub ↔ WS)
- Agent selection logic
- Conflict resolution

**Mock:** GitHub API, file system

### 2. Integration Tests (GitHub Test Repo)
- Real GitHub API calls
- Create/update/delete issues
- Project board sync
- Webhook handling

**Target:** Test repository (not production)

### 3. E2E Tests (Full Agent Execution)
- Spawn real agent
- Execute task end-to-end
- Verify GitHub updates
- Check WS file changes

**Target:** Isolated test environment

---

## Dependencies

### Required
- `pygithub` — GitHub API client
- `textual` or `rich` — TUI framework
- `aiohttp` — Async HTTP (for webhooks)
- `asyncio` — Concurrent agent execution

### Optional
- `pytest-asyncio` — Async testing
- `pytest-mock` — Mocking GitHub API

### Already in SDP
- Platform adapters (F004) ✅
- GitHub client (F002) ✅
- Workstream parser (F006) ✅

---

## Implementation Phases

### Phase 1: MVP (Basic)
- [ ] Daemon skeleton (`sdp daemon start`)
- [ ] Bidirectional sync (WS ↔ GitHub Issues)
- [ ] Task queue (in-memory, single-agent)
- [ ] CLI commands (`task create`, `task list`)
- [ ] GitHub Project Fields mapping

### Phase 2: Automation
- [ ] Multi-agent queue (priority-based)
- [ ] Agent auto-assignment
- [ ] Parallel execution (async)
- [ ] Webhook support (GitHub → Daemon)
- [ ] Pre-execution checks

### Phase 3: Orchestration
- [ ] Rich TUI (kanban board)
- [ ] Real-time monitoring (`task logs --tail`)
- [ ] Smart conflict resolution
- [ ] Agent pool management
- [ ] Dependency resolution

---

## Open Questions

1. **Webhook vs Polling:** Should we rely on GitHub webhooks or polling?
   - *Decision:* Polling for MVP, webhooks for Phase 2

2. **Conflict Resolution Details:** How exactly to merge conflicting changes?
   - *Decision:* Use git merge strategy (ours/theirs) with human fallback

3. **Agent Isolation:** Should each agent run in separate process or thread?
   - *Decision:* Separate process for isolation, use `subprocess.Popen`

4. **Task Dependencies:** How to represent and resolve dependencies?
   - *Decision:* WS `Dependencies:` field already exists, reuse it

5. **TUI Framework:** textual vs rich vs custom curses?
   - *Decision:* textual (modern, async, well-maintained)

---

## Success Criteria

### MVP Success
- [ ] Daemon runs continuously and syncs GitHub ↔ WS
- [ ] Tasks created via GitHub/CLI/auto all appear in queue
- [ ] Agent executes task and updates GitHub status
- [ ] CLI commands work (`task create`, `task list`, `daemon status`)

### Phase 2 Success
- [ ] Multiple agents run concurrently
- [ ] Webhooks trigger immediate sync
- [ ] Pre-exec checks prevent bad states
- [ ] All tests pass (unit + integration + E2E)

### Phase 3 Success
- [ ] Rich TUI shows real-time agent activity
- [ ] Smart merge resolves conflicts without human intervention
- [ ] Audit log captures all agent actions
- [ ] Production-ready (monitored, documented)

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| GitHub API rate limits | High | Smart polling, exponential backoff |
| Agent conflicts (race condition) | High | Queue-based assignment, lock files |
| Webhook delivery failures | Medium | Polling fallback |
| Token leakage | High | Secure storage, file permissions |
| Daemon crashes | Medium | Persistent state, restart recovery |
| Test flakiness | Low | Mocked GitHub API for unit tests |

---

## Next Steps

1. **Design workstream breakdown** (`/design idea-github-agent-orchestrator`)
2. **Create F012 feature** with workstreams
3. **Start with WS-00-012-01:** Daemon skeleton + sync

---

**References:**
- [Vibe Kanban](https://github.com/BloopAI/vibe-kanban) — Inspiration
- [SDP GitHub Sync](src/sdp/github/sync_service.py) — Existing sync code
- [Platform Adapters](src/sdp/adapters/) — Agent abstraction
