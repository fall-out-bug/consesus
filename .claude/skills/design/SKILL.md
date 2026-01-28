---
name: design
description: Analyze Beads task and decompose into workstreams with dependencies. Creates sub-tasks with parent-child relationships using EnterPlanMode.
tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
version: 2.1.0-beads-ai-comm
---

# @design - Feature Decomposition (Beads + AI-Comm Integration)

Analyze requirements and decompose Beads feature tasks into workstreams with sequential dependencies using EnterPlanMode for interactive planning.

## When to Use

- After `@idea` creates a Beads task
- When a feature needs to be broken into workstreams
- Before starting implementation
- When architectural decisions need user input

## Beads vs Markdown Workflow

**This skill creates Beads sub-tasks** with hash-based IDs, dependencies, and execution graphs.

For traditional markdown workflow, use `prompts/commands/design.md` instead.

## Invocation

```bash
@design bd-0001
```

**Environment Variables:**
- `BEADS_USE_MOCK=true` - Use mock Beads (default for dev)
- `BEADS_USE_MOCK=false` - Use real Beads CLI (requires Go + bd installed)

## Workflow

**IMPORTANT:** Use AskUserQuestion for architectural decisions before decomposition.

### When to Call /think

If architecture is **complex with multiple valid approaches**, call `@think` first:

```python
Skill("think")
# Returns structured analysis of architectural options
```

Use @think for:
- Multiple valid architectural approaches
- Complex integration points
- Unclear failure modes
- Significant performance/security tradeoffs

### Step 0: Enter Plan Mode (NEW from ai-comm)

```markdown
EnterPlanMode()
```

This allows you to explore the codebase and gather context before presenting a plan.

### Step 1: Initialize Beads Client

```python
from sdp.beads import create_beads_client, FeatureDecomposer
from sdp.design.graph import DependencyGraph  # NEW
import os

use_mock = os.getenv("BEADS_USE_MOCK", "true").lower() == "true"
client = create_beads_client(use_mock=use_mock)
decomposer = FeatureDecomposer(client)
graph = DependencyGraph()  # NEW
```

### Step 2: Read Parent Task (In Plan Mode)

```python
# Get feature task from @idea
feature = client.get_task(beads_id)

if not feature:
    print(f"❌ Task not found: {beads_id}")
    return

print(f"📋 Designing: {feature.title}")
print(f"   Description: {feature.description[:100]}...")

# Read intent file if exists (NEW)
try:
    with open(f"docs/intent/{beads_id}.json") as f:
        intent = json.load(f)
        print(f"   Mission: {intent.get('mission')}")
        print(f"   Alignment: {intent.get('alignment')}")
except FileNotFoundError:
    pass
```

### Step 3: Read Context (In Plan Mode)

```bash
# Core documentation
@PROJECT_MAP.md
@PROTOCOL.md
@CODE_PATTERNS.md

# Feature context (NEW)
@docs/drafts/beads-{beads_id}.md
@docs/intent/{beads_id}.json  # Machine-readable intent
@PRODUCT_VISION.md  # Product alignment
```

### Step 4: Interactive Planning

**Use AskUserQuestion** for architectural decisions:

```markdown
AskUserQuestion({
  "questions": [{
    "question": "What is the complexity level of this feature?",
    "header": "Complexity",
    "options": [
      {"label": "Simple (1-2 workstreams)", "description": "Straightforward, minimal integration"},
      {"label": "Medium (3-5 workstreams)", "description": "Standard complexity, some integration points"},
      {"label": "Large (6+ workstreams)", "description": "Complex, multiple integrations, significant changes"}
    ],
    "multiSelect": false
  }, {
    "question": "Which layers need implementation?",
    "header": "Layers",
    "options": [
      {"label": "Domain", "description": "Business logic, entities, value objects"},
      {"label": "Repository", "description": "Data access, persistence layer"},
      {"label": "Service", "description": "Application services, use cases"},
      {"label": "API/Presentation", "description": "Endpoints, controllers, UI"}
    ],
    "multiSelect": true
  }]
})
```

**Continue interviewing** about:
- Database schema changes
- External API integrations
- Authentication/authorization needs
- Performance requirements
- Testing strategy

### Step 5: Determine Workstreams with Enhanced Metadata (MERGED)

Based on interview answers, determine workstreams with execution metadata:

