import math


def calculate_pipe_velocity_fps(flow_gpm, diameter_in):
    if flow_gpm <= 0 or diameter_in <= 0:
        return 0

    cubic_ft_per_sec = flow_gpm * 0.002228
    diameter_ft = diameter_in / 12
    area_sq_ft = math.pi * (diameter_ft / 2) ** 2

    if area_sq_ft <= 0:
        return 0

    return cubic_ft_per_sec / area_sq_ft


def add_warning(items, severity, category, message, recommendation):
    items.append({
        "severity": severity,
        "category": category,
        "message": message,
        "recommendation": recommendation
    })


def add_pipe_recommendation(items, branch_number, current_pipe, recommended_pipe, reason, estimated_velocity):
    items.append({
        "branch_number": branch_number,
        "current_pipe": current_pipe,
        "recommended_pipe": recommended_pipe,
        "reason": reason,
        "estimated_velocity_fps": estimated_velocity
    })


def sorted_pipe_options(available_pipes):
    return sorted(
        available_pipes,
        key=lambda pipe: pipe.diameter_in
    )


def find_next_larger_pipe(current_pipe, available_pipes):
    if not current_pipe:
        return None

    pipes = sorted_pipe_options(available_pipes)

    for pipe in pipes:
        if pipe.diameter_in > current_pipe.diameter_in:
            return pipe

    return None


def find_pipe_for_velocity(flow_gpm, available_pipes, target_velocity_fps=8):
    pipes = sorted_pipe_options(available_pipes)

    for pipe in pipes:
        velocity = calculate_pipe_velocity_fps(flow_gpm, pipe.diameter_in)
        if velocity <= target_velocity_fps:
            return pipe, velocity

    if pipes:
        largest = pipes[-1]
        return largest, calculate_pipe_velocity_fps(flow_gpm, largest.diameter_in)

    return None, 0


def analyze_branch(branch):
    warnings = []

    pipe = branch.get("pipe")
    flow = branch.get("flow", {}).get("total_flow_gpm", 0)
    final_pressure = branch.get("final_pressure_psi", 0)
    required_pressure = branch.get("required_terminal_pressure_psi", 0)
    margin = branch.get("pressure_margin_psi", 0)
    role = branch.get("role", "")
    branch_number = branch.get("branch_number")

    diameter = pipe.diameter_in if pipe else 0
    velocity = calculate_pipe_velocity_fps(flow, diameter)

    if velocity > 10:
        add_warning(
            warnings,
            "Critical",
            "Branch Velocity",
            f"Branch {branch_number} velocity is very high at {velocity:.2f} ft/s.",
            "Increase branch pipe size, reduce device count on this branch, or split this branch into multiple manifold ports."
        )
    elif velocity > 8:
        add_warning(
            warnings,
            "Warning",
            "Branch Velocity",
            f"Branch {branch_number} velocity is elevated at {velocity:.2f} ft/s.",
            "Consider increasing pipe size or reducing simultaneous demand on this branch."
        )

    if margin < 0:
        add_warning(
            warnings,
            "Critical",
            "Pressure Margin",
            f"Branch {branch_number} is below required terminal pressure by {abs(margin):.2f} PSI.",
            "Increase pump pressure, reduce flow on this branch, shorten the branch, reduce elevation penalty, or increase pipe size."
        )
    elif margin < 10:
        add_warning(
            warnings,
            "Warning",
            "Pressure Margin",
            f"Branch {branch_number} has a thin pressure margin of {margin:.2f} PSI.",
            "Add design margin before treating this branch as reliable under fire conditions."
        )

    if role in ["last_line", "structure_eaves"] and not branch.get("passed"):
        add_warning(
            warnings,
            "Critical",
            "Last Line Defense",
            f"Branch {branch_number} is assigned to last-line or structure defense but does not pass.",
            "Treat this as a governing design failure. Structure/eaves protection should pass before first-line property hydration is trusted."
        )

    if flow <= 0:
        add_warning(
            warnings,
            "Warning",
            "Branch Configuration",
            f"Branch {branch_number} is active but has no flow.",
            "Add devices to this branch or deactivate it."
        )

    return {
        "branch_number": branch_number,
        "velocity_fps": velocity,
        "flow_gpm": flow,
        "final_pressure_psi": final_pressure,
        "required_pressure_psi": required_pressure,
        "pressure_margin_psi": margin,
        "warnings": warnings
    }


