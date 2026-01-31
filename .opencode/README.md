# OpenCode Integration

**Commands moved to:** `.claude/skills/`

All SDP commands are now unified in `.claude/skills/` directory.

## Usage

Use `/` prefix to invoke commands:

```bash
/feature "description"  # Unified entry point
/idea "description"     # Requirements gathering
/design {id}            # Plan workstreams
/build {ws-id}          # Execute workstream
/review {feature}       # Quality review
/deploy {feature}       # Production deployment
/debug "issue"          # Systematic debugging
/hotfix "critical"      # Emergency fix
/bugfix "issue"         # Quality fix
```

## See Also

- [CLAUDE.md](../CLAUDE.md) - Full protocol
- [.claude/skills/](../.claude/skills/) - All skill definitions
