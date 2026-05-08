from generation_manager import (
    seed_candidate
)

from mutation_evaluator import (
    evaluate_mutation
)


from elite_memory import (
    update_elite,
    get_elite
)

from survivor_memory import (
    store_survivor,
    get_survivors
)


def run_evolution_cycles(
    base_candidate,
    cycles=5
):
    current = base_candidate

    history = []

    for i in range(cycles):
        seeded = seed_candidate(current)

        result = evaluate_mutation(seeded)

        store_survivor(result)

        update_elite(result)

        history.append({
            "cycle": i + 1,
            "score": result["mutated_score"],
            "improved": result["improved"]
        })

        current = result["candidate"]

    return {
        "history": history,
        "survivor_count": len(
            get_survivors()
        ),
        "best_candidate": get_elite()
    }
