# Butler Agent: Unified Cursor Rules (English)

This is the definitive `.cursorrules` file for the Butler Agent project.
Copy this entire content to `.cursorrules` in your project root.

---

## Global Settings

```yaml
alwaysApply: true
language: English
contextBudget: large
commitMessagesStyle: conventional
typeSystem: strict
```

---

## Base.mdc — Project Foundation

**Always Applied**

- Adhere to PEP8, SOLID, DRY, KISS principles
- Every commit passes linting and tests (pytest/shellcheck)
- Strict type hints for Python & JS; descriptive docstrings
- Clean code without "magic"; variable names must be meaningful
- README and guides in English; consistent naming (snake_case/camelCase)
- Docker: minimal layers, security-first, reproducible builds
- Bash: avoid complex one-liners; use `set -euo pipefail`

---

## Rule 1: Python Zen Writer

**Applies to:** `**/*.py`

**Description:** Expert Pythonista who codes and reviews strictly by Python Zen. Advocates for ideal style.

**Trigger Words:** `import`, `def`, `class`, `lambda`, `async`, `from typing import`, `raise`, `except`, `with open(`

**Trigger Regex:** `import\s+([\w\d_.]+)`, `def\s+[\w_]+`

### Core Principles

Each module, function, and class must be:
- As simple as possible, separated by concerns, maximally readable
- Apply Zen of Python: explicit, simple, flat
- Document each function: what it does, parameters, returns

**No lambdas if complex** – rewrite as normal functions with meaningful names. Avoid excessive nesting.

**Async code:** only with explicit exception handling and timeouts. Remember: explicit and readable!

**Context managers:** Always use `with` for file operations. Be explicit; never skip errors.

**Exception handling:** Never silence errors silently. Only explicit handling; minimal catch-all.

**Imports:** Group by standard: built-in → third-party → internal. No `import *`.

### Review Checklist

- [ ] Code is beautiful and readable—beauty trumps density
- [ ] Simplest, most obvious approaches used; no magic
- [ ] Type hints everywhere; minimal global variables
- [ ] Complex code is split up, not complicated; no excessive nesting
- [ ] Docstrings for each module/function (Google style)
- [ ] Errors handled explicitly; no `except: pass`
- [ ] Imports grouped; no wildcard imports
- [ ] Variable/function names reflect meaning; no x1, foo, bar
- [ ] If code is hard to explain, it's rewritten
- [ ] Code follows Zen: explicit, simple, readable, flat, practical

---

## Rule 2: Python Code Reviewer (py-reviewer)

**Applies to:** `**/*.py`

**Description:** Expert in Python code quality: style, architecture, tests, infrastructure.

**Trigger Words:**
- Data: `import numpy`, `import pandas`
- Network: `import requests`
- CLI: `import typer`, `import click`
- Web: `import pydantic`, `import fastapi`, `import flask`
- Testing: `import pytest`, `import logging`
- Type: `from typing import`, `import asyncio`

**Trigger Regex:** `import\s+(numpy|pandas|requests|fastapi|flask|pytest|pydantic|typer|click|logging|asyncio|dataclasses|torch|sklearn|optuna)`

### Auto-Prompts

**Data Processing (numpy/pandas)**
- Validate data types during transformations
- Handle NA/NaN and outliers properly
- Use vectorized operations vs loops
- Safe and readable file operations

**HTTP Requests (requests)**
- Check HTTP error handling, timeouts, header security
- Recommend session reuse and response hooks

**CLI (typer/click)**
- Argparse compatibility, error handling
- Document help and parameters
- Ensure testability with pytest

**Web API (FastAPI/Flask)**
- Validate schemas with pydantic/dataclasses
- Error control and status codes
- Endpoint coverage with tests
- Input/output logging

**Testing (pytest)**
- Edge case coverage; generated fixtures
- Parametrized tests, mock, patch
- Clean setup/teardown
- @slow, @integration marks for long tests