**Simple feature:**
```python
# Default 3 workstreams
ws_ids = decomposer.decompose(beads_id)
```

**Medium feature:**
```python
# Custom workstreams with enhanced metadata
from sdp.beads import WorkstreamSpec

custom_workstreams = [
    WorkstreamSpec(
        title="Domain model",
        sequence=1,
        size="MEDIUM",
        # Enhanced metadata (NEW)
        estimated_loc=450,
        estimated_duration="2-3 hours",
        oneshot_ready=True,
    ),
    WorkstreamSpec(
        title="Database schema",
        sequence=2,
        size="MEDIUM",
        dependencies=["ws-001"],
        estimated_loc=300,
        estimated_duration="1-2 hours",
        oneshot_ready=False,  # Requires manual verification
    ),
    WorkstreamSpec(
        title="Repository layer",
        sequence=3,
        size="MEDIUM",
        dependencies=["ws-002"],
        estimated_loc=500,
        estimated_duration="3-4 hours",
        oneshot_ready=True,
    ),
    WorkstreamSpec(
        title="Service layer",
        sequence=4,
        size="MEDIUM",
        dependencies=["ws-003"],
        estimated_loc=600,
        estimated_duration="4-5 hours",
        oneshot_ready=True,
    ),
    WorkstreamSpec(
        title="API endpoints",
        sequence=5,
        size="MEDIUM",
        dependencies=["ws-004"],
        estimated_loc=400,
        estimated_duration="2-3 hours",
        oneshot_ready=True,
    ),
]

ws_ids = decomposer.decompose(beads_id, workstreams=custom_workstreams)
```

**Large feature:**
```python
# More granular workstreams with detailed metadata
custom_workstreams = [
    WorkstreamSpec(
        title="Domain entities",
        sequence=1,
        size="MEDIUM",
        estimated_loc=350,
        estimated_duration="2-3 hours",
        oneshot_ready=True,
    ),
    WorkstreamSpec(
        title="Value objects",
        sequence=2,
        size="SMALL",
        dependencies=["ws-001"],
        estimated_loc=200,
        estimated_duration="1-2 hours",
        oneshot_ready=True,
    ),
    WorkstreamSpec(
        title="Database migration",
        sequence=3,
        size="MEDIUM",
        estimated_loc=300,
        estimated_duration="1-2 hours",
        oneshot_ready=False,  # Manual DB verification required
    ),
    WorkstreamSpec(
        title="Repository interface",
        sequence=4,
        size="SMALL",
        dependencies=["ws-001"],
        estimated_loc=150,
        estimated_duration="1 hour",
        oneshot_ready=True,
    ),
    WorkstreamSpec(
        title="Repository implementation",
        sequence=5,
        size="MEDIUM",
        dependencies=["ws-003", "ws-004"],
        estimated_loc=550,
        estimated_duration="3-4 hours",
        oneshot_ready=True,
    ),
    WorkstreamSpec(
        title="Service interface",
        sequence=6,
        size="SMALL",
        dependencies=["ws-001"],
        estimated_loc=200,
        estimated_duration="1-2 hours",
        oneshot_ready=True,
    ),
    WorkstreamSpec(
        title="Service implementation",
        sequence=7,
        size="MEDIUM",
        dependencies=["ws-005", "ws-006"],
        estimated_loc=700,
        estimated_duration="4-5 hours",
        oneshot_ready=True,
    ),
    WorkstreamSpec(
        title="API controllers",
        sequence=8,
        size="MEDIUM",
        dependencies=["ws-007"],
        estimated_loc=450,
        estimated_duration="2-3 hours",
        oneshot_ready=True,
    ),
]

ws_ids = decomposer.decompose(beads_id, workstreams=custom_workstreams)
```

### Step 6: Build Execution Graph (NEW from ai-comm)

```python
# Build dependency graph for topological sort
for ws in custom_workstreams:
    graph.add(WorkstreamNode(
        ws_id=f"ws-{ws.sequence:03d}",
        title=ws.title,
        depends_on=ws.dependencies or [],
        oneshot_ready=ws.oneshot_ready,
        estimated_loc=ws.estimated_loc,
        estimated_duration=ws.estimated_duration,
    ))

# Get correct execution order
execution_order = graph.topological_sort()

print(f"✅ Execution order: {' → '.join(execution_order)}")
```

