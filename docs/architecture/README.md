# FLD System Builder Architecture Documentation

This folder contains the high-level architecture documentation for the FLD System Builder platform.

The purpose of this documentation is to explain:

- what the platform does
- how the major software layers are organized
- why the architecture was structured this way
- how future engineers should understand, maintain, extend, or rebuild the system

The FLD System Builder is evolving from a prototype into a modular engineering platform that supports hydraulic modeling, system optimization, proposal generation, runtime intelligence, and future wildfire automation logic.

## Core Documentation Areas

- `architecture/` documents the overall platform structure.
- `decision-records/` documents major engineering decisions.
- `hydraulics/` documents hydraulic modeling and design assumptions.
- `deployment/` documents GitHub, Render, Flask, Gunicorn, and WSGI deployment.
- `commercial/` documents BOM, cut-sheet, cost, markup, and proposal logic.
- `operations/` documents operational wildfire system behavior and future V2/V3/V4 logic.
- `roadmap/` documents future platform direction.

## Current Architecture Direction

The platform is moving toward a modular structure:

```text
config/
domain/
engines/
repositories/
renderers/
services/
runtime/
webapp/
docs/
