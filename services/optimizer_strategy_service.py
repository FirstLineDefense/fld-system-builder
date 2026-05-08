from services.optimizer_discovery_service import (
    discover_optimizers,
)

from services.optimizer_execution_service import (
    run_optimizer,
)


CAPABILITY_PRIORITY = {
    "minimum_viable_match": 10,
    "component_selection": 20,
    "baseline_optimization": 30,
    "cost_optimization": 40,
    "resilience_optimization": 50,
}


def choose_optimizer(required_capabilities):
    optimizers = discover_optimizers()

    ranked = []

    for optimizer in optimizers:
        capabilities = optimizer.get(
            "capabilities",
            [],
        )

        score = 0

        for capability in required_capabilities:
            if capability in capabilities:
                score += CAPABILITY_PRIORITY.get(
                    capability,
                    1,
                )

        ranked.append(
            (
                score,
                optimizer,
            )
        )

    ranked.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    if not ranked:
        raise ValueError(
            "No optimizers available"
        )

    best = ranked[0][1]

    return best


def execute_best_optimizer(
    required_capabilities,
    requirements,
):
    optimizer = choose_optimizer(
        required_capabilities
    )

    return run_optimizer(
        optimizer["name"],
        requirements,
    )
