def score_pipe_realism(primary):
    branches = primary.get("branches", []) or []

    score = 100
    notes = []

    for branch in branches:
        diameter = float(
            branch.get("pipe_diameter_in", 0)
            or 0
        )

        gpm = float(
            branch.get("target_gpm", 0)
            or 0
        )

        if diameter >= 4:
            score -= 35
            notes.append(f"extreme diameter {diameter}")

        elif diameter >= 3:
            score -= 18
            notes.append(f"large diameter {diameter}")

        if gpm < 100 and diameter >= 3:
            score -= 20
            notes.append("oversized relative to demand")

    score = max(0, min(100, score))

    return (
        score,
        ", ".join(notes)
        if notes
        else "pipe realism healthy"
    )


def score_pump_utilization(primary):
    pump = primary.get("pump", {}) or {}
    branches = primary.get("branches", []) or []

    pump_gpm = float(
        pump.get("gpm", 0) or 0
    )

    total_branch_gpm = 0

    for branch in branches:
        total_branch_gpm += (
            branch.get("target_gpm", 0)
            or 0
        )

    if not pump_gpm:
        return 50, "pump missing"

    utilization = total_branch_gpm / pump_gpm

    target_utilization = 0.85
    deviation = abs(target_utilization - utilization)

    penalty = min(
        40,
        round(deviation * 100, 1)
    )

    score = 100 - penalty

    return (
        max(0, min(100, score)),
        f"utilization {round(utilization, 2)}"
    )