### Step 7: Verify Dependencies

```python
# Check ready tasks
ready = client.get_ready_tasks()
print(f"✅ Ready to start: {ready}")

# Verify dependencies
for i, ws_id in enumerate(ws_ids):
    ws = client.get_task(ws_id)
    deps = ws.dependencies

    if deps:
        print(f"  {ws_id} ({ws.title}) blocked by {len(deps)} tasks")
    else:
        print(f"  {ws_id} ({ws.title}) ready to start")
```

### Step 8: Exit Plan Mode (NEW from ai-comm)

After decomposition is complete, exit plan mode and present plan for approval:

```markdown
ExitPlanMode({
  "allowedPrompts": [
    {"tool": "Bash", "prompt": "run tests"},
    {"tool": "Bash", "prompt": "install dependencies"}
  ]
})
```

This shows the user:
- Workstream decomposition
- Execution order with dependency graph
- Estimated LOC and duration for each WS
- Requires user approval before proceeding

### Step 9: Export to Markdown with Execution Graph (MERGED)

```python
# Export for human reference with enhanced metadata
markdown_path = f"docs/workstreams/beads-{beads_id}.md"

with open(markdown_path, "w") as f:
    f.write(f"# Workstreams for {feature.title}\n\n")
    f.write(f"> **Parent Task:** {beads_id}\n")
    f.write(f"> **Created:** {datetime.utcnow().isoformat()}\n\n")

    # Add execution graph (NEW)
    f.write("## Execution Graph\n\n")
    f.write("```mermaid\n")
    f.write(graph.to_mermaid())
    f.write("```\n\n")

    for i, ws_id in enumerate(ws_ids, 1):
        ws = client.get_task(ws_id)
        f.write(f"## {i}. {ws.title}\n")
        f.write(f"**ID:** {ws_id}\n")
        f.write(f"**Status:** {ws.status.value}\n")
        f.write(f"**Priority:** {ws.priority.value}\n")

        # Enhanced metadata (NEW)
        if ws.sdp_metadata.get("estimated_loc"):
            f.write(f"**Estimated LOC:** {ws.sdp_metadata['estimated_loc']}\n")
        if ws.sdp_metadata.get("estimated_duration"):
            f.write(f"**Estimated Duration:** {ws.sdp_metadata['estimated_duration']}\n")
        if ws.sdp_metadata.get("oneshot_ready") is not None:
            f.write(f"**Oneshot Ready:** {'✅' if ws.sdp_metadata['oneshot_ready'] else '❌'}\n")

        if ws.dependencies:
            dep_ids = [d.task_id for d in ws.dependencies]
            f.write(f"**Dependencies:** {', '.join(dep_ids)}\n")
        f.write("\n")
```

## Output

**Primary:** List of Beads workstream IDs (e.g., `[bd-0001.1, bd-0001.2, bd-0001.3]`)

**Secondary:**
- Optional markdown export to `docs/workstreams/beads-{parent_id}.md` with execution graph
- Execution order for @oneshot (NEW)

**Beads Sub-Tasks:**
- `id`: Hash-based IDs (auto-generated, e.g., `bd-0001.1`)
- `title`: Workstream title
- `parent_id`: Reference to parent feature task
- `status`: OPEN (default)
- `dependencies`: List of blocking dependencies
- `sdp_metadata`: Workstream sequence, size, enhanced metadata (LOC, duration, oneshot_ready)

## Next Steps

After decomposition:

1. **Exit plan mode and get approval** (NEW)

2. **Check ready tasks:**
   ```bash
   bd ready

   # Output:
   # Ready tasks:
   # - bd-0001.1 (Domain entities)
   ```

3. **Start execution:**
   ```bash
   @build bd-0001.1
   ```

   Or use autonomous execution:
   ```bash
   @oneshot bd-0001  # Uses execution graph for correct order (NEW)
   ```

4. **Monitor progress:**
   ```bash
   bd status --watch

   # Automatically shows new tasks as they become ready
   ```

## Example Session

```bash
# Decompose feature
@design bd-0001

# ... (EnterPlanMode exploration, interviewing happens) ...