**Logging**
- Standardize levels (info, warning, error)
- Formatters and log rotation
- Error and exception logging
- Best practices logging config

**Type System**
- Full type hints for inputs/outputs/models
- Use pydantic/dataclasses for structures
- Validate all critical data

**Async Code**
- Correct event loop, await, exception handlers
- Concurrency handling, timeouts, cancellation

### Review Checklist

- [ ] PEP8 + Google Python Style Guide
- [ ] Type hints everywhere; pydantic/dataclasses for complex structures
- [ ] Functions/classes have docstrings (Google style); commits in English
- [ ] Linting (flake8, black, isort, mypy) + pre-commit pass
- [ ] Tests: pytest, coverage ≥80%; edge fixtures, parametrization
- [ ] Logging via logging module; structured messages
- [ ] All IO work is safe: context managers, timeouts, path checks
- [ ] Web/API: pydantic validation, error handling
- [ ] CLI: help, input validation, exit codes
- [ ] Async code: exception handlers, test coverage
- [ ] Docker + requirements.txt: current, reproducible
- [ ] README: usage examples, dependencies, launch schema
- [ ] No "magic" constants; all in configs

---

## Rule 3: Chief Architect Reviewer

**Applies to:** `**/*.py`, `src/**`, `docker-compose.yaml`, `Makefile`, `pyproject.toml`, `README.md`

**Description:** Expert in architecture. Builds reliable, maintainable, beautiful systems. Respects MODULAR DESIGN, SOLID, CLEAN ARCHITECTURE.

**Trigger Words:** `class`, `def`, `import`, `api`, `service`, `pipeline`, `dag`, `config`, `layer`, `interface`, `container`

**Trigger Regex:** `(class|def|interface|service|pipeline|dag|layer|container|api)`

### Focal Points

**Classes & Interfaces:**
- Each class must implement single responsibility
- Be easily extendable and testable
- Follow SOLID—especially Open/Closed and Dependency Inversion

**Pipelines, DAGs, APIs:**
- Maximum transparency, documentation, scalability
- Endpoint structure, versioning strategy, component independence

**Layered Architecture:**
- Separate business logic, infrastructure, adapters, UI
- Avoid layer-skipping; keep contracts clean and documented

**Configuration & Containers:**
- Externalize all settings to env/config-files (12-factor app)
- Containers: isolated, reproducible, minimal

**Documentation & Project Setup:**
- Project description, build, dependencies, run scripts must be crystal clear
- Focus on onboarding and maintainability

### Review Checklist

- [ ] SOLID/GRASP, SRP/DRY/KISS/YAGNI adhered
- [ ] Architecture is modular, easily extended
- [ ] Module contracts via interfaces and typing
- [ ] All configuration centralized (config, env, pyproject.toml)
- [ ] No direct inter-layer dependencies—only via abstractions
- [ ] Documentation (README, architecture diagrams) current and clear
- [ ] Tests cover core business processes and integrations
- [ ] Pipelines, containers, services deploy/update easily
- [ ] Code is readable, maintainable; new developer onboarding is painless
- [ ] All components logically structured; no responsibility sprawl
- [ ] Errors/failures pre-planned; graceful degradation mechanisms exist
- [ ] Modern patterns applied: DI, CQRS, event-driven, factory, repository (as needed)

---

## Rule 4: AI Reviewer

**Applies to:** `src/**`, `config/**`, `docs/**`, `README.md`, `**/*.py`, `**/*.js`, `**/*.sh`

**Description:** Optimizes code readability and structure for AI tools. Analyzes function size, LLM visibility, token economy, suggests refactoring.

**Trigger Words:** `comment`, `docstring`, `naming`, `formatting`, `chunk`, `token`, `style`, `complexity`, `long`, `parse`, `structure`, `refactor`

### Auto-Prompts

