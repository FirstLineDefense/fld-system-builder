from services.optimizer_recommendation_service import (
    recommend_optimizer,
)


DEFAULT_POLICY = {
    "minimum_average_score": 50,
    "required_capabilities": [],
    "blocked_optimizers": [],
}


def evaluate_optimizer_policy(
    recommendation,
    policy=None,
):
    policy = policy or DEFAULT_POLICY

    if recommendation is None:
        return (
            False,
            "No optimizer recommendation available",
        )

    if (
        recommendation["name"]
        in policy["blocked_optimizers"]
    ):
        return (
            False,
            "Optimizer blocked by policy",
        )

    if (
        recommendation["average_score"]
        < policy["minimum_average_score"]
    ):
        return (
            False,
            "Optimizer score below policy threshold",
        )

    required = policy[
        "required_capabilities"
    ]

    capabilities = recommendation.get(
        "capabilities",
        [],
    )

    missing = [
        capability
        for capability in required
        if capability not in capabilities
    ]

    if missing:
        return (
            False,
            f"Missing capabilities: {missing}",
        )

    return (
        True,
        "Policy approved",
    )


def recommend_policy_approved_optimizer(
    policy=None,
):
    policy = policy or DEFAULT_POLICY

    recommendation = recommend_optimizer(
        policy["required_capabilities"]
    )

    approved, reason = evaluate_optimizer_policy(
        recommendation,
        policy,
    )

    return {
        "approved": approved,
        "reason": reason,
        "recommendation": recommendation,
    }
