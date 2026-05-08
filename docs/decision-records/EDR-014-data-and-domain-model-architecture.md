# EDR-014
# Data And Domain Model Architecture

Status: Accepted

Date: 2026-05-08

## Context

The FLD platform depends on structured engineering data for components, pumps, pipes, engines, motors, batteries, water storage, fuel storage, controls, sensors, saved projects, and future proposal inputs.

As the platform grows, raw dictionaries, CSV files, one-off forms, and loosely structured objects become harder to maintain.

## Decision

The FLD platform will progressively separate domain models and data structures from UI, rendering, routing, and temporary calculation logic.

Domain and data systems should progressively organize around:

domain/
data/
repositories/
registries/
services/

## Reasoning

Clear domain modeling improves validation, testing, component reuse, future imports, proposal generation, and future engineering automation.

The platform needs stable representations of systems, components, projects, scenarios, constraints, and outputs.

## Consequences

Positive outcomes include cleaner data flow, improved validation, better future integrations, safer refactors, and easier engineer onboarding.

Accepted tradeoffs include staged migration from legacy dictionaries and CSV-backed structures into stronger domain models.

## Related Systems

- domain/
- data/
- repositories/
- registries/
- component library
- saved projects
- project report model
- system DTOs
