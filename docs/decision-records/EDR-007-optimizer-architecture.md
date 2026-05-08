# EDR-007
# Optimizer Architecture

Status: Accepted

Date: 2026-05-08

## Context

The FLD platform contains optimization systems that evaluate and evolve possible wildfire defense system configurations.

The optimizer is responsible for balancing competing engineering goals including hydraulics, runtime, survivability, cost, operational resilience, and deployment practicality.

## Decision

The optimization engine will exist as a dedicated architectural subsystem rather than as isolated calculation utilities.

Primary optimizer responsibilities include:

- candidate generation
- mutation systems
- scoring systems
- constraint evaluation
- convergence analysis
- recommendation generation
- evolutionary refinement

Optimizer systems should primarily live under:

engines/
services/
runtime/

## Reasoning

Optimization is one of the core differentiators of the FLD platform.

The system is not simply calculating hydraulics. It is exploring design possibilities and evaluating engineering tradeoffs across multiple dimensions simultaneously.

Separating optimizer architecture improves explainability, maintainability, testing, future AI integration, and future autonomous design capabilities.

## Consequences

Positive outcomes include cleaner optimizer evolution, easier subsystem testing, clearer engineering traceability, and future scalability.

Accepted tradeoffs include temporary duplication during migration away from legacy optimizer structures.

## Related Systems

- optimizer_engine.py
- optimizer_candidates.py
- optimizer_validation.py
- optimizer_ranking.py
- optimizer_memory.py
- weighted_score.py
- mutation systems
- convergence systems
