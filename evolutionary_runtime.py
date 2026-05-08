from copy import deepcopy
import random

from population_competition import (
    run_population_cycle
)

from crossover_engine import (
    crossover_candidates
)

from mutation_pressure import (
    get_mutation_scale
)

from mutation_context import (
    set_mutation_scale
)


def breed_population(
    survivors,
    target_population_size=20
):
    next_population = []

    survivor_candidates = [
        s["candidate"]
        for s in survivors
    ]

    while (
        len(next_population)
        < target_population_size
    ):

        parent_a = random.choice(
            survivor_candidates
        )

        parent_b = random.choice(
            survivor_candidates
        )

        child = crossover_candidates(
            parent_a,
            parent_b
        )

        next_population.append(child)

    return next_population


def evaluate_existing_population(
    population
):
    from mutation_evaluator import (
        evaluate_mutation
    )

    evolved = []

    for candidate in population:

        evolved.append(
            evaluate_mutation(candidate)
        )

    ranked = sorted(
        evolved,
        key=lambda r: r.get(
            "mutated_score",
            0
        ),
        reverse=True
    )

    survivors = ranked[:6]

    return {
        "ranked": ranked,
        "survivors": survivors
    }


def run_evolution(
    base_candidate,
    generations=10,
    population_size=20
):
    population_seed = deepcopy(
        base_candidate
    )

    history = []

    current_population = None

    best_score_seen = None
    stagnant_generations = 0

    for generation in range(generations):

        mutation_scale = get_mutation_scale(
            generation + 1,
            stagnant_generations
        )

        set_mutation_scale(
            mutation_scale
        )

        if generation == 0:

            result = run_population_cycle(
                population_seed,
                population_size
            )

        else:

            result = evaluate_existing_population(
                current_population
            )

        best_score = (
            result["ranked"][0]
            ["mutated_score"]
        )

        best_candidate = (
            result["ranked"][0]
            ["candidate"]
        )

        if (
            best_score_seen is None
            or best_score > best_score_seen
        ):
            best_score_seen = best_score
            stagnant_generations = 0

        else:
            stagnant_generations += 1

        history.append({
            "generation":
                generation + 1,

            "best_score":
                best_score,

            "best_score_seen":
                best_score_seen,

            "stagnant_generations":
                stagnant_generations,

            "mutation_scale":
                mutation_scale,

            "best_candidate":
                best_candidate
        })

        print()
        print(
            "GENERATION",
            generation + 1
        )

        print(
            "BEST SCORE:",
            best_score
        )

        print(
            "BEST SEEN:",
            best_score_seen
        )

        print(
            "STAGNANT GENERATIONS:",
            stagnant_generations
        )

        print(
            "MUTATION SCALE:",
            mutation_scale
        )

        print(
            "BEST PUMP:",
            best_candidate[
                "primary"
            ]["pump"]
        )

        print(
            "BEST MUTATION SCALE:",
            best_candidate.get(
                "mutation_scale",
                "n/a"
            )
        )

        survivors = (
            result.get("survivors")
            or result["ranked"][:6]
        )

        current_population = breed_population(
            survivors,
            population_size
        )

    return history
