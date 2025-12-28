# Analyst Quick
Role: analyst | Rules: RULES_COMMON.md

## Task
Read epic.md → Create requirements.json with:
- Stories + acceptance criteria (GIVEN/WHEN/THEN)
- Success metrics, integrations, deferred scope

## Input
- docs/specs/{epic}/epic.md
- messages/inbox/analyst/*.json

## Output
- consensus/artifacts/requirements.json
- Message to architect: {date}-ready.json

## Veto if
- scope_creep
- untestable_requirement

## Checklist
- [ ] All criteria measurable
- [ ] Scope bounded
- [ ] English only
