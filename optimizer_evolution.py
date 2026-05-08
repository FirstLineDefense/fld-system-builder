from optimizer_candidates import generate_candidate_variations
from optimizer_validation import filter_valid_candidates
from optimizer_ranking import select_top_candidates


def evolve_generation(
    base_candidate,
    cycles=3,
    variants_per_cycle=10,
    survivor_count=5
):
    current_population = [base_candidate]

    history = []

    for cycle in range(cycles):
        expanded = []

        for candidate in current_population:
            variants = generate_candidate_variations(
                candidate,
                count=variants_per_cycle
            )

            expanded.extend(variants)

        filtered = filter_valid_candidates(
            expanded
        )

        valid = filtered["valid"]

        ranked = select_top_candidates(
            valid,
            keep_count=survivor_count
        )

        current_population = [
            item["candidate"]
            for item in ranked
        ]

        history.append({
            "cycle": cycle + 1,
            "generated": len(expanded),
            "valid": len(valid),
            "survivors": len(current_population),
            "best_score": (
                ranked[0]["score"]
                if ranked
                else 0
            )
        })

    return {
        "final_population": current_population,
        "history": history
    }


def summarize_evolution(result):
    history = result.get("history", [])

    if not history:
        return [{
            "type": "evolution",
            "label": "Evolution loop",
            "message": "No evolution cycles executed.",
            "confidence": "low",
            "icon": "⚠️",
            "reason": (
                "Evolution summaries require cycle history."
            )
        }]

    final = history[-1]

    return [{
        "type": "evolution",
        "label": "Evolution loop",
        "message": (
            f"{len(history)} cycles completed. "
            f"Final best score: "
            f"{final['best_score']}/100. "
            f"{final['survivors']} survivors retained."
        ),
        "confidence": "high",
        "icon": "🧬",
        "reason": (
            "Evolution loops iteratively improve candidate "
            "designs across multiple optimization generations."
        )
    }]
