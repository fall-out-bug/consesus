# Model Recommendations for Consensus Agents

This guide provides recommendations for selecting AI models for each agent role in the consensus workflow. The right model choice balances capability, cost, and latency.

**Key Update (Dec 2025):** Claude Haiku 4.5 changed the game - it matches Sonnet 4 performance at 4-5x speed and fraction of cost. **Use Haiku 4.5 for 80% of tasks.**

## Quick Reference Matrix

| Role | Tier | Claude | Notes |
|------|------|--------|-------|
| **Analyst** | High | **opus-4.5** | Complex requirements analysis |
| **Architect** | High | **opus-4.5** | System design, trade-offs |
| **Tech Lead** | Medium | **sonnet-4.5** | Planning, complex refactoring |
| **Developer** | Standard | **haiku-4.5** | Implementation, TDD (73% SWE-bench!) |
| **QA** | Standard | **haiku-4.5** | Testing, verification |
| **DevOps** | Standard | **haiku-4.5** | CI/CD, deployment |
| **SRE** | Standard | **haiku-4.5** | Observability, runbooks |
| **Security** | High | **opus-4.5** | Threat modeling |
| **Data/ML Quality** | Medium | **sonnet-4.5** | ML artifacts, data validation |
| **Documentation** | Standard | **haiku-4.5** | Docs curation |
| **Prompt Engineer** | Medium | **sonnet-4.5** | Prompt design, RAG |

## Tier Definitions

### High Tier (Strategic Decisions)
**When to use:** Architecture decisions, security reviews, complex trade-offs, initial requirements with ambiguity.

**Characteristics:**
- Multi-step reasoning required
- High stakes decisions (vetoes, architecture)
- Ambiguous or incomplete inputs
- Need to synthesize multiple sources

**Recommended:**
- Claude: `claude-opus-4-5-20251101`

**Cost:** ~$15 per 1M input tokens, ~$75 per 1M output tokens
**Token budget:** 2000-2500 per epic

### Medium Tier (Complex Execution)
**When to use:** Complex refactoring, cross-epic analysis, sophisticated planning, ML pipelines.

**Characteristics:**
- Needs deep codebase understanding
- Multi-file coordination
- Performance optimization
- Trade-off analysis in implementation

**Recommended:**
- Claude: `claude-sonnet-4-5-20250929`

**Cost:** ~$3 per 1M input tokens, ~$15 per 1M output tokens
**Token budget:** 1500-2000 per task

### Standard Tier (Implementation & Operations)
**When to use:** 80% of development tasks - implementation, testing, CI/CD, documentation.

**Characteristics:**
- Clear specifications provided
- Pattern-following tasks
- Code generation with TDD
- Test verification
- Deployment scripts
- Documentation updates

**Recommended:**
- Claude: `claude-haiku-4-5-20241022` (73.3% SWE-bench Verified)

**Cost:** ~$1 per 1M input tokens, ~$5 per 1M output tokens (⚡ 4-5x faster than Sonnet!)
**Token budget:** 1000-1500 per task

**Why Haiku 4.5 is game-changing:**
- Matches Sonnet 4 performance on coding tasks
- World-class SWE-bench score (73.3%)
- Extended thinking, computer use, context awareness
- Perfect for multi-agent systems (fast sub-agents)

## Role-Specific Guidance

### Analyst
```
Tier: High
Why: Must understand business context, identify ambiguities, define testable requirements.
Key capabilities needed:
- Stakeholder intent interpretation
- Scope boundary detection
- Success metrics formulation
```

### Architect
```
Tier: High
Why: Critical decisions about system boundaries, layer violations, technical debt.
Key capabilities needed:
- Clean Architecture pattern recognition
- Trade-off analysis
- Integration complexity assessment
- Veto justification
```

### Tech Lead
```
Tier: High (planning) / Medium (review)
Why: Translates architecture to tasks, conducts code reviews, detects duplications.
Key capabilities needed:
- Task decomposition
- Code quality assessment
- Cross-epic duplication detection
Optimization: Use High tier for planning, Medium for routine reviews.
```

