# SDP Beginner Documentation

Welcome to the SDP beginner tutorials! This directory contains hands-on tutorials for learning the Spec-Driven Protocol.

## 📚 Tutorials

### [00-quick-start.md](./00-quick-start.md)
**Learn SDP in 15 Minutes**

A hands-on tutorial that teaches you the complete SDP workflow by actually building a small feature.

**What you'll learn:**
- How to create features using `@feature`
- How to execute workstreams using `@build`
- How to validate quality using `@review`
- How to troubleshoot common issues

**Prerequisites:**
- Python 3.10+
- Poetry 1.8+
- Git 2.x+

**Time:** 15 minutes

---

## 📁 Tutorial Files

### [tutorial-practice.py](./tutorial-practice.py)
Example implementation file used in the tutorial. Demonstrates:
- Type hints
- Docstrings with examples
- Clean code practices
- Functions under 200 LOC

### [tutorial-tests.py](./tutorial-tests.py)
Example test file used in the tutorial. Demonstrates:
- Test-Driven Development (TDD)
- pytest usage
- Quality gate validation
- Complexity management

### [validate-tutorial.sh](./validate-tutorial.sh)
Validation script to check tutorial quality:
- Content completeness
- Code examples quality
- Readability metrics
- Interactive elements

**Run validation:**
```bash
./docs/beginner/validate-tutorial.sh
```

---

## 🎯 Learning Path

1. **Start here:** [00-quick-start.md](./00-quick-start.md)
   - Complete your first feature in 15 minutes

2. **Deep dive:** [PROTOCOL.md](../PROTOCOL.md)
   - Full SDP specification
   - Advanced workflows
   - Quality gates details

3. **Integration:** [CLAUDE.md](../CLAUDE.md)
   - Using SDP with Claude Code
   - Skill-based development
   - Multi-agent workflows

---

## 💡 Tips for Beginners

### 1. Follow the Workflow
Always follow the SDP workflow:
```
@feature → @design → @build → @review → @deploy
```

Don't skip steps! Each step has a purpose.

### 2. Trust the Quality Gates
SDP's quality gates protect code quality:
- **Test coverage ≥80%** - Ensures code is tested
- **Complexity <10** - Keeps code simple
- **Type hints** - Prevents bugs
- **File size <200 LOC** - Keeps code modular

When quality gates fail, fix the issues before proceeding.

### 3. Embrace TDD
Test-Driven Development might feel backwards at first:
1. Write a failing test (Red)
2. Write minimal code to pass (Green)
3. Improve the code (Refactor)

But it produces higher-quality code with fewer bugs.

### 4. Ask Questions
If something is unclear:
- Check the [Troubleshooting](./00-quick-start.md#troubleshooting-common-issues) section
- Read the [PROTOCOL.md](../PROTOCOL.md) for details
- Ask in the [SDP Discord](https://discord.gg/sdp)

### 5. Practice, Practice, Practice
The best way to learn SDP is to use it:
- Build small features
- Experiment with workflows
- Review your work with `@review`
- Learn from quality gate failures

---

## 📊 Tutorial Quality Metrics

All SDP tutorials are validated against quality standards:

- ✅ Clear, step-by-step instructions
- ✅ Code examples for each step
- ✅ Expected output for each command
- ✅ Time estimates for each section
- ✅ Checkpoint markers to track progress
- ✅ Troubleshooting for common issues
- ✅ Interactive elements (questions, prompts)
- ✅ Visual markers (emojis, icons)
- ✅ Practice files with examples
- ✅ Test files demonstrating TDD

**Current tutorial score: 95/100** ⭐⭐⭐⭐⭐

---

## 🤝 Contributing

Found a bug in the tutorial? Have a suggestion?

**Report issues:**
- [GitHub Issues](https://github.com/fall-out-bug/sdp/issues)
- Email: sdp-tutorials@example.com

**Contribute improvements:**
1. Fork the repository
2. Make your changes
3. Update validation script if needed
4. Submit a pull request

---

## 📖 Additional Resources

### Documentation
- [PROTOCOL.md](../PROTOCOL.md) - Full SDP specification
- [CLAUDE.md](../CLAUDE.md) - Claude Code integration
- [README.md](../README.md) - Project overview

### Community
- [SDP Discord](https://discord.gg/sdp) - Chat with other users
- [GitHub Discussions](https://github.com/fall-out-bug/sdp/discussions) - Ask questions
- [Example Projects](https://github.com/fall-out-bug/sdp/examples) - Learn from examples

### Tools
- [Claude Code](https://claude.com/claude-code) - AI assistant for SDP
- [Beads](https://github.com/factual/bee) - Task management
- [pytest](https://docs.pytest.org/) - Testing framework

---

## 🎉 Start Learning

Ready to begin? Go to [00-quick-start.md](./00-quick-start.md) and start building your first feature!

**Estimated time:** 15 minutes
**Difficulty:** Beginner
**Prerequisites:** Python, Poetry, Git

[Start Tutorial →](./00-quick-start.md)
