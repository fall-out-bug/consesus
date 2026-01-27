# Developer DX Guide

Guide to F012 Developer Experience features - daemon, dashboard, test watch, orchestrator, and more.

> **F012: GitHub Agent Orchestrator + Developer DX**

## Overview

F012 adds powerful Developer Experience improvements for SDP users:

- **Daemon Service**: Background task execution
- **Task Queue**: Priority-based workstream queue
- **Multi-Agent Orchestrator**: Concurrent execution with dependency resolution
- **Developer Dashboard**: Real-time TUI monitoring
- **Test Watch Mode**: Auto-rerun tests on file changes
- **Webhook Server**: GitHub webhook integration
- **Unified Status Command**: Quick workstream status overview

## Quick Reference

```bash
# Daemon (background execution)
sdp daemon start    # Start background daemon
sdp daemon stop     # Stop daemon
sdp daemon status   # Check daemon status

# Task Queue
sdp task enqueue WS-001-01        # Add workstream to queue
sdp task execute WS-001-01        # Execute next task
sdp task list                    # Show queued tasks
sdp task cancel WS-001-01         # Cancel queued task

# Orchestrator (multi-agent execution)
sdp orchestrator run F012         # Execute all workstreams for feature
sdp orchestrator enqueue F012     # Enqueue all feature workstreams
sdp orchestrator status           # Show orchestrator state

# Dashboard
sdp dashboard                    # Launch TUI dashboard

# Status
sdp status                       # Show all workstreams
sdp status --status in-progress   # Filter by status
sdp status --feature F012         # Filter by feature

# Test Watch
sdp test watch                   # Watch and rerun tests on changes

# Workspace management
sdp ws start WS-001-01           # Move backlog → in_progress
sdp ws complete WS-001-01        # Move in_progress → completed
sdp ws move WS-001-01 --to blocked  # Move to different status

# Webhooks
sdp webhook start --port 8080    # Start webhook server
sdp webhook events               # Show recent webhook events
```

## Daemon Service

The daemon runs in the background, processing tasks from the queue without blocking your terminal.

### Starting the Daemon

```bash
# Start with default settings
sdp daemon start

# Start with custom settings
sdp daemon start --port 9000 --max-workers 3
```

The daemon:
- Forks into background (double-fork method)
- Writes PID to `.sdp/daemon.pid`
- Logs to `.sdp/daemon.log`

### Checking Status

```bash
sdp daemon status
```

Output:
```
Daemon Status: RUNNING
PID: 12345
Started: 2024-01-27 10:00:00
Workers: 3
Queue: 2 tasks
```

### Stopping the Daemon

```bash
sdp daemon stop
```

## Task Queue

Manage workstreams in a priority queue with state persistence.

### Enqueuing Tasks

```bash
# Enqueue with default priority
sdp task enqueue WS-001-01

# Enqueue with high priority
sdp task enqueue WS-001-01 --priority urgent

# Enqueue entire feature
sdp orchestrator enqueue F012 --priority urgent
```

### Executing Tasks

```bash
# Execute next task from queue
sdp task execute

# Execute specific workstream (without queue)
sdp task execute WS-001-01 --direct

# Dry run (show what would execute)
sdp task execute WS-001-01 --dry-run
```

### Listing Tasks

```bash
# Show all queued tasks
sdp task list

# Show including completed
sdp task list --all
```

## Multi-Agent Orchestrator

Execute multiple workstreams concurrently with automatic dependency resolution.

### Running a Feature

```bash
# Execute all workstreams for F012
sdp orchestrator run F012

# With custom agent pool size
sdp orchestrator run F012 --max-agents 5

# Sequential execution (for debugging)
sdp orchestrator run F012 --ordered
```

The orchestrator:
- Builds dependency graph from workstream `depends_on` fields
- Executes in topological order
- Runs independent workstreams in parallel
- Persists state to `.sdp/orchestrator_state.json`
- Shows real-time progress

### Checking Orchestrator State

```bash
sdp orchestrator status
```

## Developer Dashboard

Real-time TUI dashboard for monitoring workstreams, tests, and agent activity.

```bash
sdp dashboard
```

