def build_recommendation(
    priority,
    category,
    title,
    recommendation,
    reasoning=None
):
    return {
        "priority": priority,
        "category": category,
        "title": title,
        "recommendation": recommendation,
        "reasoning": reasoning or []
    }


def analyze_architecture_recommendations(system_result):
    recommendations = []

    manifold = system_result.get("manifold", {})
    summary = system_result.get("summary", {})
    optimizer = system_result.get("hydraulic_optimizer", {})
    readiness = system_result.get("design_readiness", {})

    total_flow = manifold.get("total_flow_gpm", 0)
    utilization = manifold.get("pump_flow_utilization_fraction", 0)
    active_branches = manifold.get("active_branch_count", 0)

    branch_results = manifold.get("branch_results", [])

    # ---------------------------------------------------
    # Last-line defense missing
    # ---------------------------------------------------

    for item in readiness.get("items", []):
        if item.get("name") == "Last-line defense validation":
            if item.get("status") != "ready":
                recommendations.append(build_recommendation(
                    1,
                    "critical_architecture",
                    "Add dedicated last-line defense zone",
                    "The current design does not contain a structure/eaves or last-line defense branch.",
                    [
                        "Proposal-grade wildfire systems should include a dedicated structure-defense operating mode.",
                        "This mode should govern the overall design before property hydration optimization."
                    ]
                ))

    # ---------------------------------------------------
    # Pump oversized
    # ---------------------------------------------------

    if utilization < 0.35:
        recommendations.append(build_recommendation(
            3,
            "pump_sizing",
            "Pump may be oversized",
            "Pump is operating at very low utilization relative to maximum flow capability.",
            [
                f"Current utilization is approximately {utilization * 100:.1f}%.",
                "This may indicate unnecessary pump cost, fuel consumption, or pressure reserve.",
                "Consider staged operation, smaller pumps, or higher-demand zoning."
            ]
        ))

    # ---------------------------------------------------
    # High velocity branches
    # ---------------------------------------------------

    for branch in branch_results:
        velocity = branch.get("velocity_fps", 0)

        if velocity > 8:
            recommendations.append(build_recommendation(
                2,
                "velocity",
                f"Reduce velocity on Branch {branch.get('branch_number')}",
                f"Branch velocity is currently {velocity:.2f} ft/s.",
                [
                    "Long-term wildfire systems generally benefit from conservative velocity targets.",
                    "Consider upsizing pipe, splitting zones, or reducing simultaneous flow."
                ]
            ))

    # ---------------------------------------------------
    # Very low velocity = possible oversizing
    # ---------------------------------------------------

    for branch in branch_results:
        velocity = branch.get("velocity_fps", 0)

        if velocity < 2 and branch.get("flow_gpm", 0) > 0:
            recommendations.append(build_recommendation(
                5,
                "oversizing",
                f"Branch {branch.get('branch_number')} may be oversized",
                "Very low velocity may indicate unnecessary pipe oversizing.",
                [
                    f"Current velocity is only {velocity:.2f} ft/s.",
                    "This may increase cost with minimal hydraulic benefit."
                ]
            ))

    # ---------------------------------------------------
    # High pressure surplus
    # ---------------------------------------------------

    surplus = manifold.get("pump_pressure_surplus_psi", 0)

    if surplus > 40:
        recommendations.append(build_recommendation(
            4,
            "pressure_surplus",
            "Pressure reserve may be excessive",
            f"System currently carries approximately {surplus:.1f} PSI surplus.",
            [
                "Some reserve is desirable for wildfire systems.",
                "Very large surplus may indicate unnecessary pump pressure or inefficient design balance."
            ]
        ))

    # ---------------------------------------------------
    # Branch split recommendation
    # ---------------------------------------------------

    split_recommendations = optimizer.get("branch_split_recommendations", [])

    for split in split_recommendations:
        recommendations.append(build_recommendation(
            2,
            "branch_split",
            f"Consider splitting Branch {split.get('branch_number')}",
            split.get("recommendation"),
            [
                split.get("reason", "")
            ]
        ))

    # ---------------------------------------------------
    # Water-limited
    # ---------------------------------------------------

    runtime = system_result.get("runtime", {})

    runtime_minutes = runtime.get("runtime_minutes", 0)
    required_runtime = runtime.get("required_runtime_minutes", 0)

    if runtime_minutes < required_runtime * 1.15:
        recommendations.append(build_recommendation(
            2,
            "runtime",
            "Water reserve margin is thin",
            "Available water storage is only slightly above the required runtime target.",
            [
                f"Estimated runtime: {runtime_minutes:.1f} minutes.",
                f"Target runtime: {required_runtime:.1f} minutes.",
                "Consider additional reserve for changing wildfire conditions."
            ]
        ))

    # ---------------------------------------------------
    # Staging recommendation
    # ---------------------------------------------------

    if active_branches >= 4 and utilization > 0.75:
        recommendations.append(build_recommendation(
            2,
            "staging",
            "Consider staged manifold operation",
            "High branch count and high utilization suggest staging may improve resilience.",
            [
                "Staging can reduce instantaneous hydraulic demand.",
                "This may improve pressure margin and reduce pipe size requirements."
            ]
        ))

    # ---------------------------------------------------
    # Sort
    # ---------------------------------------------------

    recommendations = sorted(
        recommendations,
        key=lambda item: item.get("priority", 999)
    )

    return {
        "recommendations": recommendations
    }