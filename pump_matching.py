def calculate_pump_match(primary):
    pump = primary.get("pump", {}) or {}
    branches = primary.get("branches", []) or []

    pump_gpm = pump.get("gpm") or 0
    pump_psi = pump.get("psi") or 0

    total_required_gpm = 0
    worst_required_psi = 0

    for branch in branches:
        branch_gpm = branch.get("total_gpm") or branch.get("gpm") or 0
        branch_psi = branch.get("required_psi") or branch.get("psi") or 0

        total_required_gpm += branch_gpm
        worst_required_psi = max(worst_required_psi, branch_psi)

    gpm_ratio = pump_gpm / total_required_gpm if total_required_gpm else 0
    psi_ratio = pump_psi / worst_required_psi if worst_required_psi else 0

    gpm_fitness = min(gpm_ratio, 1.0) * 100
    psi_fitness = min(psi_ratio, 1.0) * 100

    weighted_score = round((gpm_fitness * 0.65) + (psi_fitness * 0.35), 2)

    weak_points = []

    if gpm_ratio < 1:
        weak_points.append("Pump GPM is below total branch demand")

    if psi_ratio < 1:
        weak_points.append("Pump PSI is below worst branch pressure demand")

    return {
        "pump_gpm": pump_gpm,
        "pump_psi": pump_psi,
        "required_gpm": round(total_required_gpm, 2),
        "required_psi": round(worst_required_psi, 2),
        "gpm_ratio": round(gpm_ratio, 3),
        "psi_ratio": round(psi_ratio, 3),
        "gpm_fitness": round(gpm_fitness, 2),
        "psi_fitness": round(psi_fitness, 2),
        "weighted_score": weighted_score,
        "weak_points": weak_points,
    }
