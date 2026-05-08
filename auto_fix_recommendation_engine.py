def recommend_auto_fixes(violations, primary):
    fixes = []

    pump = primary.get("pump", {}) or {}
    branches = primary.get("branches", []) or []

    pump_gpm = pump.get("gpm", 0) or 0

    total_branch_gpm = sum(
        branch.get("target_gpm", 0) or 0
        for branch in branches
    )

    for violation in violations:
        constraint = violation.get("constraint", "")
        severity = violation.get("severity", "medium")

        if constraint == "excessive_velocity":
            fixes.append({
                "priority": severity,
                "fix_type": "increase_pipe_size",
                "recommendation": "Increase the affected branch pipe to the next available diameter step.",
                "reason": "Higher pipe diameter lowers velocity and usually reduces friction loss."
            })

        elif constraint == "elevated_velocity":
            fixes.append({
                "priority": severity,
                "fix_type": "review_pipe_size",
                "recommendation": "Review whether this branch should move up one pipe size.",
                "reason": "Velocity is usable, but may be high for long runs, noise, or friction-sensitive branches."
            })

        elif constraint == "pump_capacity":
            recommended_gpm = round(
                total_branch_gpm * 1.15,
                1
            )

            fixes.append({
                "priority": severity,
                "fix_type": "increase_pump_capacity",
                "recommendation": f"Review a pump capacity around {recommended_gpm} GPM or higher.",
                "reason": "This gives branch demand a practical reserve instead of operating at the edge."
            })

        elif constraint == "pump_oversized":
            recommended_gpm = round(
                total_branch_gpm / 0.75,
                1
            ) if total_branch_gpm else pump_gpm

            fixes.append({
                "priority": severity,
                "fix_type": "reduce_pump_capacity_or_add_zones",
                "recommendation": f"Consider a smaller pump near {recommended_gpm} GPM, or add operating modes that use more available capacity.",
                "reason": "A heavily oversized pump may waste cost and create control problems."
            })

        elif constraint == "motor_power":
            recommended_hp = round(
                max(
                    3 * max(pump_gpm / 100, 1),
                    5
                ),
                1
            )

            fixes.append({
                "priority": severity,
                "fix_type": "review_motor_hp",
                "recommendation": f"Review motor sizing. A rough screening target is at least {recommended_hp} HP before pump-curve validation.",
                "reason": "Motor horsepower should be checked against pump curve, pressure, flow, and duty cycle."
            })

        elif constraint == "zero_branch_flow":
            fixes.append({
                "priority": severity,
                "fix_type": "add_branch_flow",
                "recommendation": "Add terminal devices, quantities, or explicit target GPM for this branch.",
                "reason": "The optimizer cannot evaluate a branch with no flow demand."
            })

        elif constraint == "missing_pipe_size":
            fixes.append({
                "priority": severity,
                "fix_type": "select_pipe_size",
                "recommendation": "Select a valid pipe size for the affected branch.",
                "reason": "Pipe diameter is required for velocity and friction-loss logic."
            })

        elif constraint == "branch_data":
            fixes.append({
                "priority": severity,
                "fix_type": "add_branch_data",
                "recommendation": "Add at least one active branch with pipe, elevation, and terminal device data.",
                "reason": "The system cannot make a meaningful hydraulic recommendation without branch data."
            })

    if not fixes:
        fixes.append({
            "priority": "low",
            "fix_type": "no_action_required",
            "recommendation": "No auto-fix recommendations were generated.",
            "reason": "No major constraint violations were detected."
        })

    return fixes


def build_auto_fix_recommendation_html(violations, primary):
    fixes = recommend_auto_fixes(
        violations,
        primary
    )

    if (
        len(fixes) == 1
        and fixes[0].get("fix_type") == "no_action_required"
    ):
        return """
        <div class="section section-green">
        <h2>Auto-Fix Recommendations</h2>
        <p>No auto-fix recommendations were generated.</p>
        </div>
        """

    html = """
    <div class="section section-yellow">
    <h2>Auto-Fix Recommendations</h2>
    <p>These are review recommendations only. The system has not automatically changed the design.</p>
    <table>
    <tr>
    <th>Priority</th>
    <th>Fix Type</th>
    <th>Recommendation</th>
    <th>Reason</th>
    </tr>
    """

    for fix in fixes:
        html += "<tr>"
        html += f"<td>{fix.get('priority')}</td>"
        html += f"<td>{fix.get('fix_type')}</td>"
        html += f"<td>{fix.get('recommendation')}</td>"
        html += f"<td>{fix.get('reason')}</td>"
        html += "</tr>"

    html += """
    </table>
    </div>
    """

    return html
