def evaluate_constraints(primary):
    constraints = []

    runtime_minutes = float(
        primary.get("runtime_minutes", 0) or 0
    )

    target_runtime = float(
        primary.get("target_runtime_minutes", 0) or 0
    )

    if target_runtime:
        constraints.append({
            "name": "runtime",
            "passed": runtime_minutes >= target_runtime,
            "actual": runtime_minutes,
            "target": target_runtime
        })

    operating_mode = (
        primary.get("operating_mode", "")
        or primary.get("mode", "")
        or ""
    ).lower()

    require_offgrid = bool(
        primary.get("require_offgrid", False)
    )

    if require_offgrid:
        passed = (
            "off-grid" in operating_mode
            or "hybrid" in operating_mode
        )

        constraints.append({
            "name": "offgrid",
            "passed": passed,
            "actual": operating_mode,
            "target": "off-grid capable"
        })

    require_hybrid = bool(
        primary.get("require_hybrid", False)
    )

    if require_hybrid:
        constraints.append({
            "name": "hybrid",
            "passed": "hybrid" in operating_mode,
            "actual": operating_mode,
            "target": "hybrid"
        })

    return constraints


def summarize_constraints(primary):
    constraints = evaluate_constraints(primary)

    if not constraints:
        return [{
            "type": "constraints",
            "label": "Optimization constraints",
            "message": "No optimization constraints configured.",
            "confidence": "medium",
            "icon": "📋",
            "reason": (
                "Constraint logic activates once runtime, "
                "architecture, or operational requirements "
                "are specified."
            )
        }]

    passed = sum(
        1 for c in constraints
        if c["passed"]
    )

    total = len(constraints)

    details = []

    for c in constraints:
        status = "PASS" if c["passed"] else "FAIL"

        details.append(
            f"{c['name']}: {status}"
        )

    confidence = (
        "high"
        if passed == total
        else "medium"
    )

    icon = (
        "✅"
        if passed == total
        else "⚠️"
    )

    return [{
        "type": "constraints",
        "label": "Optimization constraints",
        "message": (
            f"{passed}/{total} constraints satisfied. "
            + "; ".join(details)
        ),
        "confidence": confidence,
        "icon": icon,
        "reason": (
            "Constraint evaluation checks whether the "
            "current design satisfies required runtime "
            "and architecture conditions."
        )
    }]
