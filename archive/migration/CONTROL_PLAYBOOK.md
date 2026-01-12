# Regaining Control Playbook (when the repo was “written by agents”)

This is a human-first recovery workflow. It is designed for incremental stabilization without a risky “big rewrite”.

## 1) Stabilize (today)

- **Freeze**: stop running agents on the whole repo. Allow only narrow, file-scoped tasks.
- **Pick a baseline**: choose a known-good commit/branch and protect it.
- **Decide the control loop**: changes enter only via reviewed PRs using `.github/pull_request_template.md`.

## 2) Rebuild understanding (this week)

- **Module map**: list major subsystems and their owners:
  - `tools/hw_checker/` (backend + CLI + UI)
  - `consensus/` (agent protocol + prompts)
  - `courses/` (content)
- **Hotspot scan**: identify files with frequent churn / unclear logic.
- **Write “golden docs”**: short docs that define contracts and invariants (status model, API contracts, folder boundaries).

## 3) Add hard gates (permanent)

- **Bounded scope**: PRs must declare what they touch and what they avoid.
- **No mega-refactors** without an explicit epic and human sign-off.
- **Docs + tests** are required for behavior/contract changes.
- **No silent fallbacks** (explicit errors only).

## 4) How to use agents safely

When you do use an agent, constrain it:

- Give it a **single epic path** and **explicit file boundaries**.
- Require it to cite touched files and stop after a bounded change.
- Require tests and a short human-readable explanation.

## 5) When you still feel lost

Do not ask an agent to “clean the repo”. Instead:

- Pick one painful workflow (e.g., “LLM reviewer EP11”) and stabilize it end-to-end.
- Repeat for the next workflow.