def generate_pipe_recommendations(system_result):
    manifold = system_result.get("manifold", {})
    available_pipes = system_result.get("available_pipes", [])
    recommendations = []

    for branch in manifold.get("branch_results", []):
        pipe = branch.get("pipe")
        branch_number = branch.get("branch_number")
        flow = branch.get("flow", {}).get("total_flow_gpm", 0)
        margin = branch.get("pressure_margin_psi", 0)

        if not pipe or flow <= 0:
            continue

        current_velocity = calculate_pipe_velocity_fps(flow, pipe.diameter_in)
        best_pipe, best_velocity = find_pipe_for_velocity(flow, available_pipes, target_velocity_fps=8)
        next_pipe = find_next_larger_pipe(pipe, available_pipes)

        if current_velocity > 8 and best_pipe and best_pipe.name != pipe.name:
            add_pipe_recommendation(
                recommendations,
                branch_number,
                pipe.name,
                best_pipe.name,
                f"Velocity is {current_velocity:.2f} ft/s. Target is 8 ft/s or lower for a conservative design check.",
                best_velocity
            )
        elif margin < 10 and next_pipe:
            add_pipe_recommendation(
                recommendations,
                branch_number,
                pipe.name,
                next_pipe.name,
                f"Pressure margin is thin at {margin:.2f} PSI. Upsizing may reduce friction loss and improve design margin.",
                calculate_pipe_velocity_fps(flow, next_pipe.diameter_in)
            )

    return recommendations


def generate_staging_recommendations(system_result):
    manifold = system_result.get("manifold", {})
    operating_modes = manifold.get("operating_modes", {})
    recommendations = []

    max_mode = operating_modes.get("max_simultaneous_mode", {})
    first_line = operating_modes.get("first_line_mode", {})
    last_line = operating_modes.get("last_line_mode", {})

    if last_line and not last_line.get("passed"):
        recommendations.append({
            "title": "Make last-line defense the governing mode",
            "recommendation": "Structure/eaves and last-line defense should pass before broader property hydration is optimized. Reduce competing branches, increase pump pressure, or upsize pipe on those branches."
        })

    if first_line and not first_line.get("passed"):
        recommendations.append({
            "title": "Stage first-line hydration",
            "recommendation": "First-line branches may need to operate in zones rather than all at once. Reduce simultaneous ports or split the first-line layer into priority stages."
        })

    if max_mode and not max_mode.get("passed"):
        recommendations.append({
            "title": "Reduce max simultaneous ports",
            "recommendation": "The selected max simultaneous operating assumption fails. Lower max simultaneous ports, reduce branch flow, or increase pump/pipe capacity."
        })

    if not recommendations:
        recommendations.append({
            "title": "Current staging assumption passes",
            "recommendation": "The current operating-mode assumptions pass the warning engine. Next refinement should focus on branch balancing and cut-sheet accuracy."
        })

    return recommendations


def generate_branch_split_recommendations(system_result):
    manifold = system_result.get("manifold", {})
    recommendations = []

    for branch in manifold.get("branch_results", []):
        branch_number = branch.get("branch_number")
        flow = branch.get("flow", {}).get("total_flow_gpm", 0)
        devices = branch.get("flow", {}).get("device_count", 0)
        margin = branch.get("pressure_margin_psi", 0)
        pipe = branch.get("pipe")
        diameter = pipe.diameter_in if pipe else 0
        velocity = calculate_pipe_velocity_fps(flow, diameter)

        if devices >= 4 and (velocity > 8 or margin < 10):
            recommendations.append({
                "branch_number": branch_number,
                "reason": f"Branch has {devices} devices, {flow:.2f} GPM, {velocity:.2f} ft/s velocity, and {margin:.2f} PSI margin.",
                "recommendation": "Consider splitting this branch into two manifold ports or downstream sub-branches to reduce friction and improve pressure margin."
            })

    return recommendations


