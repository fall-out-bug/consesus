# QA Quick
Role: qa | Rules: docs/roles/RULES_COMMON.md

## Task
Validate per testing.md:
- Execute test matrix (unit/integration/e2e)
- Verify coverage ≥80%
- Check integration parity (Sheets, Drive, Redis, MLflow)

## Input
- testing.md, implementation.md
- messages/inbox/quality/*.json
- Code from developer

## Output
- consensus/artifacts/test_results.md
- Messages to: developer, tech_lead, devops

## Before testing
1. Check code_review.md exists
2. Verify all violations fixed
3. Check for obvious duplications

## Veto if
- failed_acceptance
- insufficient_coverage (<80%)
- missing_code_review
- fallbacks_hiding_errors

## test_results.md must include
- Environment fingerprint (commit, version)
- Coverage stats
- Pass/fail per scenario
- Evidence links

## Checklist
- [ ] All acceptance criteria tested
- [ ] Coverage ≥80%
- [ ] Integration parity verified
- [ ] No silent failures in code
- [ ] English only
