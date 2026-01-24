# SDP Update Workflow

**Last Updated:** 2026-01-24
**SDP Version:** v0.1.0+

---

## Overview

SDP (Spec-Driven Protocol) is now developed as an independent repository and consumed as a git submodule in various projects. This document describes the workflow for updating SDP across all projects.

---

## Core Principle

**SDP Development happens in the SDP repository. Projects consume SDP as a submodule.**

```
SDP Repository (github.com:fall-out-bug/sdp)
    ↓
    release (tag v0.X.0)
    ↓
    Projects update submodule
    ↓
┌───────────────┐
│ msu_ai_masters│ ← git submodule update
└───────────────┘
┌───────────────┐
│  hw_checker   │ ← git submodule update
└───────────────┘
┌───────────────┐
│  mlsd         │ ← git submodule update
└───────────────┘
```

---

## Scenario 1: Developing SDP Protocol Changes

**When:** You need to modify the SDP protocol itself.

### Workflow

```bash
# 1. Navigate to SDP repository
cd /tmp/sdp  # or your local SDP clone

# 2. Pull latest changes
git pull origin main

# 3. Create/Edit feature using SDP commands
/idea "Add new /review command"
/design idea-review-command

# 4. Execute workstreams
/build 00-600-01
/build 00-600-02

# 5. Run code review
/codereview F600

# 6. Commit changes
git add .
git commit -m "feat(sdp): F600 - Add /review command"

# 7. Create release tag
git tag -a v0.2.0 -m "SDP v0.2.0: Add /review command"

# 8. Push to remote
git push origin main
git push origin v0.2.0
```

---

## Scenario 2: Updating Projects to Use New SDP Version

**When:** SDP has a new release and you want to update projects.

### Manual Update (Recommended)

```bash
# In each project repository (msu_ai_masters, hw_checker, etc.)

# 1. Update submodule to latest
git submodule update --remote sdp

# 2. Review changes
cd sdp
git log --oneline HEAD@{1}..HEAD  # See what's new

# 3. Pin to specific version (RECOMMENDED)
git checkout v0.2.0
cd ..

# 4. Commit the update
git add sdp
git commit -m "chore(sdp): Update SDP to v0.2.0"
git push origin main
```

### Track Latest (Development Only)

```bash
# For development environments that always want latest
git submodule update --remote sdp
git add sdp
git commit -m "chore(sdp): Update SDP to latest"
```

---

## Scenario 3: Rollback SDP Update

**When:** A new SDP version has issues.

```bash
# In project repository

cd sdp
git checkout v0.1.0  # Previous version
cd ..

git add sdp
git commit -m "chore(sdp): Rollback SDP to v0.1.0"
git push origin main
```

---

## Quick Reference

| Action | Command |
|--------|---------|
| Update to latest | `git submodule update --remote sdp` |
| Pin to version | `cd sdp && git checkout vX.Y.Z && cd ..` |
| Check version | `cd sdp && git describe --tags && cd ..` |
| See what's new | `cd sdp && git log HEAD@{1}..HEAD --oneline` |
| Rollback | `cd sdp && git checkout v0.1.0 && cd ..` |

---

## Best Practices

1. **Always pin to specific versions** in production
2. **Test in staging before production**
3. **Update projects one at a time** (gradual rollout)
4. **Review changelog** before updating

---

## Related Documentation

- [SDP PROTOCOL.md](../PROTOCOL.md)
- [Migration Guide](../migration/ws-naming-migration.md)
- [Extension System](../extensions/README.md)

---

**Last Reviewed:** 2026-01-24
EOF
