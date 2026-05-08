# EDR-017 Project And Scenario Management Architecture

## Status
Accepted

## Date
2026-05-08

## Context

The FLD platform is evolving beyond a single-run engineering calculator into a persistent engineering and deployment platform.

Users must be able to create, save, compare, duplicate, modify, and analyze complete engineering projects over time.

The system must support:

- saved projects
- scenario comparisons
- alternative configurations
- optimization snapshots
- proposal variants
- deployment strategies
- operating mode comparisons
- future AI-assisted revisions
- future collaborative engineering workflows

Historically, project state existed primarily inside temporary Flask sessions and transient runtime objects.

This approach is insufficient for long-term engineering workflows.

## Decision

The FLD platform will adopt a dedicated project and scenario management architecture.

Projects and scenarios will become persistent platform-level engineering assets.

## Core Principles

### 1. Projects Become Persistent Engineering Objects

Projects are not temporary UI sessions.

Projects represent:

- engineering designs
- deployment strategies
- optimization states
- proposal configurations
- operational planning
- future maintenance histories

Projects must persist independently from the UI layer.

### 2. Scenario-Based Engineering

The platform must support multiple scenarios within a single project.

Examples include:

- different pump selections
- alternate fuel systems
- battery variations
- redundancy strategies
- operating mode comparisons
- budget tiers
- deployment phases

Scenarios allow engineering comparison without duplicating entire projects.

### 3. Separation Between Runtime State And Saved State

Temporary runtime calculations must remain separated from saved project data.

The runtime engine may generate:

- calculations
- warnings
- optimization recommendations
- transient analysis

Persistent project storage captures stable engineering definitions and selected configurations.

### 4. Version-Aware Engineering

Projects should eventually support:

- revision history
- scenario snapshots
- rollback capability
- export history
- deployment revisions
- proposal revisions

This supports long-term engineering evolution.

### 5. Future Multi-User Expansion

The architecture should eventually support:

- installer accounts
- engineering teams
- collaborative review
- permission layers
- organization-level projects

## Architectural Direction

### Project Layer

Responsible for:

- project identity
- metadata
- ownership
- persistence
- lifecycle management

### Scenario Layer

Responsible for:

- engineering variations
- optimization comparisons
- alternate configurations
- deployment alternatives

### Repository Layer

Responsible for:

- saving projects
- loading projects
- version retrieval
- future database integration

### Service Layer

Responsible for:

- project orchestration
- validation
- migration handling
- scenario comparison logic

## Future Planned Capabilities

### Intelligent Scenario Comparison

Future systems may compare:

- runtime efficiency
- deployment cost
- fuel consumption
- resiliency
- redundancy quality
- maintenance complexity

### AI Assisted Revision Workflows

Future AI systems may assist with:

- identifying better configurations
- explaining engineering tradeoffs
- suggesting optimization paths
- detecting engineering conflicts

AI systems remain advisory and do not replace engineering validation.

### Deployment Lifecycle Tracking

Projects may eventually track:

- installation progress
- maintenance schedules
- inspections
- upgrades
- runtime telemetry
- future sensor integrations

## Consequences

### Positive

- stable engineering workflows
- persistent projects
- cleaner architecture
- easier proposal generation
- future collaboration support
- easier deployment tracking
- scalable engineering structure

### Negative

- increased persistence complexity
- migration overhead
- future database requirements

## Long-Term Direction

The FLD platform is evolving toward a complete engineering lifecycle system capable of managing:

- engineering projects
- deployment planning
- optimization workflows
- operational intelligence
- proposal systems
- maintenance systems
- future AI-assisted engineering workflows

This architecture supports long-term scalability beyond temporary calculator-style engineering tools.
