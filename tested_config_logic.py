def suggest_best_tested_configuration(primary):
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

    branch_count = len(branches)
    high_velocity_count = 0
    high_loss_count = 0

    for branch in branches:
        velocity = float(branch.get("velocity_fps", 0) or 0)
        loss = float(branch.get("friction_loss_psi", 0) or branch.get("loss_psi", 0) or 0)

        if velocity >= 8:
            high_velocity_count += 1

        if loss >= 15:
            high_loss_count += 1

    has_power = bool(engine or motor)
    has_pump = bool(pump)

    if branch_count and has_power and has_pump and high_velocity_count == 0 and high_loss_count == 0:
        suggestions.append({
            "type": "tested_config",
            "label": "Promising tested configuration",
            "message": "This configuration has pump, power, and branch data with no severe branch velocity or friction-loss warnings. It may be worth saving as a tested configuration candidate.",
            "confidence": "medium",
            "icon": "✅",
            "reason": "A tested configuration candidate should have complete core system data and no severe branch-level hydraulic warnings."
        })

    if "wildfire" in operating_mode and "hybrid" in operating_mode and has_power and has_pump:
        suggestions.append({
            "type": "tested_config",
            "label": "Wildfire hybrid candidate",
            "message": "This appears to be a wildfire-oriented hybrid configuration. If field testing confirms pressure, runtime, and restart behavior, save it as a high-priority reference setup.",
            "confidence": "high",
            "icon": "🔥",
            "reason": "Wildfire hybrid systems are cal to FLD's resilient architecture and should become reusable tested templates once validated."
        })

    if high_velocity_count or high_loss_count:
        suggestions.append({
            "type": "tested_config",
            "label": "Do not lock configuration yet",
            "message": f"This setup still has {high_velocity_count} high-velocity branch warning(s) and {high_loss_count} high-friction-loss warning(s). Optimize branches before treating it as a tested baseline.",
            "confidence": "high",
            "icon": "⚠️",
            "reason": "Configurations with severe branch warnings should not become preferred templates until hydraulic problems are resolved."
        })

    return suggestions
