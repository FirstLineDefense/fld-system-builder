def component_aware_mutation_pressure(candidate):
    primary = candidate.get("primary", {}) or {}
    score = 1.0

    pump = primary.get("pump", {}) or {}
    motor = primary.get("motor", {}) or {}
    branches = primary.get("branches", []) or []

    pump_gpm = pump.get("gpm") or pump.get("rated_gpm") or 0
    motor_hp = motor.get("hp") or 0

    total_branch_gpm = 0
    for branch in branches:
        total_branch_gpm += branch.get("target_gpm", 0) or 0

    if pump_gpm and total_branch_gpm:
        ratio = total_branch_gpm / pump_gpm

        if ratio > 1.15:
            score += 0.5

        if ratio < 0.55:
            score += 0.25

    if motor_hp and pump_gpm:
        hp_per_100_gpm = motor_hp / max(pump_gpm / 100, 1)

        if hp_per_100_gpm < 3:
            score += 0.35

    return min(score, 2.5)