**Functions & Classes:**
```
Measure:
- Average and max function/method length
- Methods per class (if >6-7, recommend decomposition)
- Longest functions for refactoring list

Example output:
- Average function length: 9.7 lines
- Longest: process_data (61 lines)
- Recommendation: Split into 3-4 subfunctions
```

**Token Cost & File Size:**
```
Analyze "token cost" per file:
- Estimate cost to LLM (by char count/words/approx tokens)
- If file >2500 lines or >10k tokens → split into logical modules
- Suggest grouping for LLM chunk parsing
```

**Refactoring Strategy:**
```
For each long method/file propose concrete refactoring:
- "Extract pipeline_steps.py for data operations"
- "Move utils to src/utils.py"
- "Split ModelTrainer into ModelLoader, Trainer, Evaluator"
```

**Documentation:**
```
Generate report:
- README length in tokens and lines
- Redundant repetitions and "filler" sections
- If docs don't match code structure → add missing sections
```

**JS/Bash:**
```
- All functions short, variables explicitly named, code blocks separated
- No meaningless comments (e.g., // do something)
- AI-LLM docs: compact, no garbage
```

### Review Checklist

- [ ] No functions >30-40 lines (or marked for refactoring)
- [ ] Max: 1 class = 1 responsibility (Single Responsibility)
- [ ] Names clear, consistent style; no abbreviation magic
- [ ] No huge files—split into modules
- [ ] README/docs compressed; only useful, current info
- [ ] Comments/docstrings only substantive; no auto-generated blocks
- [ ] Code easily chunked for LLM processing
- [ ] Token cost reasonable for AI tool (<4000 per file; <2048 per function)
- [ ] Consistent encoding: PEP8, tabs=4, lines ≤88 chars

---

## Rule 5: Security Reviewer

**Applies to:** `src/**`, `config/**`, `infra/**`, `deploy/**`, `docker-compose*.yml`, `Dockerfile*`, `.gitlab-ci.yml`, `.github/workflows/**`, `k8s/**`, `airflow/**`, `**/*.env`, `**/*.pem`, `**/*.crt`, `**/*.key`, `README.md`

**Description:** Automatic security audit agent for code, infrastructure, secrets, IAM, network and container policies.

**Trigger Words:** `secret`, `password`, `token`, `key`, `IAM`, `env`, `vault`, `hash`, `cipher`, `jwt`, `CORS`, `RBAC`, `ACL`, `root`, `firewall`, `network`, `policy`, `ssl`, `tls`

**Trigger Regex:** `(secret|password|token|key|jwt|cipher|hash|vault|env|IAM|ACL|RBAC|CORS|firewall|policy|ssl|tls|root)`

### Auto-Prompts

**Secrets Management:**
- No exposed secrets, passwords, tokens, keys in code/configs/Dockerfile
- All secrets in secure vault solutions (Vault, KMS, SOPS, AWS Secrets)
- .env not in git; in .gitignore
- Secret rotation and audit documented

**IAM/RBAC/ACL:**
- Least privilege principle implemented
- RBAC/ACL for all services, containers, users
- Service accounts never root
- Centralized audit logs for access changes

**Docker/Container Security:**
- No root USER; limited users only
- No extra capabilities
- Read-only volumes, securityContext, network policies

**TLS/Cryptography:**
- All connections HTTPS/TLS; valid, updated certificates
- No leaked keys/certs in public repos
- Modern algorithms only (sha256+, tls1.2+)

**JWT/Password/Hashing:**
- Passwords via bcrypt/scrypt/argon2 with salt
- JWT tokens with short TTL + refresh tokens
- Encryption keys NOT in source

**Network Policies:**
- Explicit CORS domains
- Firewall/NetworkPolicy limits public access to needed endpoints
- External connection audit maintained

### Review Checklist

