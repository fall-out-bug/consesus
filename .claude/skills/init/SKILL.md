---
name: init
description: Initialize SDP in current project (interactive wizard)
tools: Read, Write, Bash, AskUserQuestion
---

# /init - SDP Project Setup Wizard

Interactive setup wizard for SDP projects.

## When to Use

- Setting up SDP in a new project
- Reconfiguring SDP in existing project
- Verifying SDP installation

## Workflow

### Step 1: Collect Project Metadata

Prompt for:
- **Project name**: Default from directory name
- **Description**: Brief project description
- **Author**: Project author/maintainer

### Step 2: Detect Optional Dependencies

Auto-detect:
- Beads CLI (task tracking)
- GitHub CLI (gh)
- Telegram (notifications)

### Step 3: Create Directory Structure

Create standard directories:
```
docs/
├── workstreams/
│   ├── INDEX.md
│   ├── TEMPLATE.md
│   └── backlog/
├── PROJECT_MAP.md
└── drafts/
sdp.local/
```

### Step 4: Generate Quality Gate Config

Create `quality-gate.toml` with:
- Coverage settings (80% minimum)
- Complexity limits (CC < 10)
- File size limits (200 LOC)
- Type hint requirements
- Error handling rules
- Architecture constraints

### Step 5: Create .env Template

Generate `.env.template` with placeholders for detected dependencies:
- Telegram bot token/chat ID
- GitHub token/repo
- Beads API URL

### Step 6: Install Git Hooks

Install pre-commit hook for SDP validation.

### Step 7: Run Doctor

Execute `sdp doctor` to validate setup.

## Usage

```bash
# Interactive setup (prompts for values)
sdp init

# Use defaults
sdp init --non-interactive

# Target specific directory
sdp init --path /path/to/project

# Overwrite existing files
sdp init --force
```

## Output

- `docs/PROJECT_MAP.md` — Project decision log
- `docs/workstreams/INDEX.md` — Workstream index
- `docs/workstreams/TEMPLATE.md` — Workstream template
- `quality-gate.toml` — Quality gate configuration
- `.env.template` — Environment variable template
- `.git/hooks/pre-commit` — Git hook (if git repo)

## Next Steps

After setup:
1. Edit `docs/PROJECT_MAP.md` with project info
2. Run `sdp extension list` to see available extensions
3. Start with `/idea "your first feature"`

## Interactive Flow Example

```
$ sdp init

╔════════════════════════════════════════╗
║   SDP Project Setup Wizard v0.6.0      ║
╚════════════════════════════════════════╝

→ Detecting project structure...
✓ Git repository found
✓ Python project detected (pyproject.toml)

Step 1/7: Project Metadata
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project name [my-service]: 
> my-service

Description [My service description]: 
> API service for user management

Author [John Doe]: 
> John Doe <john@example.com>

Step 2/7: Optional Dependencies
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Checking for optional tools...
✓ Beads CLI found (v1.2.0) - Task tracking enabled
✓ GitHub CLI found (v2.40.0) - GitHub integration enabled
✗ Telegram bot not configured - Notifications disabled

Step 3/7: Directory Structure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Creating directories...
✓ docs/workstreams/backlog/
✓ docs/workstreams/in_progress/
✓ docs/workstreams/completed/
✓ docs/drafts/
✓ sdp.local/

Step 4/7: Quality Gate Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Select quality gate profile:
  [1] Strict (80% coverage, CC<10, 200 LOC)
  [2] Moderate (70% coverage, CC<15, 300 LOC)
  [3] Relaxed (60% coverage, CC<20, 500 LOC)

Choose [1-3]: 
> 1

✓ Created quality-gate.toml (Strict profile)

Step 5/7: Environment Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Creating .env.template with detected integrations...
✓ Added Beads configuration
✓ Added GitHub configuration

Configure Telegram notifications? [y/N]: 
> y

Telegram bot token: 
> 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

Telegram chat ID: 
> -1001234567890

✓ Added Telegram configuration

Step 6/7: Git Hooks
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Installing SDP git hooks...
✓ pre-commit hook installed
✓ pre-push hook installed

Step 7/7: Validation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Running sdp doctor...

Python 3.11.6                    [✓] OK
Poetry 1.7.1                     [✓] OK
Git 2.42.0                       [✓] OK
Beads CLI 1.2.0                  [✓] OK
GitHub CLI 2.40.0                [✓] OK
Telegram bot                     [✓] OK
Quality gates config             [✓] OK

╔════════════════════════════════════════╗
║   ✓ SDP Setup Complete!                ║
╚════════════════════════════════════════╝

Created files:
  • docs/PROJECT_MAP.md
  • docs/workstreams/INDEX.md
  • docs/workstreams/TEMPLATE.md
  • quality-gate.toml
  • .env.template
  • .git/hooks/pre-commit

Next steps:
  1. Edit docs/PROJECT_MAP.md with project details
  2. Copy .env.template to .env and fill in values
  3. Run: @idea "Your first feature"

Documentation: https://github.com/fall-out-bug/sdp
```
