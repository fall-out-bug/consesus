# Prompts

Command-based workflow for SDP.

## Slash Commands

Use these for one-shot execution:

```
/idea "{description}"           # Requirements gathering
/design idea-{slug}              # Workstream planning
/build WS-XXX-XX                 # Execute workstream
/review F{XX}                    # Quality review
/deploy F{XX}                    # Deployment
/issue "{description}"           # Debug and route
/hotfix "{description}"          # Emergency fix
/bugfix "{description}"          # Quality fix
/oneshot F{XX}                   # Autonomous execution
```

See `prompts/commands/*.md` for full prompts.

## Structured Workflow (Alternative)

Use 4-phase workflow for step-by-step execution:

```
@prompts/structured/phase-1-analyze.md   # Form WS map
@prompts/structured/phase-2-design.md    # Plan single WS
@prompts/structured/phase-3-implement.md # Execute WS
@prompts/structured/phase-4-review.md    # Review result
```

**Note**: Slash commands are recommended. Structured workflow is an alternative approach.

## When to Use Which Command

| Task | Command | Model |
|------|---------|-------|
| Start new feature | `/idea` | Sonnet |
| Plan workstreams | `/design` | Opus |
| Implement workstream | `/build` | Haiku |
| Review feature | `/review` | Opus |
| Deploy to production | `/deploy` | Haiku |
| Debug issue | `/issue` | Sonnet |
| Emergency fix | `/hotfix` | Haiku |
| Quality fix | `/bugfix` | Haiku |
| Autonomous execution | `/oneshot` | Opus |

## Guardrails and Quality Gates

See `PROTOCOL.md` — everything in one place.