- [ ] No secrets/passwords/tokens/keys exposed/in repo
- [ ] .env, .pem, .key in .gitignore; secure storage used
- [ ] RBAC/ACL: minimal rights for services/users
- [ ] Containers: no root/capabilities, read-only volumes
- [ ] Modern crypto, valid certificates
- [ ] HTTPS/TLS everywhere, certificates regularly updated
- [ ] JWT/passwords secure, stored/transmitted safely, short TTL
- [ ] Network/firewall policies: minimal external exposure
- [ ] Security event audit: who changed rights, who read/wrote secrets
- [ ] README contains security/secrets/deploy policy
- [ ] Key rotation, cert updates, incident response instructions

---

## Rule 6: DevOps Engineer

**Applies to:** `.github/workflows/**`, `.gitlab-ci.yml`, `docker-compose*.yml`, `Dockerfile*`, `Makefile`, `infra/**`, `deploy/**`, `helm/**`, `k8s/**`, `grafana/**`, `prometheus/**`, `src/**`

**Description:** Agent reviewing DevOps: CI/CD, monitoring, alerts, cloud, security.

**Trigger Words:** `FROM`, `RUN`, `ENTRYPOINT`, `EXPOSE`, `CMD`, `ENV`, `secrets`, `volumes`, `pipeline`, `deploy`, `monitor`, `alert`, `security`, `cloud`, `helm`, `k8s`, `namespace`, `chart`

**Trigger Regex:** `(FROM|RUN|ENTRYPOINT|EXPOSE|CMD|ENV)`, `(pipeline|deploy|helm|k8s|namespace|chart)`, `(monitor|grafana|prometheus|alert)`, `(secrets|token|password|key)`

### Dockerfile Best Practices

- Minimal, non-root user, security-first
- Layer optimization for build
- ENTRYPOINT + HEALTHCHECK present
- No secrets; use environment variables
- Documented build, args, ENV in README

### docker-compose

- Services isolated (networks)
- Variables in .env (secrets!)
- Volumes for persisted data
- Health checks per service
- Dependencies explicit (depends_on)

### CI/CD Pipeline

- Lint (black, flake8, mypy)
- Test (pytest)
- Build docker image
- Push to registry
- Deploy (on main branch)

### Monitoring & Alerts

**Service Metrics:**
- CPU, memory, HTTP errors, latency, uptime

**Alert Templates:**
- Service Down: `up{job="web"} == 0` (2m)
- High Error Rate: `>5% 5xx errors / 5min` (1m)
- High Latency: `p95 latency >2500ms` (2m)
- ML Model Drift: detected drift in F1/accuracy (10m)

**Grafana Dashboards:**
- App Health: CPU/Memory, HTTP 2xx/4xx/5xx, latency, uptime, SLA
- ML Service: latency, prediction volume, error rate, drift, quality metrics, version/hash

### Review Checklist

- [ ] Dockerfile minimal, non-root, secure
- [ ] docker-compose: isolated, env vars in .env
- [ ] CI/CD pipeline: build → lint → test → scan → deploy
- [ ] Secrets via secret-manager; .env not in git
- [ ] Prometheus metrics; alert templates for standard incidents
- [ ] Grafana: minimal dashboard per service, latency, error, SLA
- [ ] ML: additional alerts/panels for drift/quality
- [ ] README: deploy/monitoring/alerts/grafana sections
- [ ] Centralized logs; clear retention, incident search
- [ ] Monitoring/deploy startup instructions verified

---

## Rule 7: Technical Writer

**Applies to:** `README.md`, `docs/**`, `CHANGELOG.md`, `CONTRIBUTING.md`, `src/**`, `config/**`, `**/*.py`, `**/*.sh`, `**/*.js`, `**/*.sql`

**Description:** Automatic agent for documentation, docstrings, user guides, changelog. Templates for ML, prod, API.

### Docstring Template (Google Style)

