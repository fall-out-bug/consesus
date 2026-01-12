# Strategic Planning Document: HW Checker Audit 2026

## 📊 1. Executive Health Dashboard
- **Overall Quality Score (0-10):** 7.5
  - *Justification:* Solid architecture foundations (Clean Architecture, SAGA pattern), good test coverage, and clear domain logic. However, critical violations of modularity ("God Classes") and "magic" metaprogramming in infrastructure layers pose maintenance risks.
- **AI-Readiness Score (0-10):** 6.0
  - *Justification:* Large files (>1000 lines) and complex string-based code generation in `executor.py` make it difficult for lightweight models (Haiku) to safely edit without losing context or introducing regressions.
- **Security Posture:** VULNERABLE
  - *Justification:* Default credentials in `docker-compose.yml` and extensive use of `docker.sock` in `worker-launcher` require hardening.
- **Top 3 Strategic Risks:**
  1.  **Maintenance Bottleneck:** `RunHomeworkUseCase` (1260 lines) and `DinDExecutorAdapter` (1193 lines) concentrate too much logic, making them risky to modify.
  2.  **Security Defaults:** Default API tokens and DB passwords in `docker-compose.yml` risk production exposure if not strictly overridden.
  3.  **Fragile Infrastructure Logic:** The "magic string" Python script generation in `executor.py` is brittle and hard to test/debug.

## 🛡️ 2. Security Audit Report
| Severity | Finding | Impact | File/Line | Remediation |
|----------|---------|--------|-----------|-------------|
| HIGH | Default API Token | Production systems might deploy with known default token if env var missing. | `docker-compose.yml:25` | Remove default value `test-token-for-development`. Fail startup if `HW_CHECKER_API_TOKEN` is unset. |
| HIGH | Default DB Password | Database accessible with known default password. | `docker-compose.yml:69` | Remove default `hw_checker_dev`. Require explicit `POSTGRES_PASSWORD` env var. |
| MEDIUM | Docker Socket Mount | `worker-launcher` has full root access to host Docker daemon. | `docker-compose.yml:151` | Ensure `worker-launcher` is running with least privilege necessary, or use a secure Docker socket proxy to limit allowed API calls. |
| LOW | Magic String Code Injection | Runtime code generation via string concatenation obscures execution logic. | `executor.py:673` | Move `setup_env.py` logic to a standalone Python file in the image or mount it as a config map/volume. |

## 🧩 3. Architecture & Modularity Analysis
- **Files Exceeding "One Screen" Rule:**
  - `tools/hw_checker/src/hw_checker/application/run_homework.py`: 1260 lines (Critical)
  - `tools/hw_checker/tests/test_application_saga_orchestrator_integration.py`: 1197 lines (Critical)
  - `tools/hw_checker/hw_checker/infrastructure/dind/executor.py`: 1193 lines (Critical)
  - `tools/hw_checker/src/hw_checker/application/sampling_validators.py`: 986 lines
  - `tools/hw_checker/src/hw_checker/cli/run_local.py`: 927 lines
- **Complex Functions (Complexity > 8):**
  - `DinDExecutorAdapter._setup_environment` (`executor.py`): Extremely high cognitive load due to nested string building and multi-language injection (Python generating Python/Shell).
  - `RunHomeworkUseCase.run` (`run_homework.py`): Orchestrates too many stages (validation, execution, sampling, publishing, cleanup) in a single method.
- **Coupling Issues:**
  - `RunHomeworkUseCase` is coupled to almost every port in the system, making it a "God Class". It should be broken down into individual Stage Use Cases (which seems to have started with `_stage_1_validate` etc., but they are still methods on the same class).

## 📝 4. Code Quality Report
- **Linter Violations:**
  - `run_homework.py`: imports are likely not sorted/grouped perfectly given the file size.
  - `runs_router.py`: `rerun_run` returns `dict` instead of a typed Pydantic model.
- **DRY Violations:**
  - `_prepare_env_vars` logic appears partially duplicated between `executor.py` and `container_lifecycle.py`.
- **SOLID Violations:**
  - **SRP Violation:** `RunHomeworkUseCase` handles SAGA orchestration, error publishing, artifact mirroring, AND business logic. It should be a pure Orchestrator delegating to specialized handlers.
  - **SRP Violation:** `DinDExecutorAdapter` handles container lifecycle, network management, AND script injection.
- **Type Hints Coverage:**
  - Generally good (>90%).
  - Exception: `runs_router.py` returns `dict` in `rerun_run` (line 206).