**Keyboard Shortcuts:**
- `1` / `w` - Workstreams tab
- `2` / `t` - Tests tab
- `3` / `a` - Activity log tab
- `r` - Refresh data
- `q` - Quit

**Features:**
- Workstreams grouped by status
- Test results with coverage
- Real-time agent activity log
- Auto-refresh every second

## Test Watch Mode

Automatically rerun tests when files change.

```bash
# Watch all tests
sdp test watch

# Watch specific module
sdp test watch tests/unit/core/

# Run once then exit
sdp test watch --run-once
```

## Status Command

Quick overview of all workstreams with filtering.

```bash
# Show all workstreams
sdp status

# Filter by status
sdp status --status in-progress

# Filter by feature
sdp status --feature F012

# Filter by assignee
sdp status --assignee "@claude"
```

## Workspace Management

Move workstreams between status directories.

```bash
# Start workstream (backlog → in-progress)
sdp ws start WS-001-01

# Complete workstream (in-progress → completed)
sdp ws complete WS-001-01

# Move to specific status
sdp ws move WS-001-01 --to blocked

# Move without updating INDEX.md
sdp ws move WS-001-01 --to blocked --no-index
```

## Webhook Server

Receive GitHub webhooks for real-time updates.

```bash
# Start webhook server
sdp webhook start --port 8080

# With SMEE tunneling (for local development)
sdp webhook start --smee-url https://smee.io/abc123

# Set webhook secret
sdp webhook start --secret my-webhook-secret
```

**Endpoints:**
- `http://localhost:8080/webhook` - GitHub webhook endpoint
- `http://localhost:8080/health` - Health check
- `http://localhost:8080/events` - Recent webhook events

### Viewing Webhook Events

```bash
sdp webhook events --limit 20
```

## Configuration Files

F012 uses `.sdp/` directory for state:

```
.sdp/
├── daemon.pid              # Daemon process ID
├── daemon.log              # Daemon logs
├── daemon_queue.json       # Queue state
├── orchestrator_state.json # Orchestrator state
├── execution_metrics.json  # Agent execution metrics
├── webhook.log             # Webhook event log
└── github_fields.toml      # GitHub field mappings (optional)
```

## GitHub Project Fields Integration

Sync workstream frontmatter with GitHub Project custom fields.

Create `.sdp/github_fields.toml`:

```toml
project_name = "SDP"

[status_field]
ws_field = "status"
gh_field_name = "Status"
gh_field_type = "single_select"

[size_field]
ws_field = "size"
gh_field_name = "Size"
gh_field_type = "single_select"

[feature_field]
ws_field = "feature"
gh_field_name = "Feature"
gh_field_type = "text"
```

Fields are auto-created in GitHub if missing.

## Workflows

### Typical Feature Development Workflow

1. **Plan workstreams** (`@design`)
2. **Execute in parallel** (`sdp orchestrator run F012`)
3. **Monitor progress** (`sdp dashboard` in separate terminal)
4. **Run tests continuously** (`sdp test watch`)

### CI/CD Integration

```bash
# In CI pipeline
sdp daemon start
sdp orchestrator enqueue F012 --priority urgent
sdp daemon stop
```

### Debugging Failed Workstreams

1. Check status: `sdp status --status blocked`
2. View execution metrics: `cat .sdp/execution_metrics.json`
3. Re-execute with verbose logging

## Tips and Tricks

### Daemon for Background Processing

```bash
# Start daemon, then close terminal
sdp daemon start & disown

# Daemon continues running
```

### Parallel Execution

The orchestrator automatically runs independent workstreams in parallel. For example:

```
WS-001 (no deps) ─┐
WS-002 (no deps) ─┼─> Execute concurrently
WS-003 (depends on WS-001) ─┘
```

### Test-Driven Development

```bash
# Terminal 1: Watch tests
sdp test watch

# Terminal 2: Dashboard
sdp dashboard

# Terminal 3: Execute workstreams
sdp orchestrator run F012 --ordered
```

### Webhook Development

```bash
# 1. Get SMEE URL
curl https://smee.io/new

# 2. Start webhook with tunneling
sdp webhook start --smee-url https://smee.io/abc123

# 3. Configure GitHub webhook to forward to SMEE URL
```
