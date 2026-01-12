# Strategic Code Review (Principal Python Architect & Security Auditor)

Date: 2026-01-06  
Scope: `tools/hw_checker/` (Clean Architecture grading system; DinD sandbox; FastAPI API; Redis workers; Postgres portal)  
Threat model: hostile student code attempting container escape, secret exfiltration, resource exhaustion, and supply-chain abuse.

---

## 📊 1. Executive Health Dashboard

- **Overall Quality Score (0-10): 6.0**
  - Strong foundations: Clean Architecture intent, high type-hint coverage, meaningful middleware, quality-gate compose.
  - Major blockers: security posture is not deploy-safe (DinD privileged, host Docker socket mount), secrets handling is dangerous, and a core module contains a syntax error that breaks static tooling.

- **AI-Readiness Score (0-10): 4.5**
  - Code is *typed* (≈95–97% fully typed), but the repo violates the “One Screen” rule heavily (many 500–1200 line files).
  - Several “god-functions” exceed complexity thresholds (C901), raising edit-risk for smaller models.

- **Security Posture: VULNERABLE**
  - Critical sandbox escape vectors exist (privileged DinD, host docker socket mount).
  - Real credential artifacts are present in-repo (even if gitignored locally).

- **Top 3 Strategic Risks**
  - **Sandbox escape / host compromise** via DinD `privileged=True` and Docker socket access.
  - **Credential compromise** due to committed OAuth token material + code paths that “look for it”.
  - **Maintenance bottleneck** from massive files + high-complexity functions → slows iteration and increases regression risk.

---

## 🛡️ 2. Security Audit Report

| Severity | Finding | Impact | File/Line | Remediation |
|----------|---------|--------|-----------|-------------|
| **CRITICAL** | Host Docker socket mounted into control-plane container | Any process in that container can control the host Docker daemon → host compromise; can start privileged containers, mount host FS, exfiltrate secrets | `tools/hw_checker/docker-compose.yml:151` and `tools/hw_checker/docker-compose.test.yml:201` (`/var/run/docker.sock`) | Remove socket mount for production. Use a **dedicated remote Docker daemon** (separate VM) or a hardened sandbox runtime (gVisor/Kata/Sysbox). If socket is unavoidable, run isolated host + strict policy around who can exec in the launcher container. |
| **CRITICAL** | DinD containers are created with `privileged=True` | Kernel attack surface expanded; seccomp/AppArmor effectively bypassed; container escape becomes much more feasible | `src/hw_checker/infrastructure/dind/docker_client.py:345` | Replace privileged DinD with **rootless** or **Sysbox** DinD; apply restrictive `security_opt` + `cap_drop` + `no-new-privileges`. Add `pids_limit`, ulimits, and a seccomp profile. |
| **CRITICAL** | Real OAuth credential artifacts exist in repo directory | Risk of account compromise and data exfiltration if repo ever published/shared; local dev machines may leak tokens | `tools/hw_checker/secrets/*` and `tools/hw_checker/secrets/tokens/access_token.json` | Rotate/revoke tokens immediately; move secrets to a secret manager; add pre-commit secret scanning; ensure CI blocks secrets. |
| **HIGH** | Hardcoded “standard locations” for credential discovery | Encourages keeping credentials in repo path; makes accidental inclusion more likely; complicates secret rotation | `src/hw_checker/infrastructure/credential_resolver.py:57-62`; `src/hw_checker/application/run_homework/result_builder.py:169-183` | Remove repository-relative default credential paths. Require explicit `GOOGLE_APPLICATION_CREDENTIALS` or config injection only. |
| **HIGH** | Control-plane container default API token in compose | If used outside dev, predictable token → unauthorized access to operational endpoints | `tools/hw_checker/docker-compose.yml:25` (`HW_CHECKER_API_TOKEN=${...:-test-token-for-development}`) | Remove insecure default; require explicit token; support proper auth (OIDC/service-to-service) or at least long random tokens and rotation. |
| **HIGH** | DinD containers can reach host network alias | Mapping `host.docker.internal` to gateway allows host service access from DinD; expands attack surface (SSRF / pivot) | `src/hw_checker/infrastructure/dind/docker_client.py:328-346` | Default-deny host access; only allow explicit upstreams (e.g., Nexus) via dedicated internal network; avoid “host gateway” mapping. |
| **MEDIUM** | Command construction uses string interpolation for in-container scripts | If any interpolated part becomes attacker-controlled (env/config), can create command injection | `src/hw_checker/infrastructure/dind/executor.py:453-478` (f-strings building shell/python commands) | Build config via mounted file or `put_archive` JSON payload; validate URLs; avoid shell quoting pitfalls. |
| **MEDIUM** | SQLite update uses f-string for placeholders | Pattern is safe if placeholders are only “?” repeated, but bandit flags it; risk grows if string pieces become untrusted | `src/hw_checker/infrastructure/status_store.py:572-579` | Keep placeholder generation isolated; ensure `stale_workers` are validated worker IDs; consider `executemany` or temp table strategy. |
| **MEDIUM** | Git “safe.directory” wildcard for `/tmp/*` | Expands trust boundary; could enable confusing git behavior with attacker-controlled dirs | `src/hw_checker/infrastructure/git_operations.py:74-81` | Avoid global wildcard; scope safe.directory to the exact repo path; use per-repo git config if possible. |
| **MEDIUM** | Logging config silently disables file logging on errors | Weakens audit trail; makes incident response harder | `src/hw_checker/infrastructure/logging_config.py:84-112` | Do not `pass` on handler creation failures; emit explicit warning/error with path and exception; expose a health check for log sinks. |

