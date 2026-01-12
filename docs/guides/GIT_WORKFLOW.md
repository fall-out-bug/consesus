# Git Workflow with SDP

Guidelines for Git commits and workflow in SDP projects.

## Conventional Commits

All commits must follow [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | When to Use | Example |
|------|------------|---------|
| `feat` | New feature | `feat(auth): WS-001-01 - implement domain layer` |
| `fix` | Bug fix | `fix(api): resolve timeout in payment endpoint` |
| `docs` | Documentation | `docs(sdp): update README with Task tool info` |
| `test` | Tests | `test(auth): WS-001-01 - add unit tests` |
| `refactor` | Code refactoring | `refactor(domain): extract validation logic` |
| `style` | Formatting | `style: run black formatter` |
| `chore` | Maintenance | `chore: update dependencies` |
| `perf` | Performance | `perf(api): optimize query performance` |
| `ci` | CI/CD | `ci: add GitHub Actions workflow` |
| `build` | Build system | `build: update Dockerfile` |

### Scope

Scope should match feature slug or module name:
- Feature: `feat(auth): ...`
- Module: `fix(domain): ...`
- Workstream: `feat(auth): WS-001-01 - ...`

### Subject

- Imperative mood: "add", "fix", "update" (not "added", "fixed", "updated")
- Lowercase
- No period at the end
- Max 72 characters

## Co-authored-by for AI Assistance

When commits are made with AI assistance (Claude Code, Cursor AI), add Co-authored-by trailer:

```
feat(auth): WS-001-01 - implement domain layer

Co-authored-by: Claude Code (Auto) <claude-code@anthropic.ai>
```

### Automatic Addition

**Option 1: Use helper script**
```bash
./scripts/commit-with-coauthor.sh "feat(auth): WS-001-01 - implement domain layer"
```

**Option 2: Use commit template**
```bash
git commit  # Template will include Co-authored-by placeholder
```

**Option 3: Manual addition**
```bash
git commit -m "feat(auth): WS-001-01 - implement domain layer

Co-authored-by: Claude Code (Auto) <claude-code@anthropic.ai>"
```

### When to Add Co-authored-by

✅ **Add when:**
- AI generated significant code
- AI wrote documentation
- AI refactored code
- AI created workstreams

❌ **Don't add when:**
- Only formatting changes
- Only file moves/renames
- Only merge commits

## Commit Message Examples

### Feature Implementation

```
feat(auth): WS-001-01 - implement user domain entities

- Add User entity with email validation
- Add Password value object
- Add Session entity
- Coverage: 85%

Co-authored-by: Claude Code (Auto) <claude-code@anthropic.ai>
```

### Bug Fix

```
fix(api): resolve timeout in payment endpoint

Increase timeout from 5s to 30s for large payment processing.
Add retry logic with exponential backoff.

Co-authored-by: Claude Code (Auto) <claude-code@anthropic.ai>
```

### Documentation

```
docs(sdp): update README with Task tool integration

- Document @oneshot with Task tool
- Add AskUserQuestion examples
- Update workflow diagrams

Co-authored-by: Claude Code (Auto) <claude-code@anthropic.ai>
```

### Multiple Workstreams

```
feat(auth): WS-001-01 through WS-001-05 - complete authentication feature

Implemented:
- WS-001-01: Domain entities
- WS-001-02: Application services
- WS-001-03: Infrastructure layer
- WS-001-04: API endpoints
- WS-001-05: Integration tests

All acceptance criteria met. Coverage: 87%.

Co-authored-by: Claude Code (Auto) <claude-code@anthropic.ai>
```

## Git Hooks

SDP includes Git hooks for validation:

### commit-msg Hook

Validates commit message format:
- Checks conventional commits pattern
- Allows Co-authored-by trailers
- Provides helpful error messages

### pre-commit Hook

Runs before commit:
- Linting (ruff, mypy)
- Tests (pytest)
- Secret detection
- File size checks

## Branch Naming

Follow GitFlow conventions:

```
feature/{slug}     # New features (from develop)
fix/{slug}         # Bug fixes (from develop)
hotfix/{slug}      # Emergency fixes (from main)
bugfix/{slug}      # Quality fixes (from develop)
```

Examples:
- `feature/user-auth`
- `fix/login-redirect`
- `hotfix/critical-api-failure`

## Commit Workflow

### During /build

After completing workstream:

```bash
# 1. Stage code
git add src/

# 2. Commit with Co-authored-by
git commit -m "feat(auth): WS-001-01 - implement domain layer

Co-authored-by: Claude Code (Auto) <claude-code@anthropic.ai>"

# 3. Stage tests
git add tests/

# 4. Commit tests
git commit -m "test(auth): WS-001-01 - add unit tests

Co-authored-by: Claude Code (Auto) <claude-code@anthropic.ai>"

# 5. Stage execution report
git add docs/workstreams/

# 6. Commit report
git commit -m "docs(auth): WS-001-01 - execution report

Co-authored-by: Claude Code (Auto) <claude-code@anthropic.ai>"
```

### During /oneshot

Orchestrator agent commits automatically with Co-authored-by for each WS.

## Best Practices

1. **One logical change per commit**
   - Don't mix features
   - Don't mix fixes with features

2. **Atomic commits**
   - Each commit should be complete and testable
   - Don't commit broken code

3. **Clear messages**
   - Explain WHAT and WHY (not HOW - code shows that)
   - Reference workstream IDs when applicable

4. **Co-authored-by for AI work**
   - Always add when AI generated code
   - Helps track AI contribution

5. **Conventional format**
   - Makes changelog generation easier
   - Enables automated tooling

## Troubleshooting

### Commit message rejected

If commit-msg hook rejects your message:
1. Check format: `type(scope): subject`
2. Ensure type is valid (feat, fix, docs, etc.)
3. Check subject is imperative mood, lowercase

### Co-authored-by not showing

If Co-authored-by doesn't appear:
1. Check format: `Co-authored-by: Name <email>`
2. Ensure it's in footer (after blank line)
3. Verify email format is valid

## Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Co-authored-by](https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/creating-a-commit-with-multiple-authors)
- [SDP PROTOCOL.md](../../PROTOCOL.md)

---

**Version:** 0.3.0  
**Last Updated:** 2026-01-12
