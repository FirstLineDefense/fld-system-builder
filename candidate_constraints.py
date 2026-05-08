def evaluate_candidate_constraints(candidate):
    primary = candidate.get("primary", {}) or {}
    branches = primary.get("branches", []) or []

    violations = []

    if not branches:
        violations.append("no branches available")

    for index, branch in enumerate(branches, start=1):
        gpm = float(branch.get("target_gpm", 0) or 0)
        velocity = float(branch.get("velocity_fps", 0) or 0)
        diameter = float(branch.get("pipe_diameter_in", 0) or 0)

        if gpm <= 0:
            violations.append(f"branch {index}: zero or negative flow")

        if diameter < 0.75:
            violations.append(f"branch {index}: pipe diameter too small")

        if velocity > 12:
            violations.append(f"branch {index}: velocity above hard max")

        if velocity < 2 and gpm > 0:
            violations.append(f"branch {index}: velocity below useful range")

    return {
        "passed": len(violations) == 0,
        "violations": violations
    }


def candidate_passes_constraints(candidate):
    return evaluate_candidate_constraints(candidate).get("passed", False)
