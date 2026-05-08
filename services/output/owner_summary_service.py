def generate_owner_summary(
    project,
    hydraulic_summary=None,
    cost_summary=None,
    warnings=None,
):
    hydraulic_summary = hydraulic_summary or {}
    cost_summary = cost_summary or {}
    warnings = warnings or []

    primary = project.get("primary", {}) or {}

    pump = primary.get("pump", {}) or {}
    motor = primary.get("motor", {}) or {}

    branches = primary.get("branches", []) or []

    lines = []

    lines.append("FLD OWNER SUMMARY")
    lines.append("=" * 60)

    lines.append("")

    lines.append(
        f"Pump Recommendation: "
        f"{pump.get('name') or pump.get('model') or 'Not selected'}"
    )

    lines.append(
        f"Motor Recommendation: "
        f"{motor.get('name') or motor.get('model') or 'Not selected'}"
    )

    lines.append(f"Protected Zones: {len(branches)}")

    lines.append("")

    lines.append("SYSTEM PERFORMANCE")

    for key, value in hydraulic_summary.items():
        lines.append(f"- {key}: {value}")

    lines.append("")

    total_cost = float(cost_summary.get("total_cost", 0) or 0)

    lines.append(
        f"Estimated Material Cost: "
        f"${total_cost:.2f}"
    )

    lines.append("")

    if warnings:
        lines.append("IMPORTANT WARNINGS")

        for warning in warnings:
            lines.append(f"- {warning}")

    else:
        lines.append("No active warnings.")

    lines.append("")
    lines.append("End of owner summary")

    return "\n".join(lines)
