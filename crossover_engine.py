from copy import deepcopy
import random


def crossover_candidates(
    parent_a,
    parent_b
):
    child = {
        "primary": {}
    }

    primary_a = (
        parent_a.get("primary", {})
        or {}
    )

    primary_b = (
        parent_b.get("primary", {})
        or {}
    )

    # pump inheritance
    child["primary"]["pump"] = deepcopy(
        random.choice([
            primary_a.get("pump", {}),
            primary_b.get("pump", {})
        ])
    )

    # motor inheritance
    child["primary"]["motor"] = deepcopy(
        random.choice([
            primary_a.get("motor", {}),
            primary_b.get("motor", {})
        ])
    )

    # branch inheritance
    child["primary"]["branches"] = deepcopy(
        random.choice([
            primary_a.get("branches", []),
            primary_b.get("branches", [])
        ])
    )

    # runtime inheritance
    child["primary"]["runtime_minutes"] = (
        random.choice([
            primary_a.get(
                "runtime_minutes",
                0
            ),
            primary_b.get(
                "runtime_minutes",
                0
            )
        ])
    )

    # storage inheritance
    child["primary"]["water_gallons"] = (
        random.choice([
            primary_a.get(
                "water_gallons",
                0
            ),
            primary_b.get(
                "water_gallons",
                0
            )
        ])
    )

    return child
