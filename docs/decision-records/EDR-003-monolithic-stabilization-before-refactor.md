# EDR-003
# Monolithic Stabilization Before Full Refactor

## Status

Accepted

## Date

2026-05-08

## Context

The FLD System Builder accumulated substantial working intelligence before the architecture was cleanly modularized.

The legacy builder contained important functional behavior, including hydraulic calculations, branch logic, operating mode selection, recommendation systems, report generation, proposal flow, and optimization behavior.

Because much of this behavior emerged through rapid iteration, a full rewrite would risk losing working logic before it was fully understood and documented.

## Decision

The FLD platform will preserve and stabilize the working legacy builder before attempting deeper replacement or full subsystem rewrite.

The platform will use staged extraction instead of immediate rewrite.

## Reasoning

Preserving working behavior is more important than achieving architectural purity too early.

The existing system already contains valuable operational intelligence. Rewriting it prematurely could introduce regressions, remove evolved behavior, or disconnect proven workflows.

The safer path is to stabilize first, then extract logic into services, renderers, engines, repositories, and domain layers.

## Consequences

Positive outcomes:

- preserves working builder behavior
- reduces rewrite risk
- allows controlled refactor
- protects deployment continuity
- gives future engineers a safer migration path

Accepted tradeoffs:

- temporary hybrid architecture
- some legacy dependencies remain
- refactor takes longer
- documentation must explain why old and new structures coexist

## Future Considerations

Future work should progressively reduce legacy coupling while preserving tested behavior.

The long-term goal is not to keep the monolith permanently. The goal is to extract, test, document, and replace it safely.

## Related Systems

- legacy FLD Builder V2.7
- Flask bridge route
- report generation
- hydraulic calculations
- optimizer logic
- proposal workflow
- runtime intelligence

## Related Files

```text
flask_app.py
webapp/routes/legacy_builder_routes.py
services/
renderers/
engines/
domain/