```python
def train_model(config: dict, data_path: str) -> Model:
    """Train ML model with specified configuration and data.
    
    Args:
        config (dict): Training config with hyperparameters
        data_path (str): Path to training data
        
    Returns:
        Model: Trained model instance
        
    Raises:
        ValueError: If config invalid or data missing
        
    Example:
        model = train_model(my_config, "/data/train.parquet")
    """
```

Document input/output params, exceptions, working examples.

### README Template (ML/Prod)

```markdown
# Project

## Description and Business Goals

Brief project description, key econ/business goals.

## Quick Start

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Train Model
```bash
python src/train.py --config configs/config_prod.yaml
```

### Inference
```bash
python src/predict.py --input samples/input.json --model models/model_latest.pkl
```

## Repository Structure
- src/ — ML code
- configs/ — YAML/JSON configs
- models/ — Model artifacts
- data/ — Example datasets

## Documentation & Examples
- API connection, run scripts
- Scenarios: end-to-end, ML pipeline, quality monitoring

## Monitoring & Deployment
- Deploy instructions (Docker/k8s)
- Metrics, alerts, Grafana dashboard

## Contributing & License
```

### API Documentation

- All endpoints: inputs/outputs
- curl/requests/Postman examples
- Error codes, responses
- OpenAPI/Swagger schema (if applicable)

### CHANGELOG (Semantic Versioning)

```markdown
## [2.1.3] — 2025-10-23

### Added
- New MLflow pipeline

### Changed
- Inference optimization; latency minimized

### Fixed
- Missing values handling bug

### Security
- Dependency updates; token validation improved
```

### CONTRIBUTING

- Commit templates (conventional commits)
- Issue/PR templates
- Test/local env instructions
- Global docstring/README guidelines

### Review Checklist

- [ ] All functions/classes: Google-style docstrings with examples
- [ ] README: description, quick start, ML/Prod instructions
- [ ] API docs: clear, current, with examples
- [ ] CHANGELOG: semantic versioning, real changes
- [ ] CONTRIBUTING: onboarding, templates, best practices
- [ ] All docs: good English/Russian, no typos, live examples

---

## Rule 8: QA/TDD Reviewer

**Applies to:** `tests/**`, `**/test_*.py`, `**/*.test.py`, `**/integration/**`, `**/e2e/**`, `**/contract/**`, `**/pytest.ini`, `**/tox.ini`, `.github/workflows/**`, `.gitlab-ci.yml`, `src/**/*.py`

**Description:** Automatic agent ensuring test coverage, TDD, integration and E2E tests.

**Trigger Words:** `import pytest`, `from unittest`, `def test_`, `@pytest.mark`, `assert `, `expected`, `setup`, `teardown`, `fixtures`, `mock`, `patch`, `coverage`, `integration`, `e2e`, `contract`

**Trigger Regex:** `def\s+test_`, `import\s+(pytest|unittest|mock)`, `class\s+TestIntegration`, `class\s+TestE2E`, `class\s+TestContract`

### Test Levels

**Unit Tests:**
- Mock external dependencies (LLM, MCP, DB)
- Test happy path + error cases
- Test edge cases

**Integration Tests:**
- Real MongoDB (or test DB)
- Real MCP tools (or mocked)
- Full flow: request → response

**E2E Tests:**
- Aiogram test client for Telegram
- Full user scenario
- Verify actual response

### Requirements

- Minimum coverage: 80% (aim for 90%)
- Critical paths: 100%
- Reports via pytest-cov

**Structure:**
```
tests/
├── unit/
│   ├── test_butler_orchestrator.py
│   └── test_handlers/
├── integration/
│   ├── test_create_task_flow.py
│   └── conftest.py (fixtures)
└── e2e/
    └── test_telegram_butler.py
```

### Review Checklist

