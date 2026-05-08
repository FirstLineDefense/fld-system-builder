def summarize_candidate(candidate):
    primary = candidate.get("primary", {}) or {}

    pump = primary.get("pump", {}) or {}
    motor = primary.get("motor", {}) or {}
    branches = primary.get("branches", []) or []

    total_branch_gpm = 0
    max_velocity = 0
    min_pressure = None

    for branch in branches:
        gpm = float(branch.get("gpm") or branch.get("target_gpm") or 0)
        velocity = float(branch.get("velocity_fps") or branch.get("velocity") or 0)
        pressure = branch.get("pressure_psi") or branch.get("psi")

        total_branch_gpm += gpm
        max_velocity = max(max_velocity, velocity)

        if pressure is not None:
            pressure = float(pressure)
            min_pressure = pressure if min_pressure is None else min(min_pressure, pressure)

    return {
        "pump_name": pump.get("name", "Unknown pump"),
        "pump_gpm": pump.get("gpm", 0),
        "motor_name": motor.get("name", "Unknown motor"),
        "motor_hp": motor.get("hp", 0),
        "branch_count": len(branches),
        "total_branch_gpm": round(total_branch_gpm, 2),
        "max_velocity_fps": round(max_velocity, 2),
        "min_pressure_psi": None if min_pressure is None else round(min_pressure, 2),
    }


def compare_candidates(previous, current):
    if not previous:
        return ["Initial candidate stored."]

    prev = summarize_candidate(previous)
    curr = summarize_candidate(current)

    notes = []

    for key in curr:
        if curr[key] != prev.get(key):
            notes.append(f"{key}: {prev.get(key)} -> {curr[key]}")

    if not notes:
        notes.append("No major summarized candidate changes detected.")

    return notes
