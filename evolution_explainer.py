def explain_evolution_result(result):
    original = result.get("original_score")
    mutated = result.get("mutated_score")
    improvement = result.get("improvement")
    improved = result.get("improved")

    candidate = result.get("candidate", {}) or {}
    primary = candidate.get("primary", {}) or {}

    targets = candidate.get("mutation_targets", []) or []
    adaptive_targets = candidate.get("adaptive_targets", []) or []

    pump = primary.get("pump", {}) or {}
    branches = primary.get("branches", []) or []

    lines = []

    lines.append(
        f"Original score: {original}"
    )

    lines.append(
        f"Mutated score: {mutated}"
    )

    lines.append(
        f"Improvement: {improvement}"
    )

    if improved:
        lines.append(
            "Result: mutation improved the design"
        )
    else:
        lines.append(
            "Result: mutation did not improve the design"
        )

    if targets:
        lines.append(
            "Mutation targets: "
            + ", ".join(targets)
        )

    if adaptive_targets:
        lines.append(
            "Adaptive targets: "
            + ", ".join(adaptive_targets)
        )

    if pump:
        lines.append(
            "Pump GPM: "
            + str(pump.get("gpm"))
        )

    for index, branch in enumerate(branches, 1):
        lines.append(
            "Branch "
            + str(index)
            + ": "
            + "target_gpm="
            + str(branch.get("target_gpm"))
            + ", pipe_diameter_in="
            + str(branch.get("pipe_diameter_in"))
            + ", velocity_fps="
            + str(branch.get("velocity_fps"))
        )

    return "\n".join(lines)
