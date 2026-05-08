# EDR-009
# Hydraulic Modeling Foundation

Status: Accepted

Date: 2026-05-08

## Context

Hydraulic modeling is one of the core engineering foundations of the FLD platform.

The platform evaluates wildfire suppression system performance using calculations involving:

- pressure
- flow
- elevation
- friction loss
- runtime
- branch balancing
- sprinkler demand
- manifold behavior
- pipe sizing
- operational survivability

The hydraulic systems evolved through iterative engineering experimentation and real-world wildfire suppression design scenarios.

## Decision

Hydraulic calculations will remain a dedicated engineering subsystem with progressively improved modular separation and documentation.

Hydraulic systems should progressively organize around:

engines/
services/
domain/
hydraulics/

Hydraulic calculations should remain deterministic, explainable, and traceable.

## Reasoning

Hydraulic behavior directly determines whether a wildfire defense system is operationally viable.

The FLD platform is intended to function as a real engineering tool rather than a simplified estimation calculator.

Clear hydraulic architecture improves engineering trust, future validation, maintainability, and future professional deployment readiness.

## Consequences

Positive outcomes include improved engineering traceability, easier future validation, clearer subsystem boundaries, and safer future expansion.

Accepted tradeoffs include temporary coexistence between legacy hydraulic calculations and newer modular hydraulic systems during migration.

## Related Systems

- hydraulics.py
- friction loss calculations
- branch calculations
- manifold logic
- sprinkler demand logic
- runtime calculations
- optimization systems