---

## 🧩 3. Architecture & Modularity Analysis

### Files Exceeding "One Screen" Rule (>200 lines)

Sample (top offenders, Python only, `src/hw_checker`):
- `src/hw_checker/application/run_homework.py` — **1260** lines (also contains syntax error; see below)
- `src/hw_checker/application/sampling_validators.py` — **986**
- `src/hw_checker/cli/run_local.py` — **927**
- `src/hw_checker/infrastructure/dind/executor.py` — **922**
- `src/hw_checker/infrastructure/publisher.py` — **920**
- `src/hw_checker/cli/workers.py` — **799**
- `src/hw_checker/application/saga_orchestrator.py` — **631**
- `src/hw_checker/infrastructure/status_store.py` — **584**

Also, there is a second parallel code root:
- `tools/hw_checker/hw_checker/infrastructure/dind/executor.py` — **1193** lines

**Risk:** duplicated/parallel implementations + huge modules create cognitive load and increase “AI hallucination” risk during edits.

### Complex Functions (Complexity > 8)

Evidence from Ruff McCabe (C901):
- `src/hw_checker/application/saga_orchestrator.py:85` — `execute` complexity **37**
- `src/hw_checker/application/sampling_validators.py:662` — `validate` complexity **37**
- `src/hw_checker/application/sampling_validators.py:403` — `_sample_mlflow_inference` complexity **35**
- `src/hw_checker/infrastructure/dind/executor.py:378` — `_setup_environment` complexity **33**
- `src/hw_checker/cli/run_local.py:524` — `run` complexity **44**
- `src/hw_checker/application/stages/docker_cleanup.py:19` — `cleanup_docker_compose` complexity **46**

### Coupling Issues (violations that block isolated testing)

- **Domain reads environment** (infrastructure concern leaks inward):
  - `src/hw_checker/domain/dind.py:20-37` uses `os.environ` to compute resource limits.
  - Recommendation: move env-reading into infrastructure config service; keep Domain as pure value objects.

- **Infrastructure uses host Docker CLI from inside worker process**:
  - `src/hw_checker/infrastructure/dind/executor.py:423-437` uses `subprocess.run(["docker", "inspect", ...])`
  - Recommendation: use injected `DockerClientPort` APIs for inspection, or a dedicated “HostIntrospectionPort”.

### Missing Abstractions (to decouple layers)

