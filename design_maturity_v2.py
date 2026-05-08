def evaluate_design_maturity_v2(input_data, primary):
    summary = primary.get("summary", {})
    manifold = primary.get("manifold", {})
    branch_results = manifold.get("branch_results", [])
    operating_modes = manifold.get("operating_modes", {}).get("modes", [])

    warnings = summary.get("warnings", [])
    pump = primary.get("pump")

    active_branches = [
        branch for branch in branch_results
        if branch.get("active")
    ]

    passing_branches = [
        branch for branch in active_branches
        if branch.get("passed")
    ]

    failing_branches = [
        branch for branch in active_branches
        if not branch.get("passed")
    ]

    first_line_modes = [
        mode for mode in operating_modes
        if "First Line" in mode.get("mode_name", "")
    ]

    last_line_modes = [
        mode for mode in operating_modes
        if "Last Line" in mode.get("mode_name", "")
    ]

    foam_modes = [
        mode for mode in operating_modes
        if "Foam" in mode.get("mode_name", "")
    ]

    first_line_passed = any(mode.get("passed") for mode in first_line_modes)
    last_line_passed = any(mode.get("passed") for mode in last_line_modes)
    foam_passed = any(mode.get("passed") for mode in foam_modes)

    hydraulic_passed = (
        len(active_branches) > 0
        and len(failing_branches) == 0
        and manifold.get("failing_branch_count", 0) == 0
    )

    pump_selected = pump is not None

    critical_warnings = []
    soft_warnings = []

    for warning in warnings:
        warning_text = str(warning)

        if (
            "does not pass" in warning_text
            or "No pump passed" in warning_text
            or "critical" in warning_text.lower()
        ):
            critical_warnings.append(warning_text)
        else:
            soft_warnings.append(warning_text)

    categories = []

    categories.append({
        "name": "Hydraulic Integrity",
        "passed": hydraulic_passed,
        "score": 30 if hydraulic_passed else 0,
        "max_score": 30,
        "note": "Active branches pass required pressure, pressure margin, and branch-level hydraulic checks."
    })

    categories.append({
        "name": "Pump Selection",
        "passed": pump_selected,
        "score": 15 if pump_selected else 0,
        "max_score": 15,
        "note": "A pump has been selected or auto-selected for the current design."
    })

    operating_score = 0
    if first_line_passed:
        operating_score += 15
    if last_line_passed:
        operating_score += 10
    if foam_passed:
        operating_score += 5

    categories.append({
        "name": "Operating Mode Coverage",
        "passed": operating_score >= 15,
        "score": operating_score,
        "max_score": 30,
        "note": "First Line, Last Line, and Foam modes are checked separately instead of collapsing the whole design into one pass/fail state."
    })

    warning_score = 15 if not critical_warnings else 5

    categories.append({
        "name": "Warning Severity",
        "passed": len(critical_warnings) == 0,
        "score": warning_score,
        "max_score": 15,
        "note": "Critical warnings reduce maturity, while soft warnings are preserved for engineering review."
    })

    total_score = sum(category["score"] for category in categories)
    max_score = sum(category["max_score"] for category in categories)

    if total_score < 35:
        grade = "Concept Grade"
    elif total_score < 65:
        grade = "Engineering Grade"
    elif total_score < 85:
        grade = "Proposal Grade"
    else:
        grade = "Deployment Grade"

    hard_gates = []

    if not hydraulic_passed:
        hard_gates.append("Hydraulic Integrity must pass before this can exceed Concept Grade.")

    if not pump_selected:
        hard_gates.append("Pump Selection must pass before this can exceed Concept Grade.")

    if not first_line_passed:
        hard_gates.append("First Line Defense Mode must pass before this can exceed Engineering Grade.")

    if hard_gates and grade in ["Proposal Grade", "Deployment Grade"]:
        grade = "Engineering Grade"

    if not hydraulic_passed or not pump_selected:
        grade = "Concept Grade"

    if grade == "Concept Grade":
        summary_text = "This design is useful for early concept comparison, but it is not ready for engineering review."
    elif grade == "Engineering Grade":
        summary_text = "This design has enough structure for engineering review, but unresolved architecture or operating-mode issues remain."
    elif grade == "Proposal Grade":
        summary_text = "This design is nearing proposal quality, but some deployment-readiness items still need review."
    else:
        summary_text = "This design is mature enough for deeper deployment planning, subject to professional engineering review."

    return {
        "version": "v2",
        "grade": grade,
        "score": total_score,
        "max_score": max_score,
        "score_percent": round((total_score / max_score) * 100, 1) if max_score else 0,
        "summary": summary_text,
        "categories": categories,
        "hard_gates": hard_gates,
        "critical_warnings": critical_warnings,
        "soft_warnings": soft_warnings,
        "mode_status": {
            "first_line_passed": first_line_passed,
            "last_line_passed": last_line_passed,
            "foam_passed": foam_passed,
        },
        "hydraulic_status": {
            "active_branch_count": len(active_branches),
            "passing_branch_count": len(passing_branches),
            "failing_branch_count": len(failing_branches),
            "hydraulic_passed": hydraulic_passed,
        }
    }