def evaluate_design_maturity(input_data, result):
    """
    Evaluates FLD design maturity.

    Grades:
    - Concept Grade
    - Engineering Grade
    - Proposal Grade
    - Deployment Grade
    """

    checks = []
    blockers = []
    recommendations = []

    branches = input_data.get("branches", [])
    active_branches = [branch for branch in branches if branch.get("active")]

    warnings = result.get("warnings", [])
    branch_results = result.get("branch_results", [])

    has_active_branches = len(active_branches) > 0
    has_pump = result.get("selected_pump") is not None
    has_water_storage = input_data.get("water_storage_name", "None") != "None"
    has_controls = len(input_data.get("selected_controls", [])) > 0
    has_sensors = len(input_data.get("selected_sensors", [])) > 0

    all_branches_pass = True

    if branch_results:
        for branch_result in branch_results:
            if not branch_result.get("passed", False):
                all_branches_pass = False
                break
    else:
        all_branches_pass = False

    has_critical_warning = False

    for warning in warnings:
        warning_lower = str(warning).lower()

        if (
            "critical" in warning_lower
            or "does not pass" in warning_lower
            or "no pump passed" in warning_lower
            or "no active branches" in warning_lower
        ):
            has_critical_warning = True

    checks.append({
        "name": "Active branches defined",
        "passed": has_active_branches,
        "note": "At least one active hydraulic branch exists."
    })

    checks.append({
        "name": "Pump selected",
        "passed": has_pump,
        "note": "A pump has been selected or auto-selected."
    })

    checks.append({
        "name": "Water storage selected",
        "passed": has_water_storage,
        "note": "A water source or storage component has been selected."
    })

    checks.append({
        "name": "Branch hydraulic results passing",
        "passed": all_branches_pass,
        "note": "All branch-level hydraulic checks pass."
    })

    checks.append({
        "name": "No critical warnings",
        "passed": not has_critical_warning,
        "note": "No critical system warnings are present."
    })

    checks.append({
        "name": "Controls selected",
        "passed": has_controls,
        "note": "Control hardware is selected."
    })

    checks.append({
        "name": "Sensors selected",
        "passed": has_sensors,
        "note": "Sensor hardware is selected."
    })

    passed_count = sum(1 for check in checks if check["passed"])
    total_count = len(checks)

    if not has_active_branches:
        blockers.append("No active branches are defined.")

    if not has_pump:
        blockers.append("No pump has been selected.")

    if not has_water_storage:
        blockers.append("No water storage or water source has been selected.")

    if not all_branches_pass:
        blockers.append("One or more branch hydraulic checks are not passing.")

    if has_critical_warning:
        blockers.append("Critical warnings are present and must be resolved.")

    if not has_controls:
        recommendations.append("Select control hardware before treating this as proposal-ready.")

    if not has_sensors:
        recommendations.append("Select sensor hardware before treating this as deployment-ready.")

    if passed_count <= 3:
        maturity_grade = "Concept Grade"
        maturity_summary = "This design is useful for early layout thinking, rough comparison, and discussion, but it is not ready for engineering review."
    elif passed_count <= 5:
        maturity_grade = "Engineering Grade"
        maturity_summary = "This design has enough structure for technical review, but it still needs unresolved issues cleaned up before proposal use."
    elif passed_count == 6:
        maturity_grade = "Proposal Grade"
        maturity_summary = "This design is close to client-facing proposal quality, but at least one deployment-readiness item remains incomplete."
    else:
        maturity_grade = "Deployment Grade"
        maturity_summary = "This design has passed the current maturity checks and is suitable for deeper deployment planning."

    if blockers:
        maturity_status = "Blocked"
    elif maturity_grade == "Deployment Grade":
        maturity_status = "Ready"
    else:
        maturity_status = "In Progress"

    return {
        "grade": maturity_grade,
        "status": maturity_status,
        "summary": maturity_summary,
        "passed_count": passed_count,
        "total_count": total_count,
        "checks": checks,
        "blockers": blockers,
        "recommendations": recommendations,
    }