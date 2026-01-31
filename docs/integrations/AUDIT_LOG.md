# Audit Log

Centralized logging system for all workflow events.

## Configuration

```bash
# Environment variables
export AUDIT_LOG_FILE="/var/log/consensus-audit.log"  # Default: /tmp/consensus-audit.log
export LOG_TO_FILE="true"   # Write to file (default: true)
export LOG_TO_STDOUT="false" # Print to stdout (default: false)
```

## Usage

```bash
# Log command execution
bash sdp/notifications/audit-log.sh command_started "/design" "F60"
bash sdp/notifications/audit-log.sh command_completed "/design" "F60" "success"

# Log WS lifecycle
bash sdp/notifications/audit-log.sh ws_started "WS-060-01"
bash sdp/notifications/audit-log.sh ws_completed "WS-060-01" "350" "85"
bash sdp/notifications/audit-log.sh ws_failed "WS-060-01" "tests failed"

# Log review
bash sdp/notifications/audit-log.sh review_started "F60"
bash sdp/notifications/audit-log.sh review_completed "F60" "APPROVED"

# Log deployment
bash sdp/notifications/audit-log.sh deploy_started "F60" "staging"
bash sdp/notifications/audit-log.sh deploy_completed "F60" "production" "v1.5.0"

# Log hotfix
bash sdp/notifications/audit-log.sh hotfix_started "001" "api-500"
bash sdp/notifications/audit-log.sh hotfix_deployed "001" "30m"

# Log Git operations
bash sdp/notifications/audit-log.sh git_push "main" "abc123d"
bash sdp/notifications/audit-log.sh git_merge "feature/lms" "main"

# Log breaking changes
bash sdp/notifications/audit-log.sh breaking_change "API" "3"

# Log approval gates
bash sdp/notifications/audit-log.sh approval_gate "PR" "123" "approved"
```

## Log Format

```
ISO8601|EVENT_TYPE|USER|GIT_BRANCH|EVENT_DATA
```

**Example:**
```
2026-01-11T00:30:15+03:00|WS_START|fall_out_bug|feature/lms-integration|ws=WS-060-01
2026-01-11T00:35:42+03:00|WS_COMPLETE|fall_out_bug|feature/lms-integration|ws=WS-060-01 loc=350 coverage=85%
2026-01-11T01:15:30+03:00|REVIEW_COMPLETE|fall_out_bug|feature/lms-integration|feature=F60 verdict=APPROVED
2026-01-11T01:20:00+03:00|DEPLOY_COMPLETE|fall_out_bug|main|feature=F60 env=production version=v1.5.0
```

## Query Examples

### Show all events for feature F60
```bash
grep "feature=F60" /tmp/consensus-audit.log
```

### Show failed WS
```bash
grep "WS_FAILED" /tmp/consensus-audit.log
```

### Show deployments today
```bash
grep "DEPLOY_COMPLETE" /tmp/consensus-audit.log | grep "$(date +%Y-%m-%d)"
```

### Count WS completed per user
```bash
grep "WS_COMPLETE" /tmp/consensus-audit.log | cut -d'|' -f3 | sort | uniq -c
```

### Show all hotfixes
```bash
grep "HOTFIX_" /tmp/consensus-audit.log
```

### Timeline for feature F60
```bash
grep "feature=F60" /tmp/consensus-audit.log | cut -d'|' -f1,2,5
```

### Breaking changes history
```bash
grep "BREAKING_CHANGE" /tmp/consensus-audit.log
```

## Rotation

Use logrotate for automatic log rotation:

```bash
# /etc/logrotate.d/consensus-audit
/var/log/consensus-audit.log {
    daily
    rotate 30
    compress
    missingok
    notifempty
    create 0644 user group
}
```

## Integration

### In slash commands

Add audit logging to all commands:

```bash
# At start of /design
bash sdp/notifications/audit-log.sh command_started "/design" "$FEATURE_ID"

# At end (success)
bash sdp/notifications/audit-log.sh command_completed "/design" "$FEATURE_ID" "success"

# At end (failure)
bash sdp/notifications/audit-log.sh command_completed "/design" "$FEATURE_ID" "failed"
```

### In hooks

Add audit logging to hooks:

```bash
# pre-build.sh
bash sdp/notifications/audit-log.sh ws_started "$WS_ID"

# post-build.sh (on success)
bash sdp/notifications/audit-log.sh ws_completed "$WS_ID" "$LOC" "$COVERAGE"

# post-build.sh (on failure)
bash sdp/notifications/audit-log.sh ws_failed "$WS_ID" "$ERROR"
```

## Monitoring

### Watch live
```bash
tail -f /tmp/consensus-audit.log
```

### Real-time dashboard (simple)
```bash
watch -n 5 'tail -20 /tmp/consensus-audit.log'
```

### Parse and display
```bash
#!/bin/bash
# Show recent activity
echo "=== Last 10 Events ==="
tail -10 /tmp/consensus-audit.log | while IFS='|' read timestamp event user branch data; do
    echo "$timestamp - $event ($user) - $data"
done
```

## Analytics

### Daily report
```bash
#!/bin/bash
# Generate daily report

TODAY=$(date +%Y-%m-%d)
LOG_FILE="/tmp/consensus-audit.log"

echo "=== Consensus Daily Report: $TODAY ==="
echo ""

echo "Commands executed:"
grep "$TODAY" "$LOG_FILE" | grep "COMMAND_START" | wc -l

echo "WS completed:"
grep "$TODAY" "$LOG_FILE" | grep "WS_COMPLETE" | wc -l

echo "Reviews:"
grep "$TODAY" "$LOG_FILE" | grep "REVIEW_COMPLETE" | wc -l

echo "Deployments:"
grep "$TODAY" "$LOG_FILE" | grep "DEPLOY_COMPLETE" | wc -l

echo "Hotfixes:"
grep "$TODAY" "$LOG_FILE" | grep "HOTFIX_DEPLOY" | wc -l

echo ""
echo "Failed WS:"
grep "$TODAY" "$LOG_FILE" | grep "WS_FAILED"

echo ""
echo "Breaking changes:"
grep "$TODAY" "$LOG_FILE" | grep "BREAKING_CHANGE"
```

## Security

- Audit log contains sensitive information (user, branches, etc.)
- Restrict read access: `chmod 640 /var/log/consensus-audit.log`
- Consider encrypting archived logs
- Regularly backup logs to secure storage
- Comply with data retention policies

## Troubleshooting

### Log file not created
```bash
# Check permissions
ls -la /tmp/consensus-audit.log

# Check directory exists
mkdir -p "$(dirname "$AUDIT_LOG_FILE")"
```

### Too large
```bash
# Check size
du -h /tmp/consensus-audit.log

# Archive old entries
gzip /tmp/consensus-audit.log
mv /tmp/consensus-audit.log.gz /archive/
```
