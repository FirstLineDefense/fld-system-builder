# EDR-006
# Runtime Intelligence Architecture

Status: Accepted

Date: 2026-05-08

## Context

The FLD platform includes runtime intelligence systems that evaluate system behavior beyond static component selection.

Runtime intelligence is used to reason about system operation, endurance, constraints, operating modes, design readiness, and real-world usability.

## Decision

Runtime intelligence will be treated as a distinct architecture layer rather than being buried inside UI, routing, or one-off calculation functions.

Runtime logic should live primarily in:

runtime/
services/
engines/

## Reasoning

Runtime intelligence is central to the FLD platform because the tool is not only selecting parts. It is evaluating whether a proposed wildfire defense system can operate effectively under real-world constraints.

Separating runtime intelligence improves maintainability, testing, explainability, and future automation readiness.

## Consequences

Positive outcomes include clearer runtime reasoning, better future testing, easier automation expansion, and stronger operational explainability.

Accepted tradeoffs include temporary overlap between legacy runtime logic and newer runtime services during migration.

## Related Systems

- runtime/
- services/runtime_retention_service.py
- runtime/runtime_intelligence_manager.py
- operating_mode_logic.py
- design_readiness.py
- design_maturity.py