## 🔍 5. Observability & Documentation Gaps
- **Logging Issues:**
  - `executor.py` logs "last 2000 chars" of output manually. This should be handled by a structured log collector or sidecar, not inline application logic.
- **Missing Documentation:**
  - `run_homework.py` has a docstring but the class is so large the docstring cannot cover all behaviors adequately.
- **Proposed ADR:**
  - **ADR-002: Decomposition of RunHomeworkUseCase**: Split the monolith use case into a true SAGA orchestrator and atomic Step Executors.
  - **ADR-003: Infrastructure Script Management**: Replace inline string-built scripts with baked-in container scripts or mounted ConfigMaps.

## 🗺️ 6. Refactoring Roadmap (Prioritized Backlog)

### Phase 1: Critical Fixes (Week 1-2)
- [ ] **[SECURITY]** Remove default credentials from `docker-compose.yml`. Force explicit env vars.
- [ ] **[SECURITY]** Audit `worker-launcher` privileges.
- [ ] **[REFACTOR]** Fix `runs_router.py` to return Pydantic models instead of `dict`.

### Phase 2: Architecture Cleanup (Month 1)
- [ ] **[REFACTOR]** Extract `setup_env.py` generation from `executor.py` into a static resource file.
- [ ] **[REFACTOR]** Split `RunHomeworkUseCase` into `HomeworkOrchestrator` and separate classes for each stage (`ValidateStage`, `ExecuteStage`, etc.) to reduce file size.
- [ ] **[TEST]** Split `test_application_saga_orchestrator_integration.py` into per-scenario test files.

### Phase 3: Optimization & Scaling (Month 2-3)
- [ ] **[OBSERVABILITY]** Implement centralized log collection (ELK/Loki) instead of file-based `run.log`.
- [ ] **[PERFORMANCE]** Optimize Docker image size (currently ~1.4GB mentioned in docs) to speed up worker spawning.

## 💎 7. Gold Standard Example

**Problematic Code (`executor.py` - Inline Script Generation):**
*Current implementation generates a Python script as a string, which is error-prone, hard to read, and hard to lint.*

```python
        # ... (lines 673-800 of executor.py)
        setup_script_lines = [
            "import sys",
            "import os",
            # ... hundreds of lines of string literals ...
            "    print('✅ Environment setup completed (pip, apt, apk, maven, curl/wget)')",
        ]
        setup_script = '\n'.join(setup_script_lines)
```

**Refactored Version (Gold Standard):**
*Use a separate file resource and read it, or better yet, bake it into the image. Here is the code-side improvement using a resource loader pattern.*

```python
from importlib import resources
from pathlib import Path
from typing import Dict
from ...infrastructure import scripts  # Package containing the scripts

def _get_setup_script(self, env_vars: Dict[str, str]) -> str:
    """
    Load the setup script and inject configuration.
    
    Instead of constructing code as strings, we read a valid, linted Python 
    file and inject configuration via environment variables or templating 
    (only where strictly necessary).
    """
    # Read the static script file (which is linted and tested separately)
    # Assuming 'setup_env.py' exists in the 'scripts' package
    script_content = resources.read_text(scripts, "setup_env.py")
    
    # We rely on environment variables passed to the container rather than 
    # string interpolation into the script source code.
    # This keeps the script static and cacheable.
    
    return script_content

def _setup_environment(self, container_id: str, network_name: str) -> None:
    # ... setup logic ...
    
    # 1. Get the static script content
    script_content = self._get_setup_script({})
    
    # 2. Write to container (using tar/put_archive as before)
    self._write_file_to_container(container_id, "/tmp/setup_env.py", script_content)
    
    # 3. Execute with environment variables
    # The variables are passed to the PROCESS, not baked into the SCRIPT
    env_vars = self._prepare_env_vars("setup")
    self._execute_command_with_env(container_id, ["python3", "/tmp/setup_env.py"], env_vars)
```

**Improvements:**
1.  **Static Analysis:** The `setup_env.py` can be a real file in the repo, checked by Ruff/Black/MyPy.
2.  **Security:** No risk of injection via f-strings in code generation.
3.  **Readability:** No mixed quoting or indentation math in Python strings.
4.  **Separation of Concerns:** Configuration is passed via Env Vars (runtime), not Code Generation (build time).

---

# Final Directive
⚠️ **"Address Phase 1 Critical Fixes before adding features."**

