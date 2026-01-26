# Developer Dashboard Design

> **Status:** Design approved
> **Date:** 2026-01-26
> **Feature:** F012 extension (Developer Dashboard)
> **Goal:** Unified TUI dashboard for workstreams + test results with fast feedback

---

## Overview

Developer Dashboard — это расширение F012, которое предоставляет единый TUI интерфейс для:
- Просмотра состояния всех workstreams (ideas, backlog, in_progress, completed)
- Мониторинга тестов в реальном времени (watch mode)
- Отслеживания активности агентов

**Key principle:** Dashboard Core — reusable компоненты, используемые и в dashboard, и в monitor (00-012-08).

---

## Architecture

### Layer 1: Data Sources

| Component | Responsibility | Update Mechanism |
|-----------|----------------|------------------|
| `WorkstreamReader` | Scan workstream dirs, parse YAML | Polling (1-2s) |
| `TestRunner` | Watch files, run pytest, parse output | File watcher (instant) |
| `AgentReader` | Read from daemon queue | Daemon events |

### Layer 2: State Management

```python
@dataclass
class DashboardState:
    workstreams: dict[str, WorkstreamState]
    test_results: TestResults
    agent_activity: list[AgentEvent]
    last_update: datetime

class StateBus:
    """Pub/sub for state updates"""
    def subscribe(callback: Callable[[DashboardState], None]) -> None
    def publish(state: DashboardState) -> None
```

### Layer 3: UI Components (Textual)

Reusable widgets:
- `WorkstreamTree` — tree of workstreams by status/project
- `TestPanel` — test results + coverage bar
- `ActivityLog` — scrolling event log

### Layer 4: CLI Integration

```bash
sdp dashboard      # Launch developer dashboard
sdp monitor        # Launch agent monitor (uses same widgets)
```

---

## File Structure

```
src/sdp/dashboard/
├── __init__.py
├── state.py              # DashboardState, StateBus
├── sources/
│   ├── __init__.py
│   ├── workstream_reader.py   # ~150 LOC
│   ├── test_runner.py         # ~200 LOC
│   └── agent_reader.py        # ~100 LOC
└── widgets/
    ├── __init__.py
    ├── workstream_tree.py     # ~200 LOC
    ├── test_panel.py          # ~150 LOC
    └── activity_log.py        # ~100 LOC

src/sdp/dashboard/
└── dashboard_app.py     # Main TUI app ~250 LOC

src/sdp/monitor/
└── monitor_app.py       # Reuses dashboard widgets ~200 LOC

tests/unit/dashboard/
├── test_state.py
├── test_sources.py
└── test_widgets.py
```

**Total estimated:** ~1,600 LOC (MEDIUM workstream count: 3-4 WS)

---

## Data Flow

### Initialization

```
sdp dashboard
  ↓
DashboardApp.__init__()
  ↓
1. Create StateBus
2. Spawn Data Sources (as async tasks):
   - WorkstreamReader → polls every 1s
   - TestRunner → starts file watcher
   - AgentReader → connects to daemon (optional)
3. Create Widgets (subscribe to StateBus)
4. Start Textual app
```

### Runtime Update (test file changed)

```
[File saved in src/ or tests/]
  ↓
watchdog detects change
  ↓
Run pytest --tb=short --cov-report=json
  ↓
Parse output → TestResults object
  ↓
StateBus.publish(DashboardState(updated=test_results))
  ↓
TestPanel widget updates
  ↓
Textual re-renders (1-2ms)
```

### Workstream Update

```
[Every 1s]
  ↓
Scan docs/workstreams/{backlog,in_progress,completed}/
  ↓
Parse YAML frontmatter
  ↓
If changed: StateBus.publish(...)
  ↓
WorkstreamTree re-renders
```

---

## UI Layout (Tab-based + Hotkeys)

```
┌─────────────────────────────────────────────────────────────┐
│  SDP Dashboard                                      [F012]  │
├─────────────────────────────────────────────────────────────┤
│                                                                  │
│  [Workstreams] [Tests] [Activity]                               │
│  ───────────────────────────────────────────────────────────  │
│                                                                  │
│  ┌─ Workstreams ─────────────────────────────────────────┐    │
│  │ 📁 Ideas (2)                                            │    │
│  │   ├─ idea-user-auth [draft]                           │    │
│  │   └─ idea-github-agent [needs_review]                 │    │
│  │                                                        │    │
│  │ 📁 Backlog (15)                                         │    │
│  │   ├─ 00-012-01: Daemon Framework [SMALL]              │    │
│  │   ├─ 00-012-02: Task Queue [SMALL]                    │    │
│  │   └─ 00-012-03: GitHub Sync [MEDIUM]                  │    │
│  │                                                        │    │
│  │ 📁 In Progress (3)                                     │    │
│  │   └─ 00-011-06: PRD Command [assignee: @user]         │    │
│  │                                                        │    │
│  │ 📁 Completed (40)                                       │    │
│  │   └─ 00-011-05: Examples ✅                            │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
│  Press: [w]orkstreams [t]ests [a]ctivity [q]uit                │
└─────────────────────────────────────────────────────────────┘
```