### Developer
```
Tier: Standard (Haiku 4.5)
Why: Follows specifications, writes tests and code, respects boundaries. Haiku 4.5 scores 73% on SWE-bench!
Key capabilities needed:
- TDD execution
- Clean Code practices
- Codebase navigation
- Error handling patterns
Note: Escalate to Sonnet 4.5 only for complex refactoring across 5+ files or unfamiliar domains.
```

### QA
```
Tier: Standard (Haiku 4.5)
Why: Verifies against acceptance criteria, checks coverage, finds edge cases. Fast execution critical.
Key capabilities needed:
- Test case generation
- Coverage analysis
- Regression detection
- Performance: 4-5x faster than Sonnet for test verification
```

### Security
```
Tier: High
Why: Threat modeling requires understanding attack vectors and system interactions.
Key capabilities needed:
- OWASP awareness
- Secret handling verification
- Auth/authz pattern recognition
```

## Cost Optimization Strategies

### 1. Default to Haiku 4.5 (NEW!)
**Start with Haiku 4.5 for all implementation tasks.**

**Why:** 73% SWE-bench score at $1/$5 per 1M tokens (vs Sonnet 4.5 at $3/$15)
**When:** Developer, QA, DevOps, SRE, Documentation
**Savings:** 70% cost reduction vs Sonnet 4.5, same quality

### 2. Quick Prompts for Routine Tasks
Use `prompts/quick/{role}_quick.md` (200-400 tokens) instead of full prompts (1500-2500 tokens).

**Savings:** 80-88% token reduction

**When to use quick prompts:**
- Iteration 2+ (context already established)
- Simple bug fixes
- Documentation updates
- Status messages

**Combine with Haiku 4.5:** 94% total cost reduction vs full prompt + Opus 4.5

### 3. Tiered Escalation
Start with Standard (Haiku 4.5), escalate only if needed:

```
Haiku 4.5 → fails after 2 iterations
  ↓
Sonnet 4.5 → complex refactoring/analysis
  ↓
Opus 4.5 → only for architecture/security decisions
```

**Warning signs to escalate:**
- Agent requests clarification (veto)
- Complex trade-offs emerge
- Multiple iterations without consensus
- Cross-file dependencies not recognized

### 4. Parallel Execution (Haiku 4.5 Speed)
For independent workstreams, run in parallel:
- 4-5x faster than Sonnet 4.5
- Developer + QA can run simultaneously
- DevOps + SRE in parallel

### 5. Context Caching (Claude)
When using Claude models with prompt caching:
- Place static content (prompts, rules) at the beginning
- Dynamic content (epic-specific) at the end
- Cache reduces costs by up to 90% on repeated content
- Especially effective with Haiku 4.5 (already cheap + caching = nearly free)

## Model-Specific Considerations

### Claude Models (December 2025)

**Opus 4.5** (`claude-opus-4-5-20251101`)
- **Use for:** Analyst, Architect, Security
- **Strengths:** Best reasoning, handles ambiguity, strategic decisions
- **Cost:** $15/$75 per 1M tokens
- **Latency:** Highest (~20-30s for complex tasks)

**Sonnet 4.5** (`claude-sonnet-4-5-20250929`)
- **Use for:** Tech Lead, complex refactoring, ML pipelines
- **Strengths:** Deep codebase understanding, multi-file coordination
- **Cost:** $3/$15 per 1M tokens
- **Latency:** Medium (~5-10s)

**Haiku 4.5** (`claude-haiku-4-5-20241022`) ⭐ **RECOMMENDED DEFAULT**
- **Use for:** Developer, QA, DevOps, SRE, Documentation (80% of tasks!)
- **Strengths:**
  - 73.3% SWE-bench Verified (world-class coding)
  - Extended thinking + computer use
  - 4-5x faster than Sonnet 4.5
  - Perfect for multi-agent systems
- **Cost:** $1/$5 per 1M tokens (70% cheaper than Sonnet!)
- **Latency:** Lowest (~1-3s)

