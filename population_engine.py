from copy import deepcopy

from mutation_evaluator import (
    evaluate_mutation
)


def create_population(
    base_candidate,
    size=20
):
    population = []

    for _ in range(size):
        population.append(
            deepcopy(base_candidate)
        )

    return population


def evaluate_population(population):
    results = []

    for candidate in population:
        result = evaluate_mutation(
            candidate
        )

        results.append(result)

    return results


def rank_population(results):
    ranked = sorted(
        results,
        key=lambda result: result.get(
            "mutated_score",
            0
        ),
        reverse=True
    )

    return ranked


def select_elite(
    ranked_results,
    elite_count=5
):
    return ranked_results[:elite_count]


def build_next_generation(
    elite_results,
    population_size=20
):
    next_generation = []

    if not elite_results:
        return next_generation

    index = 0

    while len(next_generation) < population_size:
        elite = elite_results[
            index % len(elite_results)
        ]

        next_generation.append(
            deepcopy(
                elite["candidate"]
            )
        )

        index += 1

    return next_generation


def run_population_generation(
    base_candidate,
    population_size=20,
    elite_count=5
):
    population = create_population(
        base_candidate,
        size=population_size
    )

    results = evaluate_population(
        population
    )

    ranked = rank_population(
        results
    )

    elite = select_elite(
        ranked,
        elite_count=elite_count
    )

    next_generation = build_next_generation(
        elite,
        population_size=population_size
    )

    return {
        "ranked": ranked,
        "elite": elite,
        "next_generation": next_generation
    }
