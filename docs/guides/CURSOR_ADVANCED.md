# Advanced Cursor Features for SDP

This document identifies Cursor IDE features that could enhance SDP workflow but are currently underutilized.

## Currently Used ✅

- ✅ `.cursorrules` - Project rules (auto-loaded)
- ✅ Custom slash commands (`.cursor/commands/*.md`)
- ✅ Git hooks integration
- ✅ Model selection (mentioned, not detailed)
- ✅ Chat context (mentioned, not optimized)

## Underutilized Features 🔍

### 1. Composer (Multi-file Editing)

**Current state:** Not used

**Potential:**
- Edit multiple files simultaneously during `/build`
- Refactor across layers (Domain → Application → Infrastructure)
- Update tests + implementation in one operation

**Example:**
```
# Instead of:
1. Edit domain/entity.py
2. Edit application/use_case.py
3. Edit tests/test_entity.py

# Use Composer:
@domain/entity.py @application/use_case.py @tests/test_entity.py
"Implement User entity with GetUser use case and tests following TDD"
```

**Integration with SDP:**
- Add to `/build` command: "Use Composer for multi-file changes"
- Document in `prompts/commands/build.md`

---

### 2. @file References in Chat

**Current state:** Mentioned ("@-mention relevant files") but not detailed

**Potential:**
- Explicit file context for each command
- Better token management
- Clearer AI understanding

**Example:**
```
/design idea-user-auth
@docs/drafts/idea-user-auth.md
@docs/workstreams/INDEX.md
@PROJECT_CONVENTIONS.md
"Create workstreams following SDP"
```

**Integration with SDP:**
- Document recommended @files for each command
- Add to `.cursor/commands/*.md` templates

---

### 3. Codebase Indexing

**Current state:** Not mentioned

**Potential:**
- Faster context loading for large codebases
- Better understanding of project structure
- Automatic dependency detection

**Integration with SDP:**
- Document how to enable indexing
- Use for `/design` (analyze existing code)
- Use for `/review` (check patterns)

---

### 4. Terminal Integration

**Current state:** Only bash hooks, not Cursor's built-in terminal

**Potential:**
- Run validation directly in Cursor terminal
- See test results inline
- Execute Git commands with UI feedback

**Example:**
```bash
# In Cursor terminal:
hooks/pre-build.sh WS-001-01
hooks/post-build.sh WS-001-01 project.module
```

**Integration with SDP:**
- Document terminal shortcuts
- Add terminal commands to each command guide

---

### 5. Git UI Integration

**Current state:** Only CLI (`git checkout`, `git commit`)

**Potential:**
- Visual diff before commit
- Branch management in UI
- Commit message templates
- Staging area management

**Integration with SDP:**
- Use Cursor's Git UI for `/build` commits
- Visual diff for `/review`
- Branch switching for `/design`

---

### 6. Diff View

**Current state:** Not used

**Potential:**
- Review changes before commit
- Compare workstream implementations
- Check Clean Architecture violations visually

**Integration with SDP:**
- Add to `/review` workflow
- Use for quality gates verification

---

### 7. Inline Editing

**Current state:** Not mentioned

**Potential:**
- Quick fixes without opening files
- Edit code directly in chat suggestions
- Faster iteration

**Integration with SDP:**
- Use for small fixes during `/build`
- Quick refactoring during `/review`

---

### 8. Code Actions

**Current state:** Not documented

**Potential:**
- Quick fixes for linting errors
- Auto-import organization
- Type hint generation
- Refactoring suggestions

**Integration with SDP:**
- Use for quality gates (fix linting automatically)
- Add to post-build validation

---

### 9. Workspace Settings

**Current state:** Not used

**Potential:**
- Project-specific model preferences
- Custom keybindings for SDP commands
- File associations
- Exclude patterns for indexing

**Integration with SDP:**
- Create `.vscode/settings.json` template
- Document recommended settings

---

### 10. Custom Instructions

**Current state:** Not used

