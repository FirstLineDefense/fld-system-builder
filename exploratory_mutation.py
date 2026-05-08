from copy import deepcopy
import random

from mutation_context import (
    get_current_mutation_scale
)

from hydraulic_recalculation import (
    recalculate_candidate_hydraulics
)


def maybe_apply_exploratory_mutation(candidate):
    mutated = deepcopy(candidate)

    scale = get_current_mutation_scale()

    # only explore meaningfully when mutation pressure rises
    probability = min(
        0.75,
        max(
            0.05,
            (scale - 1.0) * 0.35
        )
    )

    if random.random() > probability:
        mutated["exploratory_mutation"] = False
        return mutated

    primary = (
        mutated.get("primary", {})
        or {}
    )

    mutation_type = random.choice([
        "pump",
        "branch_diameter"
    ])

    if mutation_type == "pump":
        pump = primary.get("pump", {}) or {}

        current_gpm = (
            pump.get("gpm", 0)
            or 0
        )

        if current_gpm:
            factor = random.uniform(
                1.0 - (0.08 * scale),
                1.0 + (0.08 * scale)
            )

            pump["gpm"] = round(
                current_gpm * factor,
                1
            )

            primary["pump"] = pump

    if mutation_type == "branch_diameter":
        branches = (
            primary.get("branches", [])
            or []
        )

        if branches:
            branch = random.choice(branches)

            diameter = float(
                branch.get(
                    "pipe_diameter_in",
                    1.0
                ) or 1.0
            )

            step = random.choice([
                -0.5,
                0.5
            ])

            adjusted = max(
                1.0,
                diameter + step
            )

            branch["pipe_diameter_in"] = round(
                adjusted,
                2
            )

            primary["branches"] = branches

    mutated["primary"] = primary

    mutated = recalculate_candidate_hydraulics(
        mutated
    )

    mutated["exploratory_mutation"] = True
    mutated["exploratory_mutation_type"] = mutation_type
    mutated["exploratory_mutation_scale"] = scale

    return mutated
