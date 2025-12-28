# Model Recommendations for Consensus Agents

This guide provides recommendations for selecting AI models for each agent role in the consensus workflow. The right model choice balances capability, cost, and latency.

## Quick Reference Matrix

| Role | Tier | Claude | OpenAI | Notes |
|------|------|--------|--------|-------|
| **Analyst** | High | opus-4 | gpt-4o | Complex requirements analysis |
| **Architect** | High | opus-4 | gpt-4o | System design, trade-offs |
| **Tech Lead** | High | opus-4, sonnet-4 | gpt-4o | Planning, code review |
| **Developer** | Medium | sonnet-4 | gpt-4o-mini | Implementation, TDD |
| **QA** | Medium | sonnet-4 | gpt-4o-mini | Testing, verification |
| **DevOps** | Medium | sonnet-4 | gpt-4o-mini | CI/CD, deployment |
| **SRE** | Medium | sonnet-4 | gpt-4o-mini | Observability, runbooks |
| **Security** | High | opus-4 | gpt-4o | Threat modeling |
| **Data/ML Quality** | High | opus-4 | gpt-4o | ML artifacts, data validation |
| **Documentation** | Low | haiku-3.5 | gpt-4o-mini | Docs curation |
| **Prompt Engineer** | High | opus-4 | gpt-4o | Prompt design, RAG |

## Tier Definitions

### High Tier (Complex Reasoning)
**When to use:** Architecture decisions, security reviews, complex trade-offs, requirements with ambiguity.

**Characteristics:**
- Multi-step reasoning required
- High stakes decisions (vetoes, architecture)
- Ambiguous or incomplete inputs
- Need to synthesize multiple sources

**Recommended:**
- Claude: `claude-opus-4-5-20251101`, `claude-opus-4-20250514`
- OpenAI: `gpt-4o`, `gpt-4-turbo`

**Token budget:** 2000-2500 per epic

### Medium Tier (Structured Execution)
**When to use:** Following established patterns, implementation, testing, deployment scripts.

**Characteristics:**
- Clear specifications provided
- Pattern-following tasks
- Code generation with tests
- Documentation updates

**Recommended:**
- Claude: `claude-sonnet-4-20250514`, `claude-3-5-sonnet-20241022`
- OpenAI: `gpt-4o-mini`, `gpt-4o`

**Token budget:** 1000-1500 per task

### Low Tier (Routine Tasks)
**When to use:** Simple updates, formatting, summarization, status reports.

**Characteristics:**
- Minimal reasoning required
- Template-based outputs
- Quick iterations needed
- Cost optimization priority

**Recommended:**
- Claude: `claude-3-5-haiku-20241022`
- OpenAI: `gpt-4o-mini`

**Token budget:** 500-800 per task

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
Tier: Medium
Why: Follows specifications, writes tests and code, respects boundaries.
Key capabilities needed:
- TDD execution
- Clean Code practices
- Codebase navigation
- Error handling patterns
Note: Can use High tier for complex refactoring or unfamiliar domains.
```

### QA
```
Tier: Medium
Why: Verifies against acceptance criteria, checks coverage, finds edge cases.
Key capabilities needed:
- Test case generation
- Coverage analysis
- Regression detection
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

### 1. Quick Prompts for Routine Tasks
Use `prompts/quick/{role}_quick.md` (200-400 tokens) instead of full prompts (1500-2500 tokens).

**Savings:** 80-88% token reduction

**When to use quick prompts:**
- Iteration 2+ (context already established)
- Simple bug fixes
- Documentation updates
- Status messages

### 2. Tiered Escalation
Start with Medium tier, escalate to High if:
- Agent requests clarification (veto)
- Complex trade-offs emerge
- Multiple iterations without consensus

### 3. Batch Processing
For multiple simple tasks:
- Use Low tier model
- Process in parallel
- Human review at end

### 4. Context Caching (Claude)
When using Claude models with prompt caching:
- Place static content (prompts, rules) at the beginning
- Dynamic content (epic-specific) at the end
- Cache reduces costs by up to 90% on repeated content

## Model-Specific Considerations

### Claude Models
**Strengths:**
- Long context window (200K tokens)
- Strong reasoning for architecture
- Good at following structured protocols
- Excellent code quality

**Considerations:**
- opus-4 has higher latency
- haiku-3.5 may miss subtle requirements
- Use system prompts for role context

**Claude Code integration:**
```bash
# Set model per agent
claude --model claude-opus-4-5-20251101 --system-prompt prompts/architect_prompt.md

# Or use quick prompts
claude --model claude-sonnet-4-20250514 --system-prompt prompts/quick/developer_quick.md
```

### OpenAI Models
**Strengths:**
- Fast responses (gpt-4o-mini)
- Good tool use
- Consistent outputs

**Considerations:**
- Shorter context (128K)
- May need more explicit structure
- Function calling for artifacts

## Multi-Model Workflows

### Recommended Configuration
```
Epic Start:
  Analyst: opus-4 (requirements clarity critical)
  Architect: opus-4 (architecture decisions)

Planning:
  Tech Lead: sonnet-4 (structured planning)

Implementation (per workstream):
  Developer: sonnet-4 (code generation)
  QA: sonnet-4 (test verification)

Deployment:
  DevOps: sonnet-4 (scripts, configs)
  SRE: sonnet-4 (observability)

Review:
  Security: opus-4 (if security-sensitive)
  Tech Lead: opus-4 (cross-epic review)
```

### Fallback Strategy
If primary model unavailable:
1. High tier: fallback to other High tier model
2. Medium tier: can temporarily use High tier (cost increase)
3. Low tier: fallback to Medium tier

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

---

**Version:** 1.0
**Last Updated:** 2025-12-27