**Potential:**
- Project-wide AI behavior
- Consistent code style enforcement
- SDP-specific preferences

**Integration with SDP:**
- Add to `.cursor/` directory
- Reference in `.cursorrules`

---

### 11. Chat Context Management

**Current state:** Mentioned ("Clear chat between features") but not detailed

**Potential:**
- Pin important files (PROJECT_CONVENTIONS.md, INDEX.md)
- Clear context strategically
- Save chat sessions for reference

**Integration with SDP:**
- Document when to clear context
- Which files to pin for each command
- Session management best practices

---

### 12. File Tree Context

**Current state:** Not used

**Potential:**
- AI understands project structure better
- Automatic file discovery
- Better suggestions based on location

**Integration with SDP:**
- Document file tree organization
- Use for `/design` (analyze structure)

---

### 13. Search Across Codebase

**Current state:** Not documented

**Potential:**
- Find similar patterns
- Check for duplicates
- Discover dependencies

**Integration with SDP:**
- Use for `/design` (check INDEX.md for duplicates)
- Use for `/review` (find similar implementations)

---

### 14. Model Switching in UI

**Current state:** Mentioned but not detailed

**Potential:**
- Quick model switch per command
- Keyboard shortcuts
- Model recommendations visible

**Integration with SDP:**
- Document keyboard shortcuts
- Add model hints to each command

---

### 15. Codebase Chat

**Current state:** Not used

**Potential:**
- Ask questions about entire codebase
- Understand architecture
- Find patterns

**Integration with SDP:**
- Use for `/design` (analyze existing code)
- Use for `/issue` (debug across codebase)

---

## Recommended Enhancements

### High Priority

1. **Composer integration** - Multi-file editing for `/build`
2. **@file references** - Document recommended files per command
3. **Terminal integration** - Use Cursor terminal for validation
4. **Git UI** - Visual diff and branch management

### Medium Priority

5. **Code Actions** - Auto-fix linting during quality gates
6. **Chat context management** - Pin files, clear strategically
7. **Diff view** - Visual review before commit
8. **Workspace settings** - Project-specific configuration

### Low Priority

9. **Codebase indexing** - For large projects
10. **Inline editing** - Quick fixes
11. **Custom instructions** - Project-wide AI behavior
12. **File tree context** - Better structure understanding

---

## Implementation Plan

### Phase 1: Document Existing Features Better

- [ ] Add @file recommendations to each command
- [ ] Document terminal shortcuts
- [ ] Add Git UI workflow to `/build`
- [ ] Document chat context management

### Phase 2: Integrate High-Priority Features

- [ ] Add Composer examples to `/build`
- [ ] Create workspace settings template
- [ ] Add diff view to `/review`
- [ ] Document code actions usage

### Phase 3: Advanced Features

- [ ] Codebase indexing guide
- [ ] Custom instructions template
- [ ] File tree context optimization
- [ ] Search integration

---

## Examples

### Enhanced `/build` with Composer

```markdown
# /build WS-001-01

## Multi-file Editing

Use Cursor Composer for related files:

```
@src/domain/user.py @src/application/get_user.py @tests/test_get_user.py
"Implement GetUser use case with TDD: write test first, then implementation"
```

This edits all three files simultaneously.
```

### Enhanced `/review` with Diff View

```markdown
# /review F01

## Visual Diff

1. Open Cursor's Git panel
2. Review changes visually
3. Check for:
   - Clean Architecture violations (domain imports)
   - Test coverage (new files have tests)
   - File size (< 200 LOC)
```

### Enhanced Context Management

```markdown
## Chat Context Best Practices

**Pin these files:**
- PROJECT_CONVENTIONS.md (always)
- docs/workstreams/INDEX.md (for /design, /build)
- PROTOCOL.md (for reference)

**Clear context:**
- Between different features
- After completing /review
- When switching commands
```

---

**Version:** 0.3.0  
**Status:** Analysis document  
**Next Steps:** Prioritize and implement enhancements