- [ ] Integration tests: multi-component interaction, real services, staging env, fixtures
- [ ] E2E tests: real business flow, user action sequence, UI/backend/DB integration
- [ ] Contract tests: API endpoint validation, schema validation, backwards compatibility
- [ ] Test data/fixtures available; cleanup after runs
- [ ] Tests run on CI in docker-compose environment
- [ ] Coverage ≥80%; critical paths 100%
- [ ] Mock services properly; isolation maintained

---

## Rule 9: ML Engineer Reviewer

**Applies to:** `src/ml/**`, `src/ai/**`, `train*.py`, `finetune*.py`, `metrics.py`, `*.ipynb`, `*.py`

**Description:** Expert agent for ML/AI code, metrics, infrastructure review.

**Trigger Words:** `import torch`, `import tensorflow`, `import sklearn`, `import xgboost`, `import transformers`, `import pytorch_lightning`, `import mlflow`, `import optuna`, `import dvc`, `import hydra`

**Trigger Regex:** `import\s+(torch|tensorflow|sklearn|xgboost|transformers|pytorch_lightning|mlflow|optuna|dvc|hydra)`

### Auto-Prompts

**PyTorch/PyTorch Lightning:**
- Reproducibility (random seeds everywhere)
- Checkpoint + early stopping logic
- Learning rate + metric monitoring (accuracy, F1, ROC-AUC)
- Model/weight versioning
- MLflow integration
- Easy restart from checkpoints

**TensorFlow:**
- Model architecture via config
- Custom + built-in metric tracking
- Reproducibility (seeds, tf.random)
- SavedModel/TFRecord saving
- TPU/GPU work, logging

**scikit-learn/XGBoost:**
- Stratified splits, correct metrics
- Class balance analysis, outlier handling
- GridSearch/Optuna for tuning
- Feature importance visualization, saving

**HuggingFace Transformers:**
- Tokenization logic, generation error handling
- Fine-tuning correctness, callbacks/early stopping
- BLEU, ROUGE metric tracking (NLP)
- Inference monitoring (batch/stream)

**MLflow:**
- Model, metric, param, artifact logging
- MinIO/S3 integration for artifacts
- Reproducibility: config, seed, data saved
- MLflow dashboard export

**Optuna:**
- Hyperparameter optimization logic
- Study persistence, trial pruning
- Visualization of optimization history

### Review Checklist

- [ ] Reproducibility: seeds, config saving, data versioning
- [ ] Model versioning with metadata
- [ ] Metrics tracked: accuracy, F1, ROC-AUC, latency
- [ ] MLflow integration for experiment tracking
- [ ] Checkpoints saved; easy restart
- [ ] Inference optimized; batch/stream capable
- [ ] Error handling robust
- [ ] Logging comprehensive

---

## Rule 10: Data Engineer Reviewer

**Applies to:** `src/data/**`, `src/etl/**`, `src/features/**`, `src/pipelines/**`, `src/dwh/**`, `src/spark/**`, `dags/**`, `schemas/**`, `jobs/**`, `parquet/**`, `**/*.sql`, `docker-compose*.yml`, `airflow/**`, `spark/**`, `config/**`, `README.md`

**Description:** Agent reviewing data, ETL, schemas, lineage and monitoring. Audit and control pipeline templates.

### SQL Best Practices

**DDL with Audit & Lineage:**

```sql
CREATE TABLE IF NOT EXISTS {schema}.{table_name} (
    id SERIAL PRIMARY KEY,
    source VARCHAR(64) NOT NULL COMMENT 'Data source',
    feature_name VARCHAR(128) NOT NULL,
    value FLOAT NOT NULL,
    batch_id BIGINT COMMENT 'Load/batch ID',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    changed_by VARCHAR(64) COMMENT 'Who/when changed',
    lineage JSONB COMMENT 'Data history'
) PARTITION BY RANGE (created_at);

COMMENT ON TABLE {schema}.{table_name} IS 'Features table with lineage and audit';
```

**Raw → Staging → Mart Pattern:**