- `DockerSecurityPolicy` (domain-level intent) + `DockerRuntimeOptions` (infra implementation):
  - Centralize `privileged`, `cap_drop`, `security_opt`, `pids_limit`, ulimits, network, DNS.
- `CredentialSourcePort`:
  - Resolve credentials via env/config/secret manager, never via repo-relative fallbacks.
- `CommandBuilder` + `ContainerFileWriterPort`:
  - Avoid shell f-strings; write files via tar/put_archive to reduce injection surface.

---

## 📝 4. Code Quality Report

### Linter / Static Tooling

- **Ruff C901** shows many high-complexity hotspots (see above).
- **Ruff parse failure**: `src/hw_checker/application/run_homework.py` triggers SyntaxError:
  - The module claims to be a re-export wrapper, but also contains stray indented class body without a `class` statement.
  - This breaks Ruff and Bandit AST parsing for that file, weakening quality gates.

### DRY Violations / Duplicate Logic

- Parallel DinD executor implementations exist under both `src/hw_checker/...` and `hw_checker/...`.
  - **Risk:** divergent behavior in prod vs tests, duplicated fixes, and inconsistent security posture.

### SOLID / Clean Architecture

- **DIP violation**: Domain depends on env (`domain/dind.py`).
- **SRP risk**: `infrastructure/dind/executor.py:_setup_environment` mixes:
  - docker daemon config, nexus discovery, file writing, retries, logging, and verification in one method.

### Type Hints Coverage

Objective AST scan (`src/hw_checker`):
- **All functions**: 812 / 850 fully typed (**95.5%**)
- **Public functions**: 604 / 623 fully typed (**97.0%**)

This is a strong baseline; next gains come from reducing file size/complexity and tightening security invariants.

---

## 🔍 5. Observability & Documentation Gaps

### Logging Issues

- **Not actually JSON**: `HW_CHECKER_LOG_FORMAT=json` is set in compose, but current `setup_logging()` uses plain `logging.Formatter` and does not branch on format.
- **Audit trail gaps**:
  - API logs include `request_id`, but do not consistently include domain identifiers (submission_id, run_id, worker_id) in a structured, end-to-end way.
  - Some error paths still use `warnings.warn(...)` (e.g., compensation in `application/run_homework.py`), which bypasses central structured logging.

### Missing Documentation

- A security-oriented “sandbox hardening” README is missing at the module boundary where it matters:
  - `src/hw_checker/infrastructure/dind/` should document isolation guarantees, required Docker daemon configuration, and threat-model assumptions.

### Proposed ADR (draft titles)

- **ADR-00X: DinD Execution Security Model (Privileged vs Rootless vs Sysbox vs gVisor)**
- **ADR-00Y: Secret Handling Policy (No repo-relative secrets; mandatory secret manager integration)**
- **ADR-00Z: Observability Contract (correlation ids across API → queue → worker → container)**

---

## 🗺️ 6. Refactoring Roadmap (Prioritized Backlog)

### Phase 1: Critical Fixes (Week 1-2)

- [ ] **[SECURITY]** Eliminate host Docker socket mount in production path
  - Replace with remote executor host, or sandbox runtime with hardened daemon.
  - Update deployment docs accordingly.
- [ ] **[SECURITY]** Remove `privileged=True` DinD and implement hardened container security policy
  - Require `no-new-privileges`, `cap_drop=ALL`, explicit `cap_add` only if required.
  - Add `pids_limit`, ulimits, and a custom seccomp profile.
- [ ] **[SECURITY]** Rotate/revoke all Google OAuth tokens and remove any secret artifacts from repo history
  - Add automated secret scanning (CI + pre-commit).
- [ ] **[BLOCKER]** Fix `src/hw_checker/application/run_homework.py` syntax error wrapper
  - It must be a minimal re-export only; no stray code.

### Phase 2: Architecture Cleanup (Month 1)

- [ ] **[REFACTOR]** Split top offenders to ≤200 lines with explicit submodules
  - `infrastructure/dind/executor.py`, `application/saga_orchestrator.py`, `application/stages/docker_cleanup.py`, CLI modules.
