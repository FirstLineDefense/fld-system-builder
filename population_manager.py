def rank_population(results):
    ranked = sorted(
        results,
        key=lambda r: (
            r.get("mutated_score", 0)
        ),
        reverse=True
    )

    return ranked


def select_top_population(
    ranked,
    retain_ratio=0.3
):
    if not ranked:
        return []

    retain_count = max(
        1,
        int(len(ranked) * retain_ratio)
    )

    return ranked[:retain_count]


def summarize_population(ranked):
    summary = []

    for i, result in enumerate(ranked, 1):
        summary.append({
            "rank": i,
            "score": result.get(
                "mutated_score",
                0
            ),
            "improved": result.get(
                "improved",
                False
            )
        })

    return summary
