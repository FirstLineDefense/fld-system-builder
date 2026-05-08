# EDR-005
Renderer Layer Separation

Status

Accepted

Date

2026-05-08

Context

The FLD platform originally mixed rendering logic directly into routing and engineering logic.

As the platform expanded, UI rendering became increasingly difficult to maintain and reuse.

Decision

The platform will progressively separate rendering responsibilities into dedicated renderer modules located under:

renderers/

Renderer modules are responsible only for presentation generation and formatting behavior.

Reasoning

Separating renderers improves maintainability, UI clarity, reuse capability, subsystem isolation, testing, and future frontend flexibility.

Engineering calculations and business logic should not live inside rendering systems.

Consequences

Positive outcomes include cleaner architecture boundaries, easier UI maintenance, safer subsystem extraction, and future frontend flexibility.

Accepted tradeoffs include temporary duplication during extraction and transitional hybrid rendering structure.

Related Systems
renderers/
webapp/
services/
report generation
proposal rendering