# Output:
✅ Created 5 workstreams:
   bd-0001.1: Domain model (450 LOC, 2-3h) [READY]
   bd-0001.2: Database schema (300 LOC, 1-2h) [READY]
   bd-0001.3: Repository layer (500 LOC, 3-4h) [BLOCKED by bd-0001.2]
   bd-0001.4: Service layer (600 LOC, 4-5h) [BLOCKED by bd-0001.3]
   bd-0001.5: API endpoints (400 LOC, 2-3h) [BLOCKED by bd-0001.4]

Execution order: bd-0001.1 → bd-0001.2 → bd-0001.3 → bd-0001.4 → bd-0001.5

# Exit plan mode, get approval...

# Check what's ready
bd ready

# Output:
Ready tasks:
- bd-0001 (parent)
- bd-0001.1 (Domain model)
- bd-0001.2 (Database schema)

# Start execution (manual)
@build bd-0001.1

# Or autonomous execution with correct dependency order
@oneshot bd-0001

# After completion, bd-0001.3 automatically becomes ready!
bd ready

# Output:
Ready tasks:
- bd-0001
- bd-0001.3 (Repository layer)
```

## Key Principles

**Decomposition Strategy:**
1. **Sequential by default** - Each WS blocks the next (safe, simple)
2. **Size matters** - Keep workstreams SMALL/MEDIUM (< 500 LOC)
3. **Dependencies explicit** - Use BeadsDependency.BLOCKS for sequencing
4. **Parallel when possible** - Independent tasks can use same sequence number
5. **Plan mode first** - Explore codebase before presenting plan (NEW)

**Beads Integration:**
1. **Hash-based IDs** - No conflicts, auto-generated
2. **Parent-child** - `parent_id` links workstreams to feature
3. **Native DAG** - Beads manages dependency graph
4. **Ready detection** - `bd ready` shows executable tasks
5. **Enhanced metadata** - LOC, duration, oneshot_ready flags (NEW)

**Workstream Sizing:**
- **SMALL:** < 500 LOC, < 1500 tokens
- **MEDIUM:** 500-1500 LOC, 1500-5000 tokens
- **LARGE:** > 1500 LOC → Break into 2+ workstreams

**Execution Graphs (NEW):**
- Topological sort ensures correct dependency order
- Mermaid diagrams for visualization
- Oneshot ready flag for autonomous execution
- Estimated metrics for planning

## Migration from Markdown Workflow

**Old workflow:**
```bash
@design idea-add-auth
# → docs/workstreams/backlog/WS-001-01.md
# → docs/workstreams/backlog/WS-001-02.md
# ...
```

**New Beads + ai-comm workflow:**
```bash
@design bd-0001
# → bd-0001.1 (Domain) with execution metadata
# → bd-0001.2 (Repository) with execution metadata
# → bd-0001.3 (Service) with execution metadata
# + Execution graph for @oneshot
```

**Benefits:**
- No manual ID allocation (hash-based, automatic)
- Multi-agent ready (execute WS in parallel)
- Built-in ready detection (no manual scripts)
- Automatic unblocking (complete WS1 → WS2 becomes ready)
- Interactive planning with EnterPlanMode (NEW)
- Execution graphs for correct ordering (NEW)
- Enhanced metadata for estimation (NEW)

## Troubleshooting

**No workstreams created:**
```bash
# Check parent task exists
bd show bd-0001

# Check decomposer error logs
export DEBUG=1
```

**Dependencies incorrect:**
```bash
# View task details
bd show bd-0001.2

# Verify dependencies
bd dep list bd-0001.2
```

**Tasks not becoming ready:**
```bash
# Check blocking tasks
bd ready

# View dependency graph
bd graph bd-0001
```

**Execution order wrong (NEW):**
```python
# Check topological sort
from sdp.design.graph import DependencyGraph

graph = DependencyGraph()
# ... load workstreams ...
print(graph.topological_sort())
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `@design bd-0001` | Decompose into workstreams with execution graph |
| `@think "architecture"` | Deep analysis before @design (NEW) |
| `bd show {id}` | View task/workstream details |
| `bd ready` | List ready tasks |
| `bd dep list {id}` | List dependencies |
| `bd graph` | Show dependency graph (NEW) |
| `@build {ws_id}` | Execute workstream |
| `@oneshot {feature_id}` | Autonomous execution with graph (NEW) |

---

**Version:** 2.1.0-beads-ai-comm
**Status:** Beads + AI-Comm Integration
**See Also:** `@idea`, `@build`, `@oneshot`, `@think`
