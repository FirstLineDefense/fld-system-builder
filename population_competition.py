from copy import deepcopy

from mutation_evaluator import (
    evaluate_mutation
)


def create_population(
    base_candidate,
    population_size=20
):
    population = []

    for _ in range(population_size):
        population.append(
            deepcopy(base_candidate)
        )

    return population


def evolve_population(
    population
):
    evolved = []

    for candidate in population:

        result = evaluate_mutation(
            candidate
        )

        evolved.append(result)

    return evolved


def rank_population(
    evolved_population
):
    return sorted(
        evolved_population,
        key=lambda r: r.get(
            "mutated_score",
            0
        ),
        reverse=True
    )


def select_survivors(
    ranked_population,
    survivor_ratio=0.3
):
    survivor_count = max(
        1,
        int(
            len(ranked_population)
            * survivor_ratio
        )
    )

    return ranked_population[
        :survivor_count
    ]


def repopulate(
    survivors,
    population_size=20
):
    next_generation = []

    index = 0

    while len(next_generation) < population_size:

        survivor = survivors[
            index % len(survivors)
        ]

        next_generation.append(
            deepcopy(
                survivor["candidate"]
            )
        )

        index += 1

    return next_generation


def run_population_cycle(
    base_candidate,
    population_size=20
):
    population = create_population(
        base_candidate,
        population_size
    )

    evolved = evolve_population(
        population
    )

    ranked = rank_population(
        evolved
    )

    survivors = select_survivors(
        ranked
    )

    next_generation = repopulate(
        survivors,
        population_size
    )

    return {
        "best_score":
            ranked[0]["mutated_score"],

        "worst_score":
            ranked[-1]["mutated_score"],

        "survivor_count":
            len(survivors),

        "ranked":
            ranked,

        "next_generation":
            next_generation
    }
