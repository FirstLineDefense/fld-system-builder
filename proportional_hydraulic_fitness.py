from fitness_normalization import (
    normalize_score,
    inverse_normalize_score
)


IDEAL_VELOCITY = 4.5
MAX_ACCEPTABLE_VELOCITY = 8.0

IDEAL_FRICTION = 3
MAX_ACCEPTABLE_FRICTION = 20


def calculate_branch_fitness(branch):
    velocity = float(
        branch.get("velocity_fps", 0) or 0
    )

    friction = float(
        branch.get("friction_loss_psi", 0)
        or branch.get("loss_psi", 0)
        or 0
    )

    velocity_score = inverse_normalize_score(
        velocity,
        MAX_ACCEPTABLE_VELOCITY
    )

    friction_score = inverse_normalize_score(
        friction,
        MAX_ACCEPTABLE_FRICTION
    )

    overall = round(
        (
            velocity_score * 0.65
            + friction_score * 0.35
        ),
        2
    )

    return {
        "velocity_score": velocity_score,
        "friction_score": friction_score,
        "overall_branch_fitness": overall
    }


def calculate_hydraulic_fitness(primary):
    branches = primary.get("branches", []) or []

    if not branches:
        return {
            "overall_hydraulic_fitness": 0,
            "branch_count": 0,
            "branches": []
        }

    results = []

    for branch in branches:
        results.append(
            calculate_branch_fitness(branch)
        )

    total = sum(
        r["overall_branch_fitness"]
        for r in results
    )

    overall = round(
        total / len(results),
        2
    )

    return {
        "overall_hydraulic_fitness": overall,
        "branch_count": len(results),
        "branches": results
    }
