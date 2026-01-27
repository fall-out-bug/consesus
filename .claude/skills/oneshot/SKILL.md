---
name: oneshot
description: Autonomous multi-WS execution with checkpoints and resume capability
tools: Read, Bash, Task
---

# /oneshot - Autonomous Feature Execution

Execute all workstreams in a feature autonomously using Task tool with checkpoint resume.

## When to Use

- After `/design` completes WS planning
- To execute feature hands-off
- For features with 3+ workstreams
- When you want background execution

## Workflow

### Step 1: Read Execution Graph (NEW)

```python
from sdp.design.graph import DependencyGraph
import json

# Load workstreams and build graph
graph = DependencyGraph()
for ws_file in glob("docs/workstreams/backlog/WS-*.md"):
    ws_data = parse_frontmatter(ws_file)
    graph.add(WorkstreamNode(
        ws_id=ws_data["ws_id"],
        depends_on=ws_data.get("dependencies", []),
        oneshot_ready=ws_data.get("oneshot_ready", True)
    ))

# Get correct execution order
execution_order = graph.topological_sort()
```

### Step 2: Initialize Checkpoint (NEW)

Create checkpoint file:

```json
{
  "feature": "F60",
  "agent_id": "abc123xyz",
  "status": "in_progress",
  "completed_ws": [],
  "current_ws": "WS-060-01",
  "execution_order": ["WS-060-01", "WS-060-02", "WS-060-03"],
  "started_at": "2026-01-26T12:00:00Z",
  "metrics": {
    "ws_total": 3,
    "ws_completed": 0
  }
}
```

### Step 3: Execute Workstreams in Order

For each WS in topological order:

1. **Verify prerequisites** using DependencyGraph
2. **Execute WS** via @build pattern
3. **Update checkpoint** after completion
4. **Continue** to next ready WS

### Step 4: Checkpoint After Each WS

```python
# Update .oneshot/F60-checkpoint.json
checkpoint["completed_ws"].append(current_ws)
checkpoint["current_ws"] = next_ws
checkpoint["metrics"]["ws_completed"] += 1
write_json(checkpoint)
```

### Step 5: Resume from Checkpoint (NEW)

```bash
/oneshot F60 --resume {agent_id}
```

Reads checkpoint and continues from `current_ws`.

### Step 6: Two-Stage Review (NEW)

After all WS complete:

**Stage 1: Automated Review**
```bash
/review F60
```

**Stage 2: Human UAT**
- Manual testing (5-10 min)
- Approval for deploy

## Checkpoint Format

```json
{
  "feature": "F012",
  "completed_ws": ["00-012-01", "00-012-02"],
  "current_ws": "00-012-03",
  "status": "in_progress",
  "execution_order": ["00-012-01", "00-012-02", "00-012-03"],
  "timestamp": "2026-01-26T12:00:00Z",
  "metrics": {
    "ws_total": 4,
    "ws_completed": 2,
    "coverage_avg": 84
  }
}
```

## Output

- All WS executed in dependency order
- Checkpoint files for resume
- Final review status
- UAT guide

## Next Step

Human UAT → `/deploy F{XX}`