```sql
-- raw
CREATE TABLE raw.events (...);

-- staging
CREATE TABLE staging.cleaned_events AS
SELECT ..., validation_flag, ingestion_time
FROM raw.events
WHERE quality_check = TRUE;

-- mart
CREATE TABLE mart.daily_features AS
SELECT user_id, feature_X, feature_Y, event_date
FROM staging.cleaned_events
GROUP BY user_id, event_date;
```

### Lineage Practices

- source-to-target mapping in every pipeline
- MLflow, Airflow, or DataHub for lineage automation
- All tables/fields: comments + script links
- All transforms: tracked and versioned

### Monitoring & Alerts

**Airflow SLA:** Task >10min runtime → Dev alert

**Grafana Metrics:**
- task_duration_seconds
- dag_run_success/fail
- processed_records_count

**Data Quality:** Auto-check dupes, missing keys; bad_records in audit table

**Dashboard:**
- Dag/Task runtime, SLA missed
- Records: processed/success/fail/invalid by time
- Raw → staging → mart volume
- Errors, delays, key table alerts
- Data quality: NULL %, invalid %, lineage visualization

### Review Checklist

- [ ] DDL: clear types, constraints, comments, timestamp
- [ ] Lineage/audit: where/how/who changed data
- [ ] Monitoring/alerts: latency, errors, outliers on each step
- [ ] All pipelines/dags described; clear source → target chain
- [ ] Test + SLA templates in repo
- [ ] Docs: business meaning of layers (raw/staging/mart), SLA described
- [ ] Grafana templates: ready for health/quality review

---

## Rule 11: Docker Reviewer

**Applies to:** `Dockerfile`, `*.dockerfile`

**Description:** Expert in containerization: security and minimalism.

### Checklist

- [ ] USER present; no root; minimal images (slim/alpine)
- [ ] RUN commands sequenced for layer optimization
- [ ] ENTRYPOINT + HEALTHCHECK present
- [ ] No secrets; use environment variables
- [ ] Build, args, ENV described in README

---

## Rule 12: Bash Reviewer (sh-reviewer)

**Applies to:** `*.sh`

**Description:** Expert in shell scripts: security and readability.

### Standards

- Run shellcheck
- Shebang + `set -euo pipefail` present
- All paths absolute; variables readable, top-declared
- Use functions; avoid nested calls/concatenation
- Document via comments and README "Usage" section

---

## Rule 13: ML Engineer (ml-engineer.mdc) — Detailed

**[See Rule 9 above for full coverage]**

---

## Summary: How to Use

1. Copy entire content to `.cursorrules` in project root
2. Cursor auto-detects and applies rules
3. All 13 rule agents trigger on file changes
4. Code quality, tests, docs, security reviewed automatically

### Priority Rules (Apply Most Strictly)

1. **Python Zen Writer** — code style, readability
2. **Chief Architect** — system design, SOLID
3. **Security Reviewer** — secrets, auth, encryption
4. **QA/TDD Reviewer** — test coverage
5. **DevOps Engineer** — CI/CD, monitoring

### Moderate Rules

- Python Code Reviewer (detailed checks)
- AI Reviewer (token cost, refactor)
- Technical Writer (docs quality)

### Specialized Rules

- ML Engineer (ML/AI-specific)
- Data Engineer (ETL/warehouse)
- Docker/Bash (infrastructure)

---

## Example: How Cursor Applies Rules

```
User writes: src/domain/agents/butler_orchestrator.py

Triggered Rules:
1. Python Zen Writer: Check function length, docstrings, imports
2. Chief Architect: Validate SOLID, layer separation
3. AI Reviewer: Token cost, readability for LLM
4. Python Code Reviewer: Type hints, logging, error handling
5. Security Reviewer: No secrets, safe defaults

Output: Cursor suggests improvements across all 5 rules
```

---

**End of Unified Cursor Rules — Butler Agent**

All 13 rules consolidated, English-primary, production-ready. 🚀
