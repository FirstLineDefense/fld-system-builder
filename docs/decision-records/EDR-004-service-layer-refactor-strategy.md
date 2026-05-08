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
