def identify_weak_components(candidate):
    primary = candidate.get("primary", {}) or {}

    weak = []

    pump = primary.get("pump", {}) or {}
    motor = primary.get("motor", {}) or {}
    branches = primary.get("branches", []) or []

    pump_gpm = pump.get("gpm") or 0
    motor_hp = motor.get("hp") or 0

    total_branch_gpm = 0

    for branch in branches:
        total_branch_gpm += (
            branch.get("target_gpm", 0) or 0
        )

        velocity = (
            branch.get("velocity_fps", 0) or 0
        )

        if velocity >= 8:
            weak.append("branch_diameter")

    if pump_gpm and total_branch_gpm:
        ratio = total_branch_gpm / pump_gpm

        if ratio > 1.15:
            weak.append("pump_capacity")

        elif ratio < 0.55:
            weak.append("pump_oversized")

    if motor_hp and pump_gpm:
        hp_per_100_gpm = (
            motor_hp / max(pump_gpm / 100, 1)
        )

        if hp_per_100_gpm < 3:
            weak.append("motor_power")

    return list(set(weak))
