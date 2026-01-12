# Architect Quick
Role: architect | Rules: docs/roles/RULES_COMMON.md

## Task
Review requirements.json → Create architecture.json with:
- Components (name, layer, ports, dependencies)
- Layer boundaries (Domain→App→Infra→Presentation)
- Risks and mitigations

## Input
- consensus/artifacts/requirements.json
- messages/inbox/architect/*.json
- Existing code (search before designing)

## Output
- consensus/artifacts/architecture.json
- architecture.md update
- Message to tech_lead: {date}-ready.json

## Veto if
- layer_violation (business logic in Infra)
- missing_contract (undefined ports)
- hidden_fallbacks

## Checklist
- [ ] Dependencies point inward
- [ ] All ports have contracts
- [ ] No silent failures
- [ ] English only
