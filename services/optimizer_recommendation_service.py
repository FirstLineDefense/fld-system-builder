from services.optimizer_analytics_service import (
    summarize_optimizer_performance,
)

from services.optimizer_discovery_service import (
    discover_optimizers,
)


MINIMUM_RUNS = 1


def recommend_optimizer(
    required_capabilities=None,
):
    required_capabilities = (
        required_capabilities or []
    )

    summaries = summarize_optimizer_performance()

    optimizers = discover_optimizers()

    candidates = []

    for optimizer in optimizers:
        name = optimizer["name"]

        capabilities = optimizer.get(
            "capabilities",
            [],
        )

        if required_capabilities:
            missing = [
                capability
                for capability in required_capabilities
                if capability not in capabilities
            ]

            if missing:
                continue

        performance = summaries.get(name)

        if not performance:
            continue

        if performance["runs"] < MINIMUM_RUNS:
            continue

        candidates.append(
            {
                "name": name,
                "average_score": performance[
                    "average_score"
                ],
                "average_duration": performance[
                    "average_duration"
                ],
                "runs": performance["runs"],
                "capabilities": capabilities,
            }
        )

    candidates.sort(
        key=lambda item: (
            item["average_score"],
            -item["average_duration"],
        ),
        reverse=True,
    )

    if not candidates:
        return None

    return candidates[0]