**Hotkeys:**
- `1`, `w` — Workstreams tab
- `2`, `t` — Tests tab
- `3`, `a` — Activity tab
- `q` — Quit
- `r` — Force refresh

---

## Tabs Detail

### Workstreams Tab

- Tree view grouped by status (Ideas, Backlog, In Progress, Completed)
- Each workstream shows: WS-ID, title, size, assignee (if any)
- Color coding: yellow=backlog, blue=in_progress, green=completed
- Filter by: status, feature, project, assignee

### Tests Tab

- Summary: `PASSED 42 | FAILED 2 | SKIPPED 1 | 87% coverage`
- Failing tests list (expandable for error details)
- Coverage bar (color: red<60%, yellow 60-80%, green>80%)
- Last run timestamp
- "Run all" button

### Activity Tab

- Scrolling log of events:
  - Git hooks (pre-build, post-build)
  - Daemon events (agent started, completed, error)
  - Workstream state changes
- Color coded: info=blue, success=green, error=red

---

## Error Handling

**Graceful degradation at each layer:**

| Layer | Error Strategy |
|-------|----------------|
| WorkstreamReader | Return cached state on parse error, log warning |
| TestRunner | Return TestResults(status="error") on failure |
| AgentReader | Return None if daemon not running (disable tab) |
| Widgets | Render error message in-place, don't crash app |

**Example:**

```python
async def read_workstreams() -> dict[str, WorkstreamState]:
    try:
        return parse_yaml_files()
    except YAMLError as e:
        logger.warning(f"Invalid YAML: {e}")
        return self._cached_state  # Don't crash dashboard
```

---

## Dependencies

### New Python Packages

```toml
[project.dependencies]
textual = ">=0.80.0"      # TUI framework
watchdog = ">=4.0.0"      # File watcher for test runner
```

### Internal Dependencies

- Uses `WorkstreamState` from existing workstream module (if available)
- Connects to daemon queue from 00-012-02 (optional)
- Reuses logging configuration from `src/sdp/logging.py`

---

## Testing Strategy

### Unit Tests (pytest)

- `test_state.py` — StateBus publish/subscribe
- `test_workstream_reader.py` — YAML parsing, state building
- `test_test_runner.py` — pytest output parsing, file change detection
- `test_widgets.py` — Widget update logic (no TUI rendering)

### Integration Tests

- `test_dashboard_flow.py` — Full update cycle (sources → state → widgets)

### Manual Smoke Test

```bash
# Terminal 1
sdp dashboard

# Expected:
# - Tab 1 shows workstreams tree
# - Tab 2 shows test status
# - Press 'w', 't', 'a' to switch tabs

# Terminal 2 (test watch mode)
echo "def test_broken(): assert False" >> tests/test_x.py
# Tab 2 should update within 2s showing FAILED
```

---

## Success Criteria

- [ ] `sdp dashboard` launches TUI
- [ ] Workstreams tab shows all workstreams grouped by status
- [ ] Tests tab shows real-time test results
- [ ] File changes in src/ or tests/ trigger test run within 2s
- [ ] Activity tab shows daemon events (when daemon running)
- [ ] Hotkeys (w/t/a/q) switch tabs/quit
- [ ] Works without daemon (graceful degradation)
- [ ] Coverage ≥ 80%
- [ ] mypy --strict passes

---

## Next Steps

1. Create detailed workstreams for F012 extension:
   - 00-012-11: Dashboard Core (state, sources)
   - 00-012-12: Dashboard Widgets (textual components)
   - 00-012-13: Dashboard App (main TUI)
   - 00-012-14: Update Monitor to use Dashboard Core

2. Update 00-012-08 (Rich TUI Monitor) to depend on Dashboard Core

3. Integration testing with existing F012 components

---

**Version:** 1.0
**Author:** SDP Design Session
**Related:** F012 (GitHub Agent Orchestrator), Analysis document (2025-01-26-sdp-analysis-design.md)
