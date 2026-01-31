#!/bin/bash
# sdp/notifications/audit-log.sh
# Centralized audit log for all workflow events

set -e

# Configuration
AUDIT_LOG_FILE="${AUDIT_LOG_FILE:-/tmp/consensus-audit.log}"
LOG_TO_FILE="${LOG_TO_FILE:-true}"
LOG_TO_STDOUT="${LOG_TO_STDOUT:-false}"

# Ensure log directory exists
mkdir -p "$(dirname "$AUDIT_LOG_FILE")"

# Log event
log_event() {
    local timestamp="$(date -Iseconds)"
    local event_type="$1"
    shift
    local event_data="$@"
    
    # Format: ISO8601|EVENT_TYPE|USER|GIT_BRANCH|EVENT_DATA
    local log_entry="${timestamp}|${event_type}|${USER:-unknown}|$(git branch --show-current 2>/dev/null || echo 'no-git')|${event_data}"
    
    if [[ "$LOG_TO_FILE" == "true" ]]; then
        echo "$log_entry" >> "$AUDIT_LOG_FILE"
    fi
    
    if [[ "$LOG_TO_STDOUT" == "true" ]]; then
        echo "[AUDIT] $log_entry"
    fi
}

# Main function
main() {
    local event_type="$1"
    shift
    
    case "$event_type" in
        "command_started")
            # Usage: audit-log.sh command_started "/design" "F60"
            local command="$1"
            local args="$2"
            log_event "COMMAND_START" "command=$command args='$args'"
            ;;
        
        "command_completed")
            # Usage: audit-log.sh command_completed "/design" "F60" "success"
            local command="$1"
            local args="$2"
            local status="$3"
            log_event "COMMAND_COMPLETE" "command=$command args='$args' status=$status"
            ;;
        
        "ws_started")
            # Usage: audit-log.sh ws_started "WS-060-01"
            local ws_id="$1"
            log_event "WS_START" "ws=$ws_id"
            ;;
        
        "ws_completed")
            # Usage: audit-log.sh ws_completed "WS-060-01" "350" "85"
            local ws_id="$1"
            local loc="${2:-unknown}"
            local coverage="${3:-unknown}"
            log_event "WS_COMPLETE" "ws=$ws_id loc=$loc coverage=$coverage%"
            ;;
        
        "ws_failed")
            # Usage: audit-log.sh ws_failed "WS-060-01" "tests failed"
            local ws_id="$1"
            local reason="$2"
            log_event "WS_FAILED" "ws=$ws_id reason='$reason'"
            ;;
        
        "review_started")
            # Usage: audit-log.sh review_started "F60"
            local feature_id="$1"
            log_event "REVIEW_START" "feature=$feature_id"
            ;;
        
        "review_completed")
            # Usage: audit-log.sh review_completed "F60" "APPROVED"
            local feature_id="$1"
            local verdict="$2"
            log_event "REVIEW_COMPLETE" "feature=$feature_id verdict=$verdict"
            ;;
        
        "deploy_started")
            # Usage: audit-log.sh deploy_started "F60" "staging"
            local feature_id="$1"
            local environment="$2"
            log_event "DEPLOY_START" "feature=$feature_id env=$environment"
            ;;
        
        "deploy_completed")
            # Usage: audit-log.sh deploy_completed "F60" "production" "v1.5.0"
            local feature_id="$1"
            local environment="$2"
            local version="$3"
            log_event "DEPLOY_COMPLETE" "feature=$feature_id env=$environment version=$version"
            ;;
        
        "hotfix_started")
            # Usage: audit-log.sh hotfix_started "001" "api-500"
            local issue_id="$1"
            local slug="$2"
            log_event "HOTFIX_START" "issue=$issue_id slug=$slug"
            ;;
        
        "hotfix_deployed")
            # Usage: audit-log.sh hotfix_deployed "001" "30m"
            local issue_id="$1"
            local duration="$2"
            log_event "HOTFIX_DEPLOY" "issue=$issue_id duration=$duration"
            ;;
        
        "git_push")
            # Usage: audit-log.sh git_push "main" "abc123d"
            local branch="$1"
            local commit="$2"
            log_event "GIT_PUSH" "branch=$branch commit=$commit"
            ;;
        
        "git_merge")
            # Usage: audit-log.sh git_merge "feature/lms" "main"
            local from_branch="$1"
            local to_branch="$2"
            log_event "GIT_MERGE" "from=$from_branch to=$to_branch"
            ;;
        
        "breaking_change")
            # Usage: audit-log.sh breaking_change "API" "3"
            local category="$1"
            local count="$2"
            log_event "BREAKING_CHANGE" "category=$category count=$count"
            ;;
        
        "approval_gate")
            # Usage: audit-log.sh approval_gate "PR" "123" "approved"
            local gate_type="$1"
            local gate_id="$2"
            local decision="$3"
            log_event "APPROVAL_GATE" "type=$gate_type id=$gate_id decision=$decision"
            ;;
        
        *)
            echo "Unknown audit event: $event_type"
            exit 1
            ;;
    esac
}

# Run
main "$@"
