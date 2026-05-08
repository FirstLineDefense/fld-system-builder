# RELEASE CHECKLIST

## Goal

Safely promote tested engineering work from:

develop

to:

main

without destabilizing production.

---

# PRE-RELEASE CHECKLIST

Before merging develop into main:

- verify working tree clean
- verify latest develop pushed
- verify no partial refactors
- verify local application boots
- verify smoke tests pass
- verify Render-critical paths still function
- verify major routes load
- verify proposal/report generation works
- verify no broken imports
- verify no temporary debug code
- verify no accidental backup files included

---

# RELEASE PROCEDURE

## 1. Checkout Main

git checkout main

---

## 2. Pull Latest Main

git pull origin main

---

## 3. Merge Develop

git merge develop

---

## 4. Run Final Verification

Examples:

- local boot test
- route verification
- smoke tests
- report generation
- export generation

---

## 5. Push Main

git push origin main

Render production auto deploys from main.

---

## 6. Verify Production Deployment

Verify:
- Render deploy success
- live site loads
- core routes function
- reports function
- exports function

---

## 7. Create Stable Release Tag

Example:

git tag stable-release-name-v1

git push origin stable-release-name-v1

---

# ROLLBACK PROCEDURE

If deployment fails:

1. identify last stable tag
2. checkout stable tag
3. restore known-good state
4. redeploy production
5. diagnose develop separately

---

# IMPORTANT RULES

Never:
- push unstable code to main
- deploy directly from develop
- bypass verification
- remove rollback capability

Always:
- tag stable milestones
- maintain production stability
- preserve rollback recovery
- verify deployment health

---

# CORE PHILOSOPHY

Production stability is more important than deployment speed.

The public FLD deployment should remain operational even while architecture evolution continues separately inside develop.
