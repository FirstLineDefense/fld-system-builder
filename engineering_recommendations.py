def generate_engineering_recommendations(input_data, primary, design_maturity=None):
    recommendations = []

    summary = primary.get("summary", {})
    manifold = primary.get("manifold", {})
    branch_results = manifold.get("branch_results", [])
    operating_modes = manifold.get("operating_modes", {}).get("modes", [])
    warnings = summary.get("warnings", [])

    def add_recommendation(category, severity, title, detail):
        recommendations.append({
            "category": category,
            "severity": severity,
            "title": title,
            "detail": detail,
        })

    for branch in branch_results:
        if not branch.get("active"):
            continue

        branch_number = branch.get("branch_number", "Unknown")
        pressure_margin = branch.get("pressure_margin_psi", 0)
        velocity = branch.get("velocity_fps", 0)
        friction_loss = branch.get("friction_loss_psi", 0)
        pipe_name = branch.get("pipe_name", "Unknown pipe")

        if not branch.get("passed"):
            add_recommendation(
                "Hydraulics",
                "High",
                f"Branch {branch_number} is failing",
                "This branch does not meet the current pressure or hydraulic requirements. Increase pipe diameter, reduce run length, reduce device count, reduce elevation gain, or select a stronger pump."
            )

        if pressure_margin < 10:
            add_recommendation(
                "Hydraulics",
                "High",
                f"Branch {branch_number} has low pressure margin",
                f"Branch {branch_number} has only {round(pressure_margin, 1)} psi of pressure margin. For wildfire defense planning, consider increasing the pipe size, reducing fittings, reducing device count, or improving pump pressure."
            )

        if velocity > 8:
            add_recommendation(
                "Hydraulics",
                "Medium",
                f"Branch {branch_number} velocity is high",
                f"Branch {branch_number} is using {pipe_name} with a velocity of {round(velocity, 1)} fps. Consider increasing pipe diameter to reduce friction, noise, surge risk, and long-run stress."
            )

        if friction_loss > 15:
            add_recommendation(
                "Hydraulics",
                "Medium",
                f"Branch {branch_number} has high friction loss",
                f"Branch {branch_number} has approximately {round(friction_loss, 1)} psi of friction loss. Consider larger pipe, shorter routing, fewer fittings, or sweeping bends."
            )

    first_line_passed = False
    last_line_passed = False
    foam_passed = False

    for mode in operating_modes:
        mode_name = mode.get("mode_name", "")

        if "First Line" in mode_name and mode.get("passed"):
            first_line_passed = True

        if "Last Line" in mode_name and mode.get("passed"):
            last_line_passed = True

        if "Foam" in mode_name and mode.get("passed"):
            foam_passed = True

    if not first_line_passed:
        add_recommendation(
            "Operating Modes",
            "High",
            "First Line Defense Mode is not passing",
            "First Line mode should usually be the core FLD operating mode. Confirm that at least one active branch is assigned to first_line and that its hydraulic checks pass."
        )

    if not last_line_passed:
        add_recommendation(
            "Operating Modes",
            "Medium",
            "Last Line / Structure Defense Mode is not configured",
            "No passing Last Line mode was found. If this design is meant to protect structures directly, add one or more last_line branches for roofline, ember exposure, or structure defense coverage."
        )

    if not foam_passed:
        add_recommendation(
            "Operating Modes",
            "Low",
            "Foam Mode is not configured",
            "Foam Mode is not currently passing. If foam or gel deployment is part of this platform tier, add a dedicated foam branch or separate foam delivery path."
        )

    pump_utilization = manifold.get("pump_flow_utilization_fraction", None)

    if pump_utilization is not None:
        if pump_utilization < 0.3:
            add_recommendation(
                "Pump Selection",
                "Low",
                "Pump may be oversized for this test case",
                f"The pump is operating at approximately {round(pump_utilization * 100, 1)}% of max flow. This may be fine for expansion capacity, but for a final design confirm that oversizing is intentional."
            )

        if pump_utilization > 0.85:
            add_recommendation(
                "Pump Selection",
                "High",
                "Pump is near maximum flow capacity",
                f"The pump is operating at approximately {round(pump_utilization * 100, 1)}% of max flow. Consider a stronger pump, fewer simultaneous branches, or reduced device count."
            )

    for warning in warnings:
        warning_text = str(warning)

        if "budget" in warning_text.lower():
            add_recommendation(
                "Proposal Readiness",
                "Medium",
                "Budget issue detected",
                warning_text
            )

        if "No pump passed" in warning_text:
            add_recommendation(
                "Pump Selection",
                "High",
                "No pump fully passed all operating-mode requirements",
                "The system selected the best available pump, but at least one operating-mode requirement was not fully satisfied. Review pump capacity and mode requirements."
            )

    if design_maturity:
        grade = design_maturity.get("grade", "")

        if grade in ["Concept Grade", "Engineering Grade"]:
            add_recommendation(
                "Maturity",
                "Medium",
                "Design is not yet proposal-ready",
                f"The current maturity grade is {grade}. Resolve hard gates, operating-mode gaps, and critical warnings before treating this as client-facing."
            )

    if not recommendations:
        add_recommendation(
            "General",
            "Info",
            "No major engineering issues detected",
            "The current design does not trigger any major automated recommendations. Continue reviewing site-specific assumptions, installation constraints, and professional engineering requirements."
        )

    return recommendations