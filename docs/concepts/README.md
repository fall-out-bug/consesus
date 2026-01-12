# Concepts

Core concepts that underpin the Spec-Driven Protocol.

## Foundation

| Concept | Description | Document |
|---------|-------------|----------|
| **Principles** | SOLID, DRY, KISS, YAGNI, Clean Code | [PRINCIPLES.md](../PRINCIPLES.md) |
| **Clean Architecture** | Layer separation, dependency inversion | [clean-architecture/](clean-architecture/README.md) |
| **Artifacts** | Specs, ADRs, design docs, test reports | [artifacts/](artifacts/README.md) |

## Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         PRINCIPLES                               │
│              SOLID • DRY • KISS • YAGNI • Clean Code             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐                                          │
│  │ CLEAN ARCHITECTURE│                                          │
│  │                   │                                          │
│  │   Presentation    │                                          │
│  │        ↓          │                                          │
│  │  Infrastructure   │                                          │
│  │        ↓          │                                          │
│  │   Application     │                                          │
│  │        ↓          │                                          │
│  │     Domain        │             ┌─────────────┐              │
│  │                   │             │  ARTIFACTS  │              │
│  └──────────────────┘             │             │              │
│                                    │ Specs       │              │
│                                    │ ADRs        │              │
│                                    │ Designs     │              │
│                                    │ Tests       │              │
│                                    └─────────────┘              │
└─────────────────────────────────────────────────────────────────┘
```

## How They Connect

### Principles → Architecture

Principles like **SRP** and **DIP** directly inform Clean Architecture layers:
- SRP: Each layer has one responsibility
- DIP: Inner layers don't depend on outer layers

### Architecture → Workstreams

Clean Architecture layers guide workstream decomposition:
- WS-01: Domain entities (inner layer first)
- WS-02: Application services (uses domain)
- WS-03: Infrastructure adapters (implements ports)
- WS-04: Presentation (outer layer last)

## Reading Order

For newcomers:
1. [PRINCIPLES.md](../PRINCIPLES.md) — Start with the fundamentals
2. [clean-architecture/README.md](clean-architecture/README.md) — Understand layer separation
3. [artifacts/README.md](artifacts/README.md) — Learn what to produce

For quick reference:
- [PROTOCOL.md](../../PROTOCOL.md) — Full SDP specification
- [CODE_PATTERNS.md](../../CODE_PATTERNS.md) — Implementation patterns

## Integration with SDP

These concepts are enforced through:

| Gate | Concepts Checked |
|------|-----------------|
| /design → /build | Clean Architecture layers, SOLID |
| /build execution | DRY, KISS, proper roles |
| /review | All principles, artifact completeness |
| Pre-commit | Layer violations, code quality |

---

**See also**: [PROTOCOL.md](../../PROTOCOL.md) | [CODE_PATTERNS.md](../../CODE_PATTERNS.md)
