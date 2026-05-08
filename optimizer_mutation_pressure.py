def determine_mutation_pressure(
    improvement,
    low_threshold=1.0,
    high_threshold=10.0
):
    if improvement <= low_threshold:
        return {
            "level": "high",
            "multiplier": 2.0,
            "reason": (
                "Low improvement detected. "
                "Increasing mutation diversity."
            )
        }

    if improvement >= high_threshold:
        return {
            "level": "low",
            "multiplier": 0.5,
            "reason": (
                "Strong improvement detected. "
                "Refining locally around good solutions."
            )
        }

    return {
        "level": "medium",
        "multiplier": 1.0,
        "reason": (
            "Moderate improvement detected. "
            "Using balanced mutation pressure."
        )
    }


def summarize_mutation_pressure(improvement):
    result = determine_mutation_pressure(
        improvement
    )

    return [{
        "type": "mutation_pressure",
        "label": "Adaptive mutation pressure",
        "message": (
            f"Mutation pressure: "
            f"{result['level']}. "
            f"Multiplier: "
            f"{result['multiplier']}x."
        ),
        "confidence": "high",
        "icon": "🧬",
        "reason": result["reason"]
    }]
