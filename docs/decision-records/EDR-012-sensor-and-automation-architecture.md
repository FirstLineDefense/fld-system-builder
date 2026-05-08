# EDR-012
# Sensor And Automation Architecture

Status: Accepted

Date: 2026-05-08

## Context

The FLD platform is intended to evolve beyond manual design assistance into sensor-informed and eventually automated wildfire defense operation.

Future versions may include environmental sensors, property sensors, system health data, remote activation, threshold-based activation, and automated response logic.

## Decision

Sensor and automation logic will be treated as a future dedicated architecture layer rather than embedded directly into hydraulic, UI, or proposal systems.

Future sensor and automation systems should organize around:

services/
runtime/
domain/
engines/

## Reasoning

Sensor and automation behavior must remain explainable, testable, and operationally safe.

The platform should support future V2, V3, and V4 system evolution without forcing a redesign of the core hydraulic and proposal architecture.

## Consequences

Positive outcomes include cleaner future automation paths, safer system expansion, better sensor integration, and improved operational traceability.

Accepted tradeoffs include deferring full automation architecture until the core engineering and proposal systems are more stable.

## Related Systems

- V2 remote operation
- V3 sensor-informed operation
- V4 automation
- runtime intelligence
- operating mode logic
- future sensor mesh systems
- future activation logic