- [ ] **[ARCH]** Remove domain env-reading (`domain/dind.py:from_env`) → move to infra config service
  - Replace with injected `DinDResourceLimits` value object.
- [ ] **[REFACTOR]** Deduplicate dual code roots (`src/hw_checker` vs `hw_checker/`)
  - Keep one canonical implementation; delete or archive the other.

### Phase 3: Optimization & Scaling (Month 2-3)

- [ ] **[OBSERVABILITY]** End-to-end correlation IDs
  - Propagate `request_id` into job metadata → worker logs → container logs.
- [ ] **[PERFORMANCE]** Reduce expensive subprocess calls on hot paths
  - Replace `docker inspect` shell-outs with Docker SDK calls via `DockerClientPort`.
- [ ] **[RELIABILITY]** Harden timeouts and cancellation for container exec
  - Ensure exec processes are terminated (or the container is force-killed on timeout).

---

## 💎 7. Gold Standard Example

### Selected Hotspot

`src/hw_checker/infrastructure/dind/executor.py:_setup_environment` (Ruff C901 complexity 33) — currently mixes:
network inspection, daemon.json templating via f-strings, retries, verification, and logging.

### Original (excerpt)

```python
# src/hw_checker/infrastructure/dind/executor.py (excerpt around daemon.json creation)
create_daemon_json_cmd = f"""python3 -c "import json, os; d={{'iptables': False, 'ip-forward': True, 'registry-mirrors': ['{docker_registry_mirror}']}}; os.makedirs('/etc/docker', exist_ok=True); open('/etc/docker/daemon.json', 'w').write(json.dumps(d, indent=2))" """
result = self._docker_client.exec_command(
    container_id=self._container_id,
    command=create_daemon_json_cmd,
    timeout=DOCKER_EXEC_SHORT_TIMEOUT,
)
```

### Refactored (demonstration-grade)

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
from urllib.parse import urlparse


class DockerClientPort(Protocol):
    def exec_command(self, container_id: str, command: str, timeout: int): ...


@dataclass(frozen=True)
class DaemonConfig:
    registry_mirror_url: str
    iptables: bool = False
    ip_forward: bool = True

    def validate(self) -> None:
        parsed = urlparse(self.registry_mirror_url)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("registry_mirror_url must be http(s)")
        if not parsed.netloc:
            raise ValueError("registry_mirror_url must include host:port")


@dataclass(frozen=True)
class DockerDaemonConfigurator:
    docker: DockerClientPort
    container_id: str
    timeout_seconds: int

    def write_daemon_json(self, cfg: DaemonConfig) -> None:
        cfg.validate()
        # Avoid shell quoting: generate JSON inside Python with controlled literal
        cmd = (
            "python3 - <<'PY'\n"
            "import json, os\n"
            "cfg = {\n"
            f"  'iptables': {str(cfg.iptables)},\n"
            f"  'ip-forward': {str(cfg.ip_forward)},\n"
            f"  'registry-mirrors': [{cfg.registry_mirror_url!r}],\n"
            "}\n"
            "os.makedirs('/etc/docker', exist_ok=True)\n"
            "with open('/etc/docker/daemon.json', 'w', encoding='utf-8') as f:\n"
            "  json.dump(cfg, f, indent=2)\n"
            "print('OK')\n"
            "PY"
        )
        res = self.docker.exec_command(
            container_id=self.container_id,
            command=cmd,
            timeout=self.timeout_seconds,
        )
        if getattr(res, 'exit_code', None) != 0:
            raise RuntimeError(f'Failed to write daemon.json (exit_code={getattr(res, \"exit_code\", None)})')
```

### Improvements Made

- **Type hints**: explicit dataclasses + Protocol for dependencies.
- **Linear logic**: one responsibility per method (validate → write → check).
- **Reduced injection surface**: URL validated; JSON generated deterministically; avoids fragile quoting.
- **Structured error handling**: explicit failure path with actionable message.
- **Extensible**: security policy can evolve without touching orchestration flow.

---

## Final Directive

🚨 **"STOP. Security vulnerabilities found. Do not deploy."**


