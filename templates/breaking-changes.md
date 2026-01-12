# Breaking Changes

**Version:** {version}
**Date:** {YYYY-MM-DD}
**Feature:** {FXX}

---

## Summary

This release contains breaking changes that require action before upgrading.

**Total breaking changes:** {count}

---

## API Changes

### CRITICAL: Removed endpoint

**Endpoint:** `POST /old-endpoint`  
**Status:** REMOVED  
**Replacement:** `POST /new-endpoint`

**Impact:** All API clients using this endpoint will fail.

**Migration:**
```python
# Before
response = requests.post("https://api/old-endpoint", json=data)

# After
response = requests.post("https://api/new-endpoint", json=data)
```

---

## CLI Changes

### HIGH: Changed argument name

**Command:** `hwc grading run`  
**Changed:** `--repo-url` → `--repo`

**Impact:** Scripts using old argument name will fail.

**Migration:**
```bash
# Before
hwc grading run --repo-url https://...

# After
hwc grading run --repo https://...
```

---

## Database Changes

### CRITICAL: Dropped column

**Table:** `submissions`  
**Column:** `old_field` (dropped)

**Impact:** Queries referencing this column will fail.

**Migration:** Run migration script (see MIGRATION_GUIDE.md)

---

## Configuration Changes

### MEDIUM: Config key renamed

**Key:** `OLD_CONFIG_KEY` → `NEW_CONFIG_KEY`

**Impact:** Old config files will not work.

**Migration:**
```yaml
# Before
OLD_CONFIG_KEY: value

# After
NEW_CONFIG_KEY: value
```

---

## Checklist

Before upgrading:

- [ ] Read full MIGRATION_GUIDE.md
- [ ] Backup production database
- [ ] Update API client code
- [ ] Update CLI scripts
- [ ] Update configuration files
- [ ] Test on staging
- [ ] Plan rollback strategy

---

## Timeline

| Date | Action |
|------|--------|
| {YYYY-MM-DD} | Breaking changes announced |
| {YYYY-MM-DD + 7d} | Deploy to staging |
| {YYYY-MM-DD + 14d} | Deploy to production |
| {YYYY-MM-DD + 30d} | Old behavior fully deprecated |

---

## Support

Questions? Open an issue: {issue_tracker_url}
