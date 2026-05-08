def calculate_score_improvement(history):
    if len(history) < 2:
        return 0

    first = history[0]["best_score"]
    last = history[-1]["best_score"]

    return last - first


def detect_convergence(
    history,
    threshold=1.0
):
    if len(history) < 2:
        return False

    improvement = calculate_score_improvement(
        history
    )

    return improvement <= threshold


def summarize_convergence(history):
    if not history:
        return [{
            "type": "convergence",
            "label": "Convergence tracking",
            "message": "No convergence history available.",
            "confidence": "low",
            "icon": "⚠️",
            "reason": (
                "Convergence requires optimization history."
            )
        }]

    improvement = calculate_score_improvement(
        history
    )

    converged = detect_convergence(history)

    if converged:
        confidence = "high"
        icon = "🧠"
        state = "Optimization converged"

    else:
        confidence = "medium"
        icon = "📈"
        state = "Optimization still improving"

    return [{
        "type": "convergence",
        "label": "Convergence tracking",
        "message": (
            f"{state}. "
            f"Score improvement: "
            f"{improvement:.1f} points."
        ),
        "confidence": confidence,
        "icon": icon,
        "reason": (
            "Convergence tracking detects when the "
            "optimizer begins stabilizing around "
            "high-performing configurations."
        )
    }]
