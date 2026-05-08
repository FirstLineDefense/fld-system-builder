# EDR-011
# Operating Mode Architecture

Status: Accepted

Date: 2026-05-08

## Context

The FLD platform evolved beyond static sprinkler layout calculations and began modeling operational wildfire defense behavior through distinct operating modes.

Operating modes allow the platform to reason about:

- water source strategy
- power source strategy
- runtime survivability
- automation capability
- operational resilience
- fallback systems
- deployment readiness
- off-grid survivability
- wildfire operational behavior

The operating mode system became one of the primary intelligence layers within the FLD platform.

## Decision

Operating mode logic will remain a dedicated architectural subsystem with progressively improved modular separation.

Operating mode systems should progressively organize around:

services/
runtime/
engines/
domain/

Operating mode systems must remain explainable, deterministic, and operationally traceable.

## Reasoning

Operating mode logic is central to the FLD platform because wildfire survivability depends not only on hydraulic capability, but also on operational continuity during grid failure, evacuation conditions, infrastructure disruption, and extended runtime scenarios.

The operating mode architecture allows the FLD platform to reason about real-world operational survivability rather than isolated engineering calculations.

## Consequences

Positive outcomes include clearer operational reasoning, improved future automation capability, easier runtime evaluation, and stronger deployment intelligence.

Accepted tradeoffs include temporary overlap between legacy operating mode logic and newer modularized runtime systems during migration.

## Related Systems

- operating_mode_logic.py
- runtime intelligence
- deployment survivability systems
- runtime calculations
- power systems
- water source systems
- fallback systems
