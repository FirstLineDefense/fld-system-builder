from evolution_memory import (
    compare_candidates,
    summarize_candidate,
)

def summarize_evolution(history):
    if not history:
        return {
            "status": "no history"
        }

    first = history[0]
    final = history[-1]

    best = max(
        history,
        key=lambda item: item.get(
            "best_score",
            0
        )
    )

    best_candidate = (
        best.get("best_candidate", {})
        or {}
    )

    primary = (
        best_candidate.get("primary", {})
        or {}
    )

    branches = (
        primary.get("branches", [])
        or []
    )

    best_branch = (
        branches[0]
        if branches
        else {}
    )

    starting_candidate = (
        first.get("best_candidate", {})
        or {}
    )

    final_candidate = (
        final.get("best_candidate", {})
        or {}
    )

    best_candidate_summary = summarize_candidate(
        best_candidate
    )

    evolution_changes = compare_candidates(
        starting_candidate,
        best_candidate
    )

    return {
        "generations":
            len(history),

        "starting_score":
            first.get("best_score"),

        "final_score":
            final.get("best_score"),

        "best_score":
            best.get("best_score"),

        "total_improvement":
            round(
                best.get("best_score", 0)
                - first.get("best_score", 0),
                2
            ),

        "final_stagnant_generations":
            final.get("stagnant_generations"),

        "final_mutation_scale":
            final.get("mutation_scale"),

        "best_generation":
            best.get("generation"),

        "best_pump":
            primary.get("pump", {}),

        "best_motor":
            primary.get("motor", {}),

        "best_branch":
            best_branch,

        "best_candidate_summary":
            best_candidate_summary,

        "evolution_changes":
            evolution_changes
    }


def print_evolution_summary(history):
    summary = summarize_evolution(history)

    print()
    print("=== EVOLUTION SUMMARY ===")

    for key, value in summary.items():
        print(
            f"{key}: {value}"
        )

    return summary
