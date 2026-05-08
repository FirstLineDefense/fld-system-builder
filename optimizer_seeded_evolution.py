from optimizer_evolution import evolve_generation
from optimizer_memory import get_best_memory_candidates


def build_seed_population(base_candidate, memory_count=5):
    seeds = [base_candidate]

    memory_items = get_best_memory_candidates(
        count=memory_count
    )

    for item in memory_items:
        candidate = item.get("candidate")

        if candidate:
            seeds.append(candidate)

    return seeds


def evolve_with_memory(
    base_candidate,
    cycles=3,
    variants_per_cycle=10,
    survivor_count=5,
    memory_count=5
):
    seeds = build_seed_population(
        base_candidate,
        memory_count=memory_count
    )

    results = []

    for seed in seeds:
        result = evolve_generation(
            seed,
            cycles=cycles,
            variants_per_cycle=variants_per_cycle,
            survivor_count=survivor_count
        )

        results.append(result)

    return {
        "seed_count": len(seeds),
        "results": results
    }


def summarize_seeded_evolution(result):
    seed_count = result.get("seed_count", 0)
    results = result.get("results", [])

    best_score = 0

    for item in results:
        history = item.get("history", [])

        if history:
            score = history[-1].get("best_score", 0)
            best_score = max(best_score, score)

    return [{
        "type": "seeded_evolution",
        "label": "Memory-seeded evolution",
        "message": (
            f"Seeded evolution ran from "
            f"{seed_count} starting designs. "
            f"Best final score: {best_score}/100."
        ),
        "confidence": "high",
        "icon": "🌱",
        "reason": (
            "Memory-seeded evolution allows the optimizer "
            "to reuse historically strong designs as starting "
            "points for future optimization cycles."
        )
    }]
