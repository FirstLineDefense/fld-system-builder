def suggest_next_optimization_step(primary):
    suggestions = []

    branches = primary.get("branches", []) or []
    operating_mode = (
        primary.get("operating_mode", "")
        or primary.get("mode", "")
        or ""
    ).lower()

    engine = primary.get("engine", {}) or {}
    motor = primary.get("motor", {}) or {}
    pump = primary.get("pump", {}) or {}

    worst_branch = None
    worst_score = 0

    for branch in branches:
        name = branch.get("name", "Branch")
        velocity = float(branch.get("velocity_fps", 0) or 0)
        loss = float(branch.get("friction_loss_psi", 0) or branch.get("loss_psi", 0) or 0)

        score = 0

        if velocity >= 8:
            score += 4
        elif velocity >= 6:
            score += 2

        if loss >= 15:
            score += 4
        elif loss >= 8:
            score += 2

        if score > worst_score:
            worst_score = score
            worst_branch = {
                "name": name,
                "velocity": velocity,
                "loss": loss,
                "score": score
            }

    if worst_branch:
        suggestions.append({
            "type": "optimizer",
            "label": "Next optimization step",
            "message": f"Optimize {worst_branch['name']} next. It has about {worst_branch['velocity']:.1f} ft/sec velocity and {worst_branch['loss']:.1f} psi branch loss.",
            "confidence": "high",
            "icon": "🎯",
            "reason": "The optimizer ranks branch issues by combined velocity and friction-loss severity."
        })

        return suggestions

    if not pump:
        suggestions.append({
            "type": "optimizer",
            "label": "Next optimization step",
            "message": "Select or confirm the pump next. Branch recommendations become more useful once available pump pressure and flow are known.",
            "confidence": "medium",
            "icon": "💧",
            "reason": "Pump capability is required to evaluate whether the hydraulic design has enough pressure and flow margin."
        })

        return suggestions

    if not engine and not motor:
        suggestions.append({
            "type": "optimizer",
            "label": "Next optimization step",
            "message": "Select or confirm the power source next. Generator, battery, and fuel sizing depend on engine or motor data.",
            "confidence": "medium",
            "icon": "⚡",
            "reason": "Power architecture determines runtime, fallback behavior, and energy storage requirements."
        })

        return suggestions

    if "wildfire" in operating_mode and "hybrid" not in operating_mode:
        suggestions.append({
            "type": "optimizer",
            "label": "Next optimization step",
            "message": "Consider whether this wildfire system should be modeled as hybrid. Hybrid architecture improves resilience planning for grid loss, generator fallback, and battery reserve.",
            "confidence": "medium",
            "icon": "🔁",
            "reason": "Wildfire systems often need layered fallback logic rather than a single energy source."
        })

        return suggestions

    suggestions.append({
        "type": "optimizer",
        "label": "Next optimization step",
        "message": "No severe next-step optimization was detected. This design may be ready for report/cut-sheet preparation after review.",
        "confidence": "medium",
        "icon": "✅",
        "reason": "The optimizer did not find severe branch issues or missing core pump/power data."
    })

    return suggestions
