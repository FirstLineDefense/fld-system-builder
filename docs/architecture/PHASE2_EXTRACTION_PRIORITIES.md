# PHASE 2 EXTRACTION PRIORITIES

## Goal

Continue controlled migration away from remaining legacy monolith structures without destabilizing production.

The goal is NOT a rewrite.

The goal is controlled extraction, isolation, and consolidation.

---

# CURRENT ARCHITECTURE STATE

## New Architecture Areas

Already partially stabilized:

- services/
- renderers/
- registries/
- runtime/
- repositories/
- webapp/routes/
- tests/
- orchestration systems

---

## Remaining Legacy Core

Primary remaining legacy areas:

- app.py
- main.py
- branches.py
- hydraulic_optimizer.py
- hydraulic_intelligence.py
- builder_intelligence.py
- component_library.py
- weighted_score.py

---

# EXTRACTION PRIORITIES

## Priority 1 — app.py Decomposition

Remaining large functions:

- build_results_html
- build_branch_box
- build_system_builder_page
- build_page
- build_hydraulic_intelligence_html
- build_hydraulic_optimizer_html

Goal:
- move rendering into renderer layer
- reduce orchestration complexity
- reduce coupling

---

## Priority 2 — main.py Isolation

Current risk:
- orchestration concentration
- hidden business logic
- execution coupling

Goal:
- move orchestration into services/
- isolate runtime flow
- simplify execution pathways

---

## Priority 3 — Hydraulic Engine Separation

Current risk:
- engineering logic coupling
- optimizer coupling
- execution overlap

Files:
- hydraulic_optimizer.py
- hydraulic_intelligence.py
- hydraulics.py
- branches.py

Goal:
- deterministic engine isolation
- cleaner engineering authority boundaries
- testability improvements

---

## Priority 4 — Registry Consolidation

Current risk:
- component duplication
- fragmented configuration logic

Files:
- component_library.py
- registries/

Goal:
- centralized registry systems
- standardized component access
- future upload/import support

---

## Priority 5 — Optimizer Governance Cleanup

Current risk:
- scattered optimization logic
- legacy recommendation coupling

Files:
- weighted_score.py
- optimizer systems
- recommendation systems

Goal:
- centralized optimizer governance
- explainability improvements
- safer recommendation architecture

---

# IMPORTANT RULES

Never:
- perform giant rewrites
- migrate too many systems simultaneously
- destabilize production unnecessarily
- bypass rollback checkpoints

Always:
- extract incrementally
- commit frequently
- preserve stable tags
- verify local functionality
- isolate systems gradually

---

# CORE PHILOSOPHY

Phase 2 is controlled architectural consolidation.

The platform already possesses strong foundational architecture.

The remaining work is primarily:
- extraction
- isolation
- cleanup
- consolidation
- stabilization
