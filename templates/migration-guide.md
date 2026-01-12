# Migration Guide: v{OLD} → v{NEW}

**From Version:** {X.Y.Z}
**To Version:** {X.Y.Z}
**Date:** {YYYY-MM-DD}

---

## Overview

{Brief description of what changed and why migration is needed}

---

## Prerequisites

Before migrating:

- [ ] Backup current database
- [ ] Backup current configuration
- [ ] Read release notes for v{NEW}
- [ ] Ensure downtime window (if needed)

### Backup Commands

```bash
# Database backup
pg_dump -h localhost -U postgres project_db > backup-$(date +%Y%m%d).sql

# Configuration backup
cp config.yaml config.yaml.backup
```

---

## Breaking Changes Summary

| Change | Impact | Action Required |
|--------|--------|-----------------|
| {change 1} | {who affected} | {what to do} |
| {change 2} | {who affected} | {what to do} |

---

## Step-by-Step Migration

### Step 1: Stop Services

```bash
docker-compose down
# or
systemctl stop project-service
```

### Step 2: Update Code

```bash
git fetch origin
git checkout v{NEW}
poetry install
```

### Step 3: Run Migrations

```bash
# Database migrations
poetry run alembic upgrade head

# Data migrations (if any)
poetry run python scripts/migrate_data.py
```

### Step 4: Update Configuration

**Old format:**
```yaml
old_setting: value
```

**New format:**
```yaml
new_setting:
  nested: value
```

### Step 5: Start Services

```bash
docker-compose up -d
# or
systemctl start project-service
```

### Step 6: Verify

```bash
# Health check
curl http://localhost:8000/health

# Run smoke tests
poetry run pytest tests/smoke/ -v
```

---

## API Changes

### Deprecated Endpoints

| Endpoint | Replacement | Removal Version |
|----------|-------------|-----------------|
| `GET /api/v1/old` | `GET /api/v2/new` | v{X.Y.Z} |

### New Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /api/v2/new` | {description} |

### Request/Response Changes

**Before:**
```json
{
  "old_field": "value"
}
```

**After:**
```json
{
  "new_field": "value",
  "additional_field": "value"
}
```

---

## Configuration Changes

### New Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `new_setting` | `value` | {what it does} |

### Removed Settings

| Setting | Replacement |
|---------|-------------|
| `old_setting` | Use `new_setting` instead |

### Changed Defaults

| Setting | Old Default | New Default | Reason |
|---------|-------------|-------------|--------|
| `timeout` | 30s | 60s | {reason} |

---

## Database Changes

### New Tables

```sql
CREATE TABLE new_table (
    id UUID PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

### Modified Tables

```sql
ALTER TABLE existing_table ADD COLUMN new_column VARCHAR(255);
```

### Data Migrations

```python
# scripts/migrate_data.py
# Run after schema migration

def migrate():
    # Transform old data to new format
    pass
```

---

## Rollback Procedure

If migration fails:

### Step 1: Stop Services

```bash
docker-compose down
```

### Step 2: Restore Database

```bash
psql -h localhost -U postgres project_db < backup-{date}.sql
```

### Step 3: Restore Code

```bash
git checkout v{OLD}
poetry install
```

### Step 4: Restore Configuration

```bash
cp config.yaml.backup config.yaml
```

### Step 5: Start Services

```bash
docker-compose up -d
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Migration fails with error X

**Symptom:** {what you see}

**Cause:** {why it happens}

**Solution:**
```bash
# Fix command
```

#### Issue 2: Service won't start

**Symptom:** {what you see}

**Cause:** {why it happens}

**Solution:**
1. Check logs: `docker-compose logs`
2. Verify config
3. {additional steps}

---

## Verification Checklist

After migration:

- [ ] All services running
- [ ] Health checks passing
- [ ] Smoke tests passing
- [ ] No errors in logs
- [ ] Key functionality works
- [ ] Performance acceptable

---

## Support

If you encounter issues:

1. Check troubleshooting section above
2. Review logs: `docker-compose logs -f`
3. Create issue with:
   - Error message
   - Steps to reproduce
   - Environment details

---

## Related Documents

- [Release Notes v{NEW}](releases/v{NEW}.md)
- [API Documentation](api/)
- [Configuration Reference](config/)
