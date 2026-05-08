# STAGING DEPLOYMENT STRATEGY

## Goal

Provide a safe public testing environment for FLD engineering work without risking production stability.

Production remains stable while active engineering continues separately.

---

# ENVIRONMENT STRATEGY

## Production Environment

Purpose:
- stable public release
- client-safe deployment
- operational system
- rollback-protected deployment

Branch:
main

Rules:
- stable only
- tested releases only
- rollback tags required

---

## Staging Environment

Purpose:
- active engineering preview
- architecture refactor testing
- feature validation
- integration testing
- workflow comparison
- pre-production validation

Branch:
develop

Rules:
- may temporarily break
- experimental changes allowed
- architecture migration allowed
- unstable features permitted

---

# FUTURE DEPLOYMENT STRUCTURE

## Production

Example:

fld-system-builder.onrender.com

Connected branch:

main

---

## Staging

Possible example:

fld-system-builder-dev.onrender.com

Connected branch:

develop

---

# BENEFITS

Staging deployment allows:

- safe architecture refactors
- UI comparison
- feature validation
- workflow testing
- optimizer comparison
- historical behavior comparison
- safe experimentation
- pre-release verification

---

# VERSION COMPARISON STRATEGY

Future stable releases may optionally preserve:

- historical screenshots
- release notes
- deployment snapshots
- tagged milestone builds
- milestone environments

This allows comparison between:

- legacy workflows
- optimizer behavior
- UI changes
- reporting changes
- engineering recommendations

---

# FUTURE EXPANSION

Future deployment architecture may include:

- release candidate environments
- automated smoke testing
- deployment verification pipelines
- temporary preview deployments
- automated rollback systems
- infrastructure snapshots

---

# CORE PHILOSOPHY

Production should remain stable and trustworthy.

Staging exists to safely evolve the platform without risking public stability.
