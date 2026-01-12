# Release Notes Template

## Version {X.Y.Z} - {YYYY-MM-DD}

### Overview

{Brief description of what's added in this release — 2-3 sentences}

---

## 🚀 New Features

### {Feature Name}

{Description of functionality for users}

**What's new:**
- {Item 1}
- {Item 2}
- {Item 3}

**Usage:**

```bash
# Example command or usage
app {command} {args}
```

**API (if applicable):**

```bash
# Example API request
curl -X POST http://localhost:8000/api/endpoint \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

---

## ⬆️ Improvements

- {Improvement 1}
- {Improvement 2}

---

## 🐛 Bug Fixes

- {Fix 1}
- {Fix 2}

---

## ⚠️ Breaking Changes

{If no breaking changes, write "None"}

**Before:**
```python
# Old way
old_function(arg1, arg2)
```

**After:**
```python
# New way
new_function(arg1, arg2, arg3)
```

**Migration:**
1. Replace `old_function` with `new_function`
2. Add third argument

---

## 📋 Migration Guide

{If no migration required, write "No migration required"}

### Database Migrations

```bash
# Run migrations
poetry run alembic upgrade head
```

### Configuration Changes

{If configuration format changed}

```yaml
# Before
old_config: value

# After
new_config:
  nested: value
```

---

## 🔍 Known Issues

{If no known issues, write "None"}

- {Issue 1}: {description} — workaround: {how to work around}
- {Issue 2}: {description}

---

## 📦 Dependencies

### Added
- {New library}: v{version} — {purpose}

### Removed
- {Removed library} — {why removed}

---

## 📚 Documentation

- [Full documentation](docs/)
- [API reference](docs/api/)
- [Migration guide](docs/migration/)

---

## 🙏 Contributors

- {Contributor 1}
- {Contributor 2}
