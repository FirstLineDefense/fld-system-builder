from weighted_score import calculate_weighted_design_score


def rank_candidates(candidates):
    ranked = []

    for candidate in candidates:
        result = calculate_weighted_design_score(
            candidate
        )

        score = result["overall_score"]

        ranked.append({
            "candidate": candidate,
            "score": score,
            "details": result
        })

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked


def select_top_candidates(
    candidates,
    keep_count=5
):
    ranked = rank_candidates(candidates)

    return ranked[:keep_count]


def summarize_candidate_ranking(
    candidates,
    keep_count=5
):
    ranked = rank_candidates(candidates)

    if not ranked:
        return [{
            "type": "ranking",
            "label": "Candidate ranking",
            "message": "No candidates available.",
            "confidence": "low",
            "icon": "⚠️",
            "reason": (
                "Ranking requires candidate designs."
            )
        }]

    best = ranked[0]

    kept = min(
        keep_count,
        len(ranked)
    )

    return [{
        "type": "ranking",
        "label": "Candidate ranking",
        "message": (
            f"Top score: "
            f"{best['score']}/100. "
            f"Keeping best {kept} candidates."
        ),
        "confidence": "high",
        "icon": "🏆",
        "reason": (
            "Candidate ranking allows the optimizer "
            "to evolve stronger architectures over "
            "multiple optimization cycles."
        )
    }]
