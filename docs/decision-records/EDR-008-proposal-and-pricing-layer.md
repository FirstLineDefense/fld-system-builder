# EDR-008
# Proposal And Pricing Layer

Status: Accepted

Date: 2026-05-08

## Context

The FLD platform evolved beyond hydraulic engineering calculations and began incorporating proposal generation, BOM generation, pricing logic, deployment estimation, and future commercial workflows.

The system is intended to eventually support both internal engineering workflows and external client-facing proposal generation.

## Decision

The FLD platform will maintain a dedicated commercial and proposal architecture layer responsible for:

- BOM generation
- cut-sheet generation
- pricing logic
- markup systems
- proposal generation
- maintenance plan pricing
- deployment cost estimation
- future subscription/service pricing
- future automated proposal workflows

Commercial systems should progressively move into:

services/
commercial/
renderers/

## Reasoning

Proposal generation is a core operational requirement of the FLD platform.

The system is intended to function not only as an engineering tool, but eventually as a deployable business operations platform capable of generating real-world project proposals and operational deployment outputs.

Separating proposal and pricing architecture improves maintainability, future accounting integration, operational scalability, and future automation readiness.

## Consequences

Positive outcomes include cleaner pricing logic separation, easier proposal generation workflows, improved future scalability, and cleaner integration with operational deployment systems.

Accepted tradeoffs include temporary duplication between legacy reporting systems and future modular proposal systems during migration.

## Related Systems

- cost.py
- export_utils.py
- proposal generation
- report generation
- BOM generation
- maintenance plan systems
- pricing logic