def analyze_operating_mode(mode):
    warnings = []
    mode_name = mode.get("mode_name", "Unknown Mode")
    flow_ok = mode.get("flow_ok", True)
    passed = mode.get("passed", False)
    total_flow = mode.get("total_flow_gpm", 0)
    pump_capacity = mode.get("pump_flow_capacity_gpm", 0)
    worst = mode.get("worst_branch")

    if not flow_ok:
        add_warning(
            warnings,
            "Critical",
            "Pump Flow Capacity",
            f"{mode_name} requires {total_flow:.2f} GPM, but the pump is rated for {pump_capacity:.2f} GPM.",
            "Reduce simultaneous branches, reduce terminal devices, or select a higher-flow pump."
        )

    if not passed and worst:
        add_warning(
            warnings,
            "Warning",
            "Operating Mode",
            f"{mode_name} fails. Worst branch is Branch {worst.get('branch_number')} with {worst.get('pressure_margin_psi'):.2f} PSI margin.",
            "Use staged activation, reduce max simultaneous ports, or increase pump/pipe capacity."
        )

    return warnings


def generate_priority_recommendations(manifold):
    recommendations = []

    operating_modes = manifold.get("operating_modes", {})
    last_line = operating_modes.get("last_line_mode")
    first_line = operating_modes.get("first_line_mode")
    max_mode = operating_modes.get("max_simultaneous_mode")

    if last_line and not last_line.get("passed"):
        recommendations.append({
            "priority": "1",
            "title": "Fix last-line defense first",
            "recommendation": "Do not optimize property hydration until structure/eaves or last-line defense mode passes reliably."
        })

    if first_line and not first_line.get("passed"):
        recommendations.append({
            "priority": "2",
            "title": "Stage first-line defense",
            "recommendation": "First-line property hydration may need to run in smaller zones rather than all at once."
        })

    if max_mode and not max_mode.get("passed"):
        recommendations.append({
            "priority": "2",
            "title": "Reduce simultaneous manifold ports",
            "recommendation": "Lower the maximum simultaneous ports or increase pump/pipe capacity until max simultaneous mode passes."
        })

    if not recommendations:
        recommendations.append({
            "priority": "3",
            "title": "System passes current hydraulic checks",
            "recommendation": "Next refinement should focus on branch balancing, pipe sizing optimization, and cut-sheet accuracy."
        })

    return recommendations


def analyze_hydraulic_intelligence(system_result):
    manifold = system_result.get("manifold", {})
    runtime = system_result.get("runtime", {})
    pump = system_result.get("pump")

    warnings = []
    branch_analyses = []

    for branch in manifold.get("branch_results", []):
        branch_analysis = analyze_branch(branch)
        branch_analyses.append(branch_analysis)
        warnings.extend(branch_analysis["warnings"])

    for mode in manifold.get("operating_modes", {}).get("modes", []):
        warnings.extend(analyze_operating_mode(mode))

    if runtime and not runtime.get("passed_runtime_check", True):
        add_warning(
            warnings,
            "Warning",
            "Runtime",
            f"Runtime is only {runtime.get('runtime_minutes', 0):.2f} minutes.",
            "Increase water storage, reduce active flow, or reduce simultaneous manifold ports."
        )

    if pump and manifold.get("total_installed_flow_gpm", 0) > pump.max_flow_gpm:
        add_warning(
            warnings,
            "Info",
            "Installed Flow",
            f"Total installed flow is {manifold.get('total_installed_flow_gpm', 0):.2f} GPM, greater than pump capacity of {pump.max_flow_gpm:.2f} GPM.",
            "This may be acceptable if the system is intentionally staged, but the operating sequence must be explicit."
        )

    pipe_recommendations = generate_pipe_recommendations(system_result)
    staging_recommendations = generate_staging_recommendations(system_result)
    branch_split_recommendations = generate_branch_split_recommendations(system_result)

    critical_count = len([w for w in warnings if w["severity"] == "Critical"])
    warning_count = len([w for w in warnings if w["severity"] == "Warning"])
    info_count = len([w for w in warnings if w["severity"] == "Info"])

    if critical_count > 0:
        health = "Critical"
    elif warning_count > 0:
        health = "Needs Review"
    else:
        health = "Passes Current Checks"

    return {
        "health": health,
        "critical_count": critical_count,
        "warning_count": warning_count,
        "info_count": info_count,
        "warnings": warnings,
        "branch_analyses": branch_analyses,
        "priority_recommendations": generate_priority_recommendations(manifold),
        "pipe_recommendations": pipe_recommendations,
        "staging_recommendations": staging_recommendations,
        "branch_split_recommendations": branch_split_recommendations
    }