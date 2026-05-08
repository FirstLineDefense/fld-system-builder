# EDR-004
# Service Layer Refactor Strategy

## Status

Accepted

## Date

2026-05-08

## Context

As the FLD platform expanded, business logic, rendering logic, routing behavior, optimization systems, and runtime intelligence became increasingly intertwined.

This created growing architectural risk and reduced maintainability.

## Decision

The FLD platform will progressively extract business logic into dedicated service-layer modules located under:

```text
services/
The service layer becomes responsible for:

- business logic
- orchestration logic
- engineering workflows
- proposal generation logic
- optimization coordination
- runtime coordination
- reusable processing pipelines

## Reasoning

Separating logic into services improves:

- maintainability
- testing capability
- subsystem isolation
- future scalability
- deployment stability
- onboarding clarity

The refactor will occur incrementally while preserving operational continuity.

## Consequences

### Positive Outcomes

- improved modularity
- improved maintainability
- cleaner separation of concerns
- easier future subsystem replacement

### Accepted Tradeoffs

- temporary hybrid architecture
- staged migration complexity
- partial duplication during extraction

## Related Systems

- services/
- renderers/
- webapp/
- optimizer systems
- runtime systems
