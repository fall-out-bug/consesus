# Model Recommendations for SDP

This guide provides recommendations for selecting AI models when working with the Spec-Driven Protocol.

**Note**: AI model capabilities change rapidly. Check official provider documentation for current offerings and benchmarks.

## Quick Command Assignments

| Command | Recommended Model | Why |
|---------|-------------------|-----|
| `/idea` | Medium | Requirements gathering needs understanding |
| `/design` | Capable | Architecture planning is critical |
| `/build` | Fast | Implementation benefits from quick iteration |
| `/review` | Capable | Quality checks need thoroughness |
| `/deploy` | Fast | Config generation is routine |
| `/issue` | Medium | Debugging needs analysis |
| `/hotfix` | Fast | Speed is critical |
| `/bugfix` | Fast | Straightforward fixes |
| `/oneshot` | Capable | Autonomous execution needs reliability |

## General Principles

1. **Strategic commands** (`/design`, `/review`, `/oneshot`) benefit from more capable models
2. **Implementation commands** (`/build`, `/deploy`, `/hotfix`) work well with faster models
3. **Start fast, escalate if needed** - try faster model first, use capable model only when stuck

## For Claude Code Users

Claude Code supports Claude models only. Use `/model` command to switch:

```
/model opus    # Most capable - for /design, /review, /oneshot
/model sonnet  # Balanced - for /idea, /issue
/model haiku   # Fastest - for /build, /deploy, /hotfix, /bugfix
```

### Recommended Assignment

| Command | Model | Switch Command |
|---------|-------|----------------|
| `/idea` | Sonnet | `/model sonnet` |
| `/design` | Opus | `/model opus` |
| `/build` | Haiku/Sonnet | `/model haiku` |
| `/review` | Opus | `/model opus` |
| `/deploy` | Haiku | `/model haiku` |
| `/issue` | Sonnet | `/model sonnet` |
| `/hotfix` | Haiku | `/model haiku` |
| `/bugfix` | Haiku | `/model haiku` |
| `/oneshot` | Opus | `/model opus` |

## For Cursor Users

Cursor supports multiple providers. Configure in Settings → Models.

### Suggested Strategy

- **Strategic work** (`/design`, `/review`, `/oneshot`): Use most capable model (Claude Opus, GPT-4)
- **Implementation** (`/build`, `/deploy`, fixes): Use fast model (Claude Haiku, GPT-4 Turbo)
- **Check Cursor's current offerings** - they change frequently

## Cost Optimization

### Strategy 1: Quality-First
Use capable models for all commands. Higher cost, best results.

### Strategy 2: Balanced (Recommended)
- Strategic commands (`/design`, `/review`, `/oneshot`): Capable model
- Implementation commands (`/build`, `/deploy`, fixes): Fast model

### Strategy 3: Budget
Use fast models for all commands. Lowest cost, adequate for many projects.

## Model Selection Tips

1. **Match model to task complexity**
   - Simple tasks → Fast model
   - Complex reasoning → Capable model

2. **Escalate when stuck**
   - Start with fast model
   - If 2+ iterations without progress, switch to capable model

3. **Strategic decisions matter most**
   - `/design` sets the architecture foundation
   - `/review` ensures quality gates
   - Don't skimp on these commands

4. **Implementation is repetitive**
   - `/build`, `/deploy` do similar tasks repeatedly
   - Fast models work well here

5. **Speed matters for fixes**
   - `/hotfix` prioritizes speed over capability
   - `/bugfix` benefits from quick turnaround

## Current Model Landscape

Check these sources for current benchmarks:
- [SWE-bench](https://www.swebench.com/) - Coding benchmark leaderboard
- [Anthropic Models](https://docs.anthropic.com/claude/docs/models-overview) - Claude specifications
- [OpenAI Models](https://platform.openai.com/docs/models) - GPT specifications
- [Google AI](https://ai.google.dev/models) - Gemini specifications

---

**Note**: This guide focuses on principles rather than specific model versions, as the AI landscape evolves rapidly. Always verify current model capabilities with official documentation.
