def build_bottleneck(
    priority,
    bottleneck_type,
    title,
    finding,
    recommended_action,
    evidence=None
):
    return {
        "priority": priority,
        "type": bottleneck_type,
        "title": title,
        "finding": finding,
        "recommended_action": recommended_action,
        "evidence": evidence or []
    }


def analyze_bottleneck_intelligence(system_result):
    bottlenecks = []

    manifold = system_result.get("manifold", {})
    runtime = system_result.get("runtime", {})
    readiness = system_result.get("design_readiness", {})
    optimizer = system_result.get("hydraulic_optimizer", {})

    branch_results = manifold.get("branch_results", [])
    operating_modes = manifold.get("operating_modes", {})

    total_flow = manifold.get("total_flow_gpm", 0)
    pump_utilization = manifold.get("pump_flow_utilization_fraction", 0)

    runtime_minutes = runtime.get("runtime_minutes", 0)
    required_runtime = runtime.get("required_runtime_minutes", 0)

    # ---------------------------------------------------
    # Structure / last-line defense limitation
    # ---------------------------------------------------

    for item in readiness.get("items", []):
        if item.get("name") == "Last-line defense validation":
            if item.get("status") != "ready":
                bottlenecks.append(build_bottleneck(
                    1,
                    "structure_defense_limited",
                    "Structure-defense mode is not defined",
                    "The current design cannot be treated as proposal-grade because no last-line or structure/eaves branch exists.",
                    "Add at least one dedicated last-line or structure/eaves branch, then make that mode the governing design case.",
                    [
                        "Last-line defense validation is not ready.",
                        "This limits confidence even if first-line/property hydration calculations pass."
                    ]
                ))

    # ---------------------------------------------------
    # Velocity-limited branches
    # ---------------------------------------------------

    high_velocity_branches = []

    for branch in branch_results:
        velocity = branch.get("velocity_fps", 0)
        flow = branch.get("flow", {}).get("total_flow_gpm", 0)

        if flow > 0 and velocity > 8:
            high_velocity_branches.append(branch)

    if high_velocity_branches:
        evidence = []

        for branch in high_velocity_branches:
            evidence.append(
                f"Branch {branch.get('branch_number')}: {branch.get('velocity_fps', 0):.2f} ft/s at {branch.get('flow', {}).get('total_flow_gpm', 0):.2f} GPM."
            )

        bottlenecks.append(build_bottleneck(
            2,
            "velocity_limited",
            "System is velocity-limited",
            "One or more active branches exceed the preferred velocity target.",
            "Upsize the affected branch pipe, split the branch into multiple zones, or reduce simultaneous branch flow.",
            evidence
        ))

    # ---------------------------------------------------
    # Pressure-margin limited branches
    # ---------------------------------------------------

    low_margin_branches = []

    for branch in branch_results:
        if branch.get("flow", {}).get("total_flow_gpm", 0) <= 0:
            continue

        margin = branch.get("pressure_margin_psi", 0)
        minimum_margin = branch.get("minimum_pressure_margin_psi", 20)

        if margin < minimum_margin:
            low_margin_branches.append(branch)

    if low_margin_branches:
        evidence = []

        for branch in low_margin_branches:
            evidence.append(
                f"Branch {branch.get('branch_number')}: margin {branch.get('pressure_margin_psi', 0):.2f} PSI, target {branch.get('minimum_pressure_margin_psi', 20):.2f} PSI."
            )

        bottlenecks.append(build_bottleneck(
            2,
            "pressure_margin_limited",
            "System is pressure-margin limited",
            "One or more active branches do not maintain the required pressure reserve.",
            "Increase pump pressure, reduce friction loss, reduce elevation penalty, reduce device demand, or upsize the affected branch pipe.",
            evidence
        ))

    # ---------------------------------------------------
    # Pump utilization / oversizing
    # ---------------------------------------------------

    if total_flow > 0 and pump_utilization < 0.35:
        bottlenecks.append(build_bottleneck(
            3,
            "pump_oversized",
            "Pump appears oversized for current demand",
            "The selected pump is operating at low flow utilization relative to its capacity.",
            "Evaluate whether a smaller pump, additional simultaneous zones, or a different staging strategy would better match the current design.",
            [
                f"Active operating flow: {total_flow:.2f} GPM.",
                f"Pump utilization: {pump_utilization * 100:.1f}%."
            ]
        ))

    if total_flow > 0 and pump_utilization > 0.85:
        bottlenecks.append(build_bottleneck(
            2,
            "pump_capacity_limited",
            "Pump is near capacity",
            "The selected pump is operating near the high end of its flow range.",
            "Consider reducing simultaneous zones, increasing pipe size, reducing device count, or selecting a larger pump.",
            [
                f"Active operating flow: {total_flow:.2f} GPM.",
                f"Pump utilization: {pump_utilization * 100:.1f}%."
            ]
        ))

    # ---------------------------------------------------
    # Runtime / water limitation
    # ---------------------------------------------------

    if required_runtime > 0 and runtime_minutes < required_runtime:
        bottlenecks.append(build_bottleneck(
            1,
            "water_limited",
            "System is water-limited",
            "Available water does not support the required runtime target.",
            "Increase water storage, reduce active flow, reduce simultaneous zones, or reduce required runtime.",
            [
                f"Estimated runtime: {runtime_minutes:.1f} minutes.",
                f"Required runtime: {required_runtime:.1f} minutes."
            ]
        ))

    elif required_runtime > 0 and runtime_minutes < required_runtime * 1.25:
        bottlenecks.append(build_bottleneck(
            4,
            "thin_water_reserve",
            "Water reserve margin is thin",
            "Available water meets the required runtime, but with limited reserve.",
            "Consider adding water reserve or reducing active operating flow.",
            [
                f"Estimated runtime: {runtime_minutes:.1f} minutes.",
                f"Required runtime: {required_runtime:.1f} minutes."
            ]
        ))

    # ---------------------------------------------------
    # Staging limitation
    # ---------------------------------------------------

    max_mode = operating_modes.get("max_simultaneous_mode", {})

    if max_mode and not max_mode.get("passed", True):
        bottlenecks.append(build_bottleneck(
            2,
            "staging_limited",
            "System is staging-limited",
            "The selected maximum simultaneous manifold-port assumption does not pass.",
            "Reduce maximum simultaneous ports, split operation into priority stages, or increase pump/pipe capacity.",
            [
                f"Max simultaneous ports tested: {manifold.get('max_simultaneous_ports', 0)}.",
                f"Max simultaneous mode passed: {max_mode.get('passed')}."
            ]
        ))

    # ---------------------------------------------------
    # No active flow / configuration problem
    # ---------------------------------------------------

    if total_flow <= 0:
        bottlenecks.append(build_bottleneck(
            1,
            "configuration_incomplete",
            "No active operating flow",
            "The current design has no meaningful hydraulic demand.",
            "Add active branches and selected sprinkler/device quantities before interpreting hydraulic results.",
            [
                "Total active operating flow is 0 GPM."
            ]
        ))

    # ---------------------------------------------------
    # Best optimizer action as bottleneck hint
    # ---------------------------------------------------

    best_actions = optimizer.get("best_actions", [])

    if best_actions:
        first_action = best_actions[0]
        bottlenecks.append(build_bottleneck(
            5,
            "optimizer_guidance",
            "Optimizer priority action",
            first_action.get("action", ""),
            first_action.get("details", ""),
            [
                "This is the top action currently identified by the hydraulic optimizer."
            ]
        ))

    bottlenecks = sorted(
        bottlenecks,
        key=lambda item: item.get("priority", 999)
    )

    if bottlenecks:
        primary = bottlenecks[0]
        summary = f"Primary bottleneck: {primary.get('title')}"
    else:
        summary = "No major bottlenecks detected from the current design data."

    return {
        "summary": summary,
        "bottlenecks": bottlenecks
    }