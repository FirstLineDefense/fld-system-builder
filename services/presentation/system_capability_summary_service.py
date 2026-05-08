def generate_system_capability_summary(
    project=None,
    hydraulic_summary=None,
    multi_scenario_proposals=None,
):
    project = project or {}
    hydraulic_summary = hydraulic_summary or {}
    multi_scenario_proposals = multi_scenario_proposals or {}

    flow_gpm = hydraulic_summary.get("total_gpm")
    pressure_psi = hydraulic_summary.get("system_pressure_psi")

    scenario_count = len(multi_scenario_proposals)

    lines = [
        "FLD SYSTEM CAPABILITY SUMMARY",
        "============================================================",
        "",
        "This section summarizes the intended operational capabilities of the proposed FLD wildfire resiliency system.",
        "",
        "The system is designed as layered wildfire infrastructure capable of supporting both property protection and future responder integration objectives.",
        "",
        "CORE CAPABILITIES",
        "------------------------------------------------------------",
        "",
        "- Layered wildfire sprinkler protection",
        "- Off-grid operational expansion path",
        "- Modular V2 / V3 / V4 upgrade architecture",
        "- Maintenance-oriented system layout",
        "- Future responder infrastructure integration",
        "- Multi-scenario deployment planning",
    ]

    if flow_gpm:
        lines.append(f"- Estimated system flow capacity: {flow_gpm} GPM")

    if pressure_psi:
        lines.append(f"- Estimated operating pressure: {pressure_psi} PSI")

    if scenario_count:
        lines.extend(
            [
                "",
                f"This report currently includes {scenario_count} deployment/proposal scenarios for comparative planning purposes.",
            ]
        )

    lines.extend(
        [
            "",
            "RESPONDER INTEGRATION DIRECTION",
            "------------------------------------------------------------",
            "",
            "Future responder-facing documentation may include:",
            "- 1.5 inch attack hose connection locations",
            "- Off-grid pump operating procedures",
            "- Water source information",
            "- Emergency responder access notes",
            "- Property protection zone maps",
            "- Fuel and power architecture summaries",
        ]
    )

    return "\n".join(lines)
