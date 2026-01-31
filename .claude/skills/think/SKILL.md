---
name: think
description: Deep structured thinking with parallel agents (INTERNAL - used by @idea and @design)
tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, Task
---

# /think - Deep Structured Thinking

**INTERNAL SKILL** — Used by `@idea` and `@design` for deep analysis with parallel expert agents.

## Purpose

When a problem needs deeper exploration than surface-level questions:
- Complex tradeoffs with no clear answer
- Architectural decisions with multiple valid approaches
- Unknown unknowns in requirements
- System-level implications

## When @idea or @design Should Call This

**@idea calls /think when:**
- Requirements have significant ambiguity
- Multiple user types with conflicting needs
- Technical approach unclear
- Success metrics debatable

**@design calls /think when:**
- Architecture has multiple valid approaches
- Integration points complex
- Failure modes unclear
- Performance/security tradeoffs significant

## Parallel Expert Agents Pattern

### Step 1: Define Expert Roles

For complex problems, spawn 2-4 parallel expert agents:

| Expert | Focus | When to Use |
|--------|-------|-------------|
| **Architect** | System design, patterns, modularity | All architectural decisions |
| **Security** | Threats, auth, data protection | User data, APIs, external integration |
| **Performance** | Latency, throughput, scalability | High load, real-time requirements |
| **UX** | User experience, discoverability | User-facing features |
| **Ops** | Deployability, monitoring, failure modes | Production systems |

### Step 2: Launch Parallel Analysis

```python
# Spawn experts in parallel (single message)
Task(
    subagent_type="general-purpose",
    prompt="""You are the ARCHITECT expert for this problem.

PROBLEM: {problem_description}

Your expertise: System design, patterns, modularity, clean architecture

Explore the problem from your perspective:
1. What are the key architectural considerations?
2. What patterns apply here?
3. What are the risks?

Return your analysis in 3-5 bullet points.""",
    description="Architect analysis"
)

# Launch other experts similarly...
```

**All agents run in parallel** — user sees all thoughts simultaneously.

### Step 3: Aggregate and Synthesize

After all experts complete, synthesize:

```markdown
## Expert Analysis Summary

### @architect
- Clean architecture suggests domain layer first
- Risk: tight coupling to existing services

### @security
- Need threat modeling for user data
- OAuth2 preferred over custom auth

### @performance
- Caching strategy needed for read-heavy workload
- Database indexing critical for query performance

### Synthesis
Combining all perspectives, recommended approach: ...
```

## Single-Agent Mode (Simple Problems)

For straightforward problems, skip parallel agents:

1. **Deconstruct** the problem into dimensions
2. **Explore** 3+ angles (ideal/pragmatic/minimal)
3. **Synthesize** insights
4. **Present** findings

## Output Format

```markdown
## Problem Analysis

### Context
{Brief problem statement}

### Expert Analysis

**@architect:** {analysis}
**@security:** {analysis}
**@performance:** {analysis}

### Synthesis
{Combined insights}

### Recommendation
{Clear recommendation with rationale}

### Open Questions
{What remains unknown}
```

## Principles

- **Parallel exploration** — Multiple experts run simultaneously
- **Real-time thoughts** — User sees all expert thoughts as they complete
- **Role-based expertise** — Each expert has defined perspective
- **Synthesis** — Combine insights into coherent recommendation
- **Explicit tradeoffs** — State what you're optimizing for

## Exit When

- All experts have completed analysis (parallel mode) OR
- All angles explored (single mode)
- Tradeoffs are explicit
- Recommendation is clear with rationale

## Example: Parallel Expert Output

```
User: @idea "Add real-time notifications to dashboard"

@idea agent: This requires deeper analysis. Calling /think...

→ Spawning 4 expert agents in parallel:
  • @architect - System design analysis
  • @security - Threat modeling
  • @performance - Scalability concerns
  • @ux - User experience implications

[All agents run simultaneously]

ARCHITECT AGENT:
→ Analyzing system design...
Key considerations:
- WebSocket vs Server-Sent Events (SSE) tradeoff
- Need pub/sub pattern for multi-server support
- Risk: tight coupling to existing API structure
- Pattern: Event-driven architecture with message broker
Recommendation: Redis pub/sub with WebSocket fallback

SECURITY AGENT:
→ Analyzing threats...
Threat analysis:
- WebSocket connections are stateful, need auth per connection
- Risk: token replay attacks if not properly secured
- Need rate limiting to prevent DOS via connection spam
- CORS policy must whitelist specific origins only
Recommendation: JWT tokens with short expiry, per-connection auth

PERFORMANCE AGENT:
→ Analyzing scalability...
Performance concerns:
- Each WebSocket connection holds memory (~50KB)
- 10K concurrent users = ~500MB memory overhead
- Redis pub/sub adds ~5ms latency per message
- Need connection pooling strategy
Recommendation: Horizontal scaling with sticky sessions

UX AGENT:
→ Analyzing user experience...
UX implications:
- Real-time updates improve perceived performance
- Risk: notification fatigue if too frequent
- Need clear visual indicators for new notifications
- Offline state handling critical for mobile users
Recommendation: Batched updates (max 1/second), clear UI states

## Synthesis

Combining all expert perspectives:

**Technical Approach:**
- Use WebSocket with SSE fallback (progressive enhancement)
- Redis pub/sub for server-to-server messaging
- JWT auth per connection with 5-min expiry

**Architecture:**
```
Browser ← WebSocket → API Server ← Redis Pub/Sub → Other API Servers
```

**Key Tradeoffs:**
- Complexity (+) vs Real-time UX (+++)
- Memory overhead (~500MB for 10K users) vs User engagement (high)
- Added Redis dependency vs Simplified scaling

**Recommendation:** 
Proceed with real-time notifications using WebSocket + Redis pub/sub.
Benefits (user engagement, perceived performance) outweigh costs (complexity, memory).

**Open Questions:**
1. What notification types are highest priority? (affects batching strategy)
2. Do we need notification history? (affects storage requirements)
3. Mobile app integration planned? (affects fallback strategy)

@idea agent: Let me ask you about these open questions...
```
