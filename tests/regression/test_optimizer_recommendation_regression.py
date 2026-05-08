import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

root_str = str(ROOT)

if root_str not in sys.path:
    sys.path.insert(0, root_str)

from services.optimizer_execution_service import (
    run_optimizer,
)

from services.optimizer_recommendation_service import (
    recommend_optimizer,
)


def run():
    run_optimizer(
        "basic",
        {
            "target_gpm": 150,
        },
    )

    recommendation = recommend_optimizer(
        [
            "minimum_viable_match",
        ]
    )

    print("\nRECOMMENDATION:")
    print(recommendation)

    assert recommendation is not None

    assert recommendation["name"] == "basic"

    assert recommendation["average_score"] > 0

    print(
        "\nOptimizer recommendation regression passed"
    )


if __name__ == "__main__":
    run()
