# BRANCH QUICK REFERENCE

## main

Purpose:
- stable production
- public deployment
- Render production branch

Rules:
- stable only
- tested only
- deploy-safe only

Production URL:
https://fld-system-builder.onrender.com

---

## develop

Purpose:
- active engineering
- architecture refactors
- feature development
- experimentation

Rules:
- may temporarily break
- not public-safe
- not deployment-safe

---

# STANDARD WORKFLOW

## Start Work

git checkout develop

---

## Commit Work

git add .

git commit -m "description"

git push origin develop

---

## Stable Release

git checkout main

git pull origin main

git merge develop

git push origin main

---

## Stable Release Tag

git tag stable-release-name-v1

git push origin stable-release-name-v1

---

# IMPORTANT RULES

Never:
- develop directly on main
- push unstable code to main
- deploy experimental work to production

Always:
- work inside develop
- verify before merge
- preserve rollback capability
- create stable tags