**Claude Code integration:**
```bash
# High tier (Analyst, Architect, Security)
claude --model claude-opus-4-5-20251101 \
       --system-prompt prompts/architect_prompt.md

# Medium tier (Tech Lead, complex tasks)
claude --model claude-sonnet-4-5-20250929 \
       --system-prompt prompts/tech_lead_prompt.md

# Standard tier (80% of tasks) - RECOMMENDED
claude --model claude-haiku-4-5-20241022 \
       --system-prompt prompts/quick/developer_quick.md
```

## Multi-Model Workflows

### Recommended Configuration (December 2025)
```
Epic Start (Strategic):
  Analyst: opus-4.5 (requirements clarity critical)
  Architect: opus-4.5 (architecture decisions)
  Cost: ~$20-30 per epic

Planning:
  Tech Lead: sonnet-4.5 (structured planning, cross-epic analysis)
  Cost: ~$5-10 per epic

Implementation (80% of work):
  Developer: haiku-4.5 ⭐ (TDD, code generation)
  QA: haiku-4.5 ⭐ (test verification, coverage)
  DevOps: haiku-4.5 ⭐ (CI/CD, deployment)
  SRE: haiku-4.5 ⭐ (observability, runbooks)
  Cost: ~$2-5 per workstream (70% savings!)

Review & Security:
  Security: opus-4.5 (threat modeling)
  Tech Lead: sonnet-4.5 (code review)
  Cost: ~$5-15 per epic

Total Epic Cost:
  Old (all Sonnet 4): ~$80-120
  New (Haiku 4.5 for 80%): ~$35-50
  Savings: 60% cost reduction 🎉
```

### Parallel Execution Strategy
**Haiku 4.5's speed enables true parallel workflows:**

```
Time: 0min
  ├─ Analyst (Opus 4.5): 10min → requirements.json
Time: 10min
  ├─ Architect (Opus 4.5): 15min → architecture.json
Time: 25min
  ├─ Tech Lead (Sonnet 4.5): 8min → implementation.md
Time: 33min
  ├─ Developer (Haiku 4.5): 5min → code + tests ⚡
  └─ DevOps (Haiku 4.5): 5min → CI/CD (parallel) ⚡
Time: 38min
  ├─ QA (Haiku 4.5): 3min → verification ⚡
  └─ SRE (Haiku 4.5): 3min → monitoring (parallel) ⚡
Time: 41min
  └─ Security (Opus 4.5): 10min → audit

Total: 51 minutes (vs 90+ minutes with all Sonnet 4)
```

### Fallback Strategy
If primary model unavailable:
1. Haiku 4.5 unavailable → Sonnet 4.5 (cost increase, slower)
2. Sonnet 4.5 unavailable → Haiku 4.5 for simple tasks, Opus 4.5 for complex
3. Opus 4.5 unavailable → Sonnet 4.5 (quality may decrease for architecture)

## Measuring Model Effectiveness

Track these metrics per role:
- **Veto rate:** High veto rate may indicate model mismatch
- **Iteration count:** More iterations = possible under-capability
- **Time to consensus:** Faster with right model tier
- **Token usage:** Compare actual vs budget

### Warning Signs
- Analyst missing edge cases → upgrade to High tier
- Developer creating duplications → check codebase search capability
- Architect approving layer violations → upgrade or add examples

## Updates

This guide should be updated when:
- New models are released
- Significant capability changes observed
- Cost structures change
- New roles are added

**Recent Updates:**
- **Dec 2025:** Added Claude Haiku 4.5 (game-changer for consensus workflows)
- **Oct 2025:** Claude Haiku 4.5 released - 73.3% SWE-bench, matches Sonnet 4 performance

## References

- [Claude Haiku 4.5 Announcement](https://www.anthropic.com/news/claude-haiku-4-5) - Official Anthropic announcement
- [Claude API Documentation](https://docs.anthropic.com/en/docs/about-claude/models) - Model specifications
- [SWE-bench Verified Scores](https://www.swebench.com/) - Coding benchmark

---

**Version:** 2.0
**Last Updated:** 2025-12-29
**Key Change:** Haiku 4.5 is now recommended default for 80% of development tasks
