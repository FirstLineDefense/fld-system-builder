import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

root_str = str(ROOT)

if root_str not in sys.path:
    sys.path.insert(0, root_str)

from services.optimizer_execution_service import (
    run_optimizer,
)

from services.optimizer_policy_service import (
    recommend_policy_approved_optimizer,
)


def run():
    run_optimizer(
        "basic",
        {
            "target_gpm": 160,
        },
    )

    result = (
        recommend_policy_approved_optimizer(
            {
                "minimum_average_score": 50,
                "required_capabilities": [
                    "minimum_viable_match",
                ],
                "blocked_optimizers": [],
            }
        )
    )

    print("\nPOLICY RESULT:")
    print(result)

    assert result["approved"] is True

    recommendation = result[
        "recommendation"
    ]

    assert recommendation["name"] == "basic"

    print(
        "\nOptimizer policy regression passed"
    )


if __name__ == "__main__":
    run()
