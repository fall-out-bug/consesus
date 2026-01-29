# SDP Quick Start Tutorial
**Learn SDP in 15 Minutes - Create Your First Feature**

This hands-on tutorial teaches you the SDP workflow by actually building a small feature. You'll learn by doing, with validation at each step.

---

## Prerequisites Check (2 minutes)

Let's verify you have everything installed:

```bash
# Check Python version (need 3.10+)
python --version
# Expected: Python 3.10.x or higher

# Check Poetry (need 1.8+)
poetry --version
# Expected: Poetry version 1.8.x or higher

# Check Git
git --version
# Expected: git version 2.x.x or higher

# Verify you're in an SDP project
ls CLAUDE.md PROTOCOL.md
# Expected: Both files exist
```

❓ **If anything is missing:**
- Python: Install from [python.org](https://www.python.org/downloads/)
- Poetry: `curl -sSL https://install.python-poetry.org | python3 -`
- Git: Install from [git-scm.com](https://git-scm.com/downloads)

**✅ Checkpoint:** All commands above should succeed.

---

## Step 1: Create Your First Feature (3 minutes)

Use the `@feature` command to start a new feature. SDP will guide you through requirements gathering.

```bash
# Start the feature workflow
@feature "Add user authentication"
```

**What happens:**
1. SDP asks clarifying questions about authentication
2. You provide answers (or press Enter for defaults)
3. SDP generates a feature specification

**Example interaction:**
```
🤔 What authentication methods do you need? (email, oauth, sso)
> email

🤔 Should users be able to reset passwords? (yes/no)
> yes

🤔 Do you need session management? (yes/no)
> yes
```

**Expected output:**
```
✅ Feature specification created: docs/drafts/feature-user-auth.md
✅ Workstreams designed: 4 workstreams created
Next: Run @build WS-001-01 to start implementation
```

**✅ Checkpoint:** You should see a new feature file in `docs/drafts/`.

---

## Step 2: Review Workstream Design (2 minutes)

SDP automatically breaks your feature into workstreams. Let's review them:

```bash
# List generated workstreams
ls docs/workstreams/backlog/
```

**Expected output:**
```
WS-001-01-user-models.md
WS-001-02-auth-service.md
WS-001-03-password-reset.md
WS-001-04-session-management.md
```

Each workstream includes:
- 🎯 Goal (what you're building)
- 📋 Acceptance Criteria (how to know it's done)
- 🔗 Dependencies (what needs to be done first)

**View a workstream:**
```bash
cat docs/workstreams/backlog/WS-001-01-user-models.md
```

**✅ Checkpoint:** You should see 4 workstream files with clear goals and acceptance criteria.

---

## Step 3: Execute Your First Workstream (5 minutes)

Now let's actually build something! Use `@build` to execute a workstream.

```bash
# Build the first workstream
@build WS-001-01
```

**What happens:**
1. **Red Phase:** SDP writes a failing test
2. **Green Phase:** SDP writes minimal code to pass
3. **Refactor Phase:** SDP improves the code
4. **Quality Gates:** SDP runs tests, linters, complexity checks

**Expected output:**
```
🔨 Building WS-001-01: User Models

→ Step 1: Write failing test
   ✅ Created test: tests/unit/test_user_models.py
   ❌ Test failed (expected)

→ Step 2: Implement minimal code
   ✅ Created: src/auth/models.py
   ✅ Test passed!

→ Step 3: Refactor implementation
   ✅ Code refactored

→ Step 4: Quality gates
   ✅ Tests passing (4/4)
   ✅ Coverage: 85% (≥80%)
   ✅ Mypy: 0 errors
   ✅ Ruff: 0 errors
   ✅ Complexity: CC < 10

✅ Workstream complete!
```

**Expected files created:**
```bash
# Implementation file
ls src/auth/models.py
# Output: src/auth/models.py

# Test file
ls tests/unit/test_user_models.py
# Output: tests/unit/test_user_models.py
```

**✅ Checkpoint:** Test file and implementation created, all quality gates pass.

---

## Step 4: Review Your Work (2 minutes)

Use `@review` to verify quality before moving on.

```bash
# Review the completed workstream
@review WS-001-01
```

**Expected output:**
```
📊 Review Report for WS-001-01

✅ Code Quality
   - Lines of code: 45 (<200)
   - Test coverage: 85% (≥80%)
   - Type hints: Complete
   - No tech debt markers

✅ Architecture
   - Clean layer separation: OK
   - No circular dependencies

✅ Documentation
   - Function docstrings: Complete
   - Module docstring: Present

✅ Tests
   - All tests passing
   - Fast marker: Applied
   - No print statements

🎉 Quality score: 95/100
```

**✅ Checkpoint:** All quality checks pass with score ≥80.

---

## Step 5: Build Remaining Workstreams (3 minutes)

Continue building the remaining workstreams.

```bash
# Build the second workstream
@build WS-001-02

# Build the third workstream
@build WS-001-03

# Build the fourth workstream
@build WS-001-04
```

**Watch the pattern:**
- Each `@build` follows the same Red → Green → Refactor cycle
- Quality gates enforce standards automatically
- SDP tracks progress in real-time

**Expected output per workstream:**
```
✅ Tests passing
✅ Coverage ≥80%
✅ No tech debt
✅ Code complexity OK
```

**✅ Checkpoint:** All 4 workstreams complete, all tests pass.

---

## Step 6: Final Feature Review (1 minute)

After all workstreams complete, review the entire feature.

```bash
# Review the complete feature
@review F01
```

**Expected output:**
```
🎉 Feature Review: F01 - User Authentication

✅ Implementation Complete
   Workstreams: 4/4 completed
   Total time: 45 minutes
   Test coverage: 87%

✅ Quality Gates
   All files <200 LOC: ✓
   Type hints: ✓
   No tech debt: ✓
   Complexity OK: ✓

📦 Ready for integration
   Run: @deploy F01
```

**✅ Checkpoint:** Feature complete, ready for deployment.

---

## Troubleshooting Common Issues

### Issue 1: Test Fails After Implementation

**Symptom:** Test still fails after code implementation

**Solution:**
```bash
# Check test output
pytest tests/unit/test_user_models.py -v

# Common fixes:
# 1. Check for typos in function names
# 2. Verify import statements
# 3. Check assertion logic
```

---

### Issue 2: Coverage Below 80%

**Symptom:** Quality gate fails with "Coverage: 75% (<80%)"

**Solution:**
```bash
# See which lines aren't covered
pytest tests/unit/test_user_models.py --cov=auth/models --cov-report=term-missing

# Add tests for missing paths
# Example: Test error cases, edge cases, all branches
```

---

### Issue 3: Type Hint Errors

**Symptom:** Mypy reports "Missing type annotation"

**Solution:**
```bash
# Check specific errors
mypy src/auth/models.py --strict

# Add type hints:
def get_user(user_id: int) -> User | None:
    #     ^^^^^^^    ^^^^^^^^^^^^^^^^
    #    parameter      return type
```

---

### Issue 4: Complexity Too High

**Symptom:** Radon reports "CC > 10"

**Solution:**
```bash
# Check complexity
radon cc src/auth/models.py -a

# Refactor: Extract helper functions
def complex_function(x, y, z):
    # Split into smaller functions
    result = helper1(x, y)
    result = helper2(result, z)
    return result
```

---

### Issue 5: Import Errors

**Symptom:** "ModuleNotFoundError: No module named 'auth'"

**Solution:**
```bash
# Verify you're in the right directory
pwd
# Should be in project root

# Install dependencies
poetry install

# Check module structure
ls src/auth/
```

---

## What You Learned

Congratulations! 🎉 You've completed the SDP Quick Start tutorial.

**You now know how to:**
1. ✅ Create features using `@feature`
2. ✅ Design workstreams automatically
3. ✅ Execute workstreams with `@build`
4. ✅ Validate quality with `@review`
5. ✅ Troubleshoot common issues

**Key SDP concepts:**
- **Test-Driven Development:** Tests written before code
- **Quality Gates:** Automatic validation (coverage, complexity, types)
- **Clean Architecture:** Enforced layer separation
- **Small Files:** Everything under 200 LOC
- **No Tech Debt:** "Fix it now" mentality

---

## Next Steps

**Continue learning:**
- 📖 Read [PROTOCOL.md](../PROTOCOL.md) - Full SDP specification
- 📖 Read [CLAUDE.md](../CLAUDE.md) - Integration guide
- 🔧 Try advanced workflows: `@oneshot`, `@design`, `@idea`

**Build your own feature:**
```bash
@feature "Your feature idea here"
```

**Get help:**
- 💬 Join the [SDP Discord](https://discord.gg/sdp)
- 🐛 [Report issues](https://github.com/fall-out-bug/sdp/issues)
- 📧 Email: sdp-support@example.com

---

## Tutorial Checklist

Use this checklist to track your progress:

- [ ] Prerequisites installed (Python, Poetry, Git)
- [ ] Created first feature with `@feature`
- [ ] Reviewed generated workstreams
- [ ] Built first workstream with `@build`
- [ ] Reviewed work with `@review`
- [ ] Built remaining workstreams
- [ ] Completed final feature review
- [ ] Troubleshooted at least one issue

**Time spent:** _____ minutes

**What was most helpful?** _________________________________

**What was confusing?** ___________________________________

---

## Feedback

**How was this tutorial?**
- Too easy / Just right / Too hard
- Too fast / Just right / Too slow
- More examples / Fewer examples

**Rate this tutorial:** ⭐⭐⭐⭐⭐ (1-5)

**Your feedback helps improve SDP!** [Take 1-minute survey](https://forms.gle/sdp-tutorial)

---

**🎉 You're ready to use SDP!**

Go build something amazing. 🚀
