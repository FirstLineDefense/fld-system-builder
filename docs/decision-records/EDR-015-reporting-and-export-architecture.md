# EDR-015 Reporting And Export Architecture

## Status
Accepted

## Date
2026-05-08

## Context

The FLD System Builder platform generates large amounts of engineering, operational, and proposal data that must be transformed into usable reports for multiple audiences.

The platform requires:

- engineering cut sheets
- hydraulic summaries
- proposal documents
- operating mode reports
- optimization summaries
- bottleneck analysis
- runtime intelligence summaries
- deployment recommendations
- client-facing proposal exports
- internal engineering exports
- future insurance/compliance documentation

Historically, reporting logic became tightly coupled to Flask routes and UI rendering, creating instability and making future export systems difficult to scale.

The reporting architecture must now become a formal platform subsystem.

## Decision

The FLD platform will adopt a dedicated reporting and export architecture consisting of:

- report orchestration layer
- report renderer layer
- export generation layer
- report template layer
- report persistence layer
- future async export pipeline

Reports will become first-class platform objects rather than temporary Flask responses.

## Core Architectural Principles

### 1. Reports Are Platform Assets

Reports are not simple HTML pages.

Reports represent:

- engineering outputs
- operational outputs
- proposal outputs
- compliance outputs
- client deliverables

The reporting system becomes a permanent subsystem of the platform.

### 2. Separation Between Data And Presentation

Engineering calculations must remain fully separated from presentation formatting.

Hydraulic engines must never directly generate HTML.

Optimization systems must never directly generate export formatting.

The reporting layer consumes structured domain data and transforms it into presentation formats.

### 3. Multi-Format Export Support

The architecture must support:

- HTML
- PDF
- CSV
- JSON
- Excel
- future GIS/map exports
- future CAD/design exports

without requiring business logic duplication.

### 4. Reusable Report Sections

Large report sections must become reusable renderer modules.

Examples:

- readiness banners
- optimization summaries
- hydraulic summaries
- recommendation cards
- operating mode summaries
- pricing tables
- runtime intelligence sections

Renderer reuse reduces duplication and improves long-term maintainability.

### 5. Client And Internal Report Separation

The system must support multiple report visibility layers:

- engineering/internal
- installer/internal
- client-facing
- insurer/compliance
- deployment/operator

Not all audiences should see the same information.

## Architectural Layers

### Report Orchestration Layer

Responsible for:

- assembling report sections
- coordinating renderers
- selecting export formats
- validating report completeness

Example future location:

services/reporting/

### Renderer Layer

Responsible for:

- converting structured data into visual sections
- HTML fragments
- tables
- summary cards
- charts
- structured layouts

Example future location:

renderers/reports/

### Export Layer

Responsible for:

- PDF generation
- CSV export
- Excel export
- JSON export
- future packaged proposal generation

Example future location:

services/exports/

### Persistence Layer

Responsible for:

- saving generated reports
- browsing historical reports
- regenerating exports
- future audit history

Example future location:

repositories/reports/

## Future Planned Capabilities

### Proposal System Expansion

Future proposal exports may include:

- client pricing
- markup calculations
- labor estimates
- design-hour estimates
- maintenance plan pricing
- subscription pricing
- financing scenarios

### AI Assisted Reporting

Future AI systems may generate:

- engineering summaries
- proposal explanations
- deployment notes
- operational recommendations

AI generation must remain separated from engineering calculations.

### Map-Based Design Exports

Future reporting systems may generate:

- property layout exports
- sprinkler placement maps
- operational zone maps
- sensor placement diagrams

### Async Export Pipeline

Large reports may eventually require:

- background processing
- queued export jobs
- cloud rendering workers
- downloadable artifact pipelines

## Consequences

### Positive

- reporting subsystem becomes scalable
- export systems become modular
- easier future proposal generation
- cleaner renderer separation
- reusable report components
- easier testing
- future async processing possible

### Negative

- additional architecture complexity
- increased renderer management
- more subsystem coordination required

## Long-Term Direction

The reporting system is evolving into a full engineering deliverable platform capable of producing:

- internal engineering documentation
- client proposals
- operational deployment packages
- future insurance/compliance documentation
- future AI-assisted design deliverables

This architecture supports the transition of FLD Builder from a prototype calculator into a professional engineering and deployment platform.
