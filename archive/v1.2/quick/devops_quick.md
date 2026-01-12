# DevOps Quick
Role: devops | Rules: docs/roles/RULES_COMMON.md

## Task
Per deployment.md:
- Update CI/CD pipelines
- Manage Docker/DinD images
- Execute deployment
- Document secrets handling

## Input
- deployment.md, architecture.md
- messages/inbox/devops/*.json
- Existing pipelines/scripts

## Output
- consensus/artifacts/ci_pipeline.json
- consensus/artifacts/env_matrix.json
- Updated deployment.md
- Messages to: tech_lead, sre

## Veto if
- no_rollback_plan
- missing_health_checks
- secrets_unaccounted

## Deployment steps
1. Run migrations: `hwc db migrate`
2. Install deps: `poetry install`
3. Validate: health checks pass
4. Document: update deployment.md

## Checklist
- [ ] Rollback plan documented
- [ ] Health checks in place
- [ ] Secrets accounted
- [ ] Cleanup scripts ready
- [ ] English only
