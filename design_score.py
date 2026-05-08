def suggest_design_score(primary):
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

    score = 100
    notes = []

    if not pump:
        score -= 20
        notes.append("pump missing")

    if not engine and not motor:
        score -= 20
        notes.append("power source missing")

    if not branches:
        score -= 20
        notes.append("branch data missing")

    high_velocity_count = 0
    high_loss_count = 0

    for branch in branches:
        velocity = float(branch.get("velocity_fps", 0) or 0)
        loss = float(branch.get("friction_loss_psi", 0) or branch.get("loss_psi", 0) or 0)

        if velocity >= 8:
            high_velocity_count += 1
            score -= 10

        if loss >= 15:
            high_loss_count += 1
            score -= 10

    if "wildfire" in operating_mode and "hybrid" not in operating_mode:
        score -= 10
        notes.append("wildfire system without hybrid fallback")

    score = max(0, min(100, score))

    if score >= 85:
        confidence = "high"
        icon = "✅"
        status = "strong"
    elif score >= 65:
        confidence = "medium"
        icon = "🚡"
        status = "developing"
    else:
        confidence = "low"
        icon = "⚠️"
        status = "incomplete"

    if notes:
        note_text = ", ".join(notes)
    else:
        note_text = "no major missing core inputs"

    suggestions.append({
        "type": "design_score",
        "label": "Design readiness score",
        "message": f"Current design score: {score}/100. Status: {status}. Main notes: {note_text}.",
        "confidence": confidence,
        "icon": icon,
        "reason": f"Score reflects missing core data, severe branch warnings, and operating-mode resilience gaps. High velocity branches: {high_velocity_count}. High loss branches: {high_loss_count}."
    })

    return suggestions
