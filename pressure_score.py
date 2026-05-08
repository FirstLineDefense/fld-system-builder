def score_pressure_performance(primary):
    branches = primary.get("branches", []) or []

    score = 100
    notes = []

    if not branches:
        return 50, "pressure data missing"

    for index, branch in enumerate(branches, start=1):
        required_psi = float(
            branch.get("required_terminal_pressure_psi", 0)
            or branch.get("required_pressure_psi", 0)
            or 50
        )

        final_psi = float(
            branch.get("final_pressure_psi", 0)
            or branch.get("available_pressure_psi", 0)
            or 0
        )

        elevation_ft = float(
            branch.get("elevation_change_ft", 0)
            or 0
        )

        friction_loss = float(
            branch.get("friction_loss_psi", 0)
            or branch.get("loss_psi", 0)
            or 0
        )

        if final_psi <= 0:
            notes.append(f"branch {index}: final pressure unknown")
            score -= 8
            continue

        margin = final_psi - required_psi

        if margin < 0:
            penalty = min(45, abs(margin) * 1.5)
            score -= penalty
            notes.append(f"branch {index}: pressure shortfall {round(abs(margin),1)} psi")

        elif margin < 10:
            penalty = round((10 - margin) * 1.2, 1)
            score -= penalty
            notes.append(f"branch {index}: thin pressure margin {round(margin,1)} psi")

        elif margin > 60:
            penalty = min(20, (margin - 60) * 0.3)
            score -= penalty
            notes.append(f"branch {index}: excessive pressure margin {round(margin,1)} psi")

        if elevation_ft > 100:
            notes.append(f"branch {index}: high elevation lift {round(elevation_ft,1)} ft")

        if friction_loss > 20:
            penalty = min(25, (friction_loss - 20) * 0.8)
            score -= penalty
            notes.append(f"branch {index}: high friction loss {round(friction_loss,1)} psi")

    score = max(0, min(100, round(score, 1)))

    return (
        score,
        ", ".join(notes) if notes else "pressure performance stable"
    )
