def detect_constraint_violations(primary):
    violations = []

    pump = primary.get("pump", {}) or {}
    motor = primary.get("motor", {}) or {}
    branches = primary.get("branches", []) or []

    pump_gpm = pump.get("gpm", 0) or 0
    motor_hp = motor.get("hp", 0) or 0

    total_branch_gpm = sum(
        branch.get("target_gpm", 0) or 0
        for branch in branches
    )

    if not branches:
        violations.append({
            "constraint": "branch_data",
            "severity": "high",
            "message": "No branch data is available for optimization.",
            "suggested_fix": "Add at least one active branch with flow and pipe data."
        })

    if pump_gpm and total_branch_gpm:
        ratio = total_branch_gpm / pump_gpm

        if ratio > 1.15:
            violations.append({
                "constraint": "pump_capacity",
                "severity": "high",
                "message": f"Pump appears undersized. Branch demand is {round(ratio * 100, 1)}% of pump capacity.",
                "suggested_fix": "Increase pump capacity or reduce simultaneous branch demand."
            })

        elif ratio < 0.45:
            violations.append({
                "constraint": "pump_oversized",
                "severity": "medium",
                "message": f"Pump appears heavily oversized. Branch demand is only {round(ratio * 100, 1)}% of pump capacity.",
                "suggested_fix": "Consider a smaller pump or add operating modes that use the available capacity."
            })

    if motor_hp and pump_gpm:
        hp_per_100_gpm = motor_hp / max(pump_gpm / 100, 1)

        if hp_per_100_gpm < 3:
            violations.append({
                "constraint": "motor_power",
                "severity": "medium",
                "message": f"Motor horsepower may be low for pump flow. Current ratio is {round(hp_per_100_gpm, 2)} HP per 100 GPM.",
                "suggested_fix": "Review motor horsepower against pump curve, pressure requirement, and duty cycle."
            })

    for branch in branches:
        branch_number = branch.get("branch_number", "unknown")
        velocity = branch.get("velocity_fps", 0) or 0
        pipe_diameter = branch.get("pipe_diameter_in", 0) or 0
        target_gpm = branch.get("target_gpm", 0) or 0

        if target_gpm <= 0:
            violations.append({
                "constraint": "zero_branch_flow",
                "severity": "high",
                "message": f"Branch {branch_number} has no target flow.",
                "suggested_fix": "Add device flow, device quantity, or explicit target GPM."
            })

        if velocity > 10:
            violations.append({
                "constraint": "excessive_velocity",
                "severity": "high",
                "message": f"Branch {branch_number} velocity is {velocity} ft/s, which is above the preferred range.",
                "suggested_fix": "Increase pipe diameter or reduce flow on this branch."
            })

        elif velocity > 7:
            violations.append({
                "constraint": "elevated_velocity",
                "severity": "medium",
                "message": f"Branch {branch_number} velocity is {velocity} ft/s, which should be reviewed.",
                "suggested_fix": "Consider increasing pipe diameter if friction loss or noise is a concern."
            })

        if pipe_diameter <= 0:
            violations.append({
                "constraint": "missing_pipe_size",
                "severity": "high",
                "message": f"Branch {branch_number} has no valid pipe diameter.",
                "suggested_fix": "Select a valid pipe size for this branch."
            })

    return violations


def summarize_constraint_violations(primary):
    violations = detect_constraint_violations(primary)

    high_count = sum(
        1 for item in violations
        if item.get("severity") == "high"
    )

    medium_count = sum(
        1 for item in violations
        if item.get("severity") == "medium"
    )

    low_count = sum(
        1 for item in violations
        if item.get("severity") == "low"
    )

    if high_count:
        status = "high priority constraints detected"
    elif medium_count:
        status = "review recommended"
    elif violations:
        status = "minor constraints detected"
    else:
        status = "no major constraint violations detected"

    return {
        "status": status,
        "high_count": high_count,
        "medium_count": medium_count,
        "low_count": low_count,
        "total_count": len(violations),
        "violations": violations
    }
