# EDR-018 Runtime And State Management Architecture

## Status
Accepted

## Date
2026-05-08

## Context

The FLD platform performs complex engineering calculations involving:

- hydraulic analysis
- optimization systems
- runtime intelligence
- recommendation systems
- proposal generation
- operating mode evaluation
- bottleneck analysis
- scenario comparison
- future AI-assisted workflows

Historically, runtime state evolved organically through Flask request flows, temporary dictionaries, global variables, and transient engineering objects.

As the platform scales, runtime state management must become structured and predictable.

## Decision

The FLD platform will adopt a dedicated runtime and state management architecture.

Runtime systems will progressively separate:

- transient execution state
- persistent project state
- calculated engineering outputs
- optimization state
- UI/session state
- export state

## Core Principles

### 1. Runtime State Is Not Persistent State

Temporary calculations must remain independent from saved project definitions.

Examples of runtime state include:

- active calculations
- optimization iterations
- transient warnings
- temporary recommendations
- engineering scratch values
- intermediate analysis

Persistent projects capture validated engineering configurations rather than temporary execution data.

### 2. Calculation Isolation

Engineering engines should execute in isolated calculation contexts.

This reduces:

- side effects
- accidental mutation
- cross-system contamination
- inconsistent outputs

### 3. Predictable Data Flow

The platform should progressively move toward predictable engineering execution flow:

input state

↓

validation

↓

calculation engines

↓

optimization systems

↓

recommendation systems

↓

report generation

↓

export systems

This improves debugging and future scalability.

### 4. Separation From UI Session State

Flask sessions and browser state must not become the authoritative engineering source of truth.

UI state should remain lightweight and replaceable.

The engineering platform must remain functional independently from browser/session implementation details.

### 5. Future Async Execution Support

The architecture should eventually support:

- background calculations
- queued optimization jobs
- report rendering workers
- async export systems
- future AI execution pipelines

## Architectural Direction

### Runtime Engine Layer

Responsible for:

- calculation orchestration
- execution pipelines
- transient engineering state
- engine coordination

### State Management Layer

Responsible for:

- runtime tracking
- state transitions
- execution isolation
- temporary result handling

### Persistence Layer

Responsible for:

- durable storage
- saved projects
- report history
- scenario persistence

### UI Session Layer

Responsible for:

- browser interactions
- temporary form state
- navigation state
- lightweight session handling

## Future Planned Capabilities

### Distributed Execution

Future systems may support:

- distributed optimization
- cloud processing
- multi-worker execution
- large-scale engineering calculations

### AI Execution Pipelines

Future AI systems may participate in:

- recommendation generation
- optimization assistance
- engineering analysis
- proposal explanation

AI systems must remain isolated from authoritative engineering calculations.

### Runtime Telemetry

Future runtime systems may track:

- execution timing
- optimization performance
- bottleneck detection
- engine health
- calculation tracing

## Consequences

### Positive

- cleaner runtime architecture
- improved debugging
- reduced side effects
- easier scaling
- future async support
- safer optimization execution
- cleaner engineering pipelines

### Negative

- increased architectural complexity
- additional state coordination
- migration overhead from legacy execution flow

## Long-Term Direction

The FLD runtime architecture is evolving toward a scalable engineering execution platform capable of supporting:

- advanced optimization
- distributed calculations
- AI-assisted workflows
- future deployment intelligence
- large-scale report generation
- operational analytics
- future cloud engineering systems

This architecture supports long-term transition away from tightly coupled request-driven engineering execution.
