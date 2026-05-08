# SAFE DEPLOYMENT WORKFLOW

## Branch Strategy

### main
Purpose:
- stable production branch
- public deployment branch
- Render production deployment source

Rules:
- must remain deployable
- must remain stable
- only tested code merges into main
- production rollback tags created regularly

### develop
Purpose:
- active engineering branch
- architecture refactors
- unstable experimental work
- extraction/migration work

Rules:
- may temporarily break
- all active engineering happens here
- merged into main only after testing

---

## Production Deployment Rules

Production deploys occur ONLY from:

main

Render production service must remain connected to:

main

Never connect production Render deployment to:

develop

---

## Standard Engineering Workflow

### Daily Development

1. checkout develop
2. implement changes
3. local testing
4. commit frequently
5. push develop regularly

### Stable Release Workflow

1. verify develop stability
2. perform smoke tests
3. merge develop into main
4. push main
5. Render auto deploys production
6. create stable git tag

---

## Stable Release Tagging

Examples:

stable-phase1-foundation-complete-v1
stable-render-deploy-fix-v1
stable-resilience-edr-v1

Tags provide:
- rollback capability
- historical recovery
- architecture checkpoints
- deployment safety

---

## Rollback Procedure

If production breaks:

1. identify last stable tag
2. checkout stable tag
3. merge/redeploy stable state
4. restore production stability
5. diagnose develop branch separately

---

## Future Planned Expansion

Future deployment architecture may include:

- staging deployment environment
- preview deployment environments
- historical release snapshots
- automated smoke testing
- deployment verification pipelines
- release candidate workflows

---

## Core Philosophy

Production stability takes priority over rapid deployment.

The public FLD deployment should remain stable and usable even while active engineering work continues separately.
