import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

root_str = str(ROOT)

if root_str not in sys.path:
    sys.path.insert(0, root_str)

from services.optimizer_strategy_service import (
    choose_optimizer,
    execute_best_optimizer,
)


def run():
    optimizer = choose_optimizer(
        [
            "minimum_viable_match",
            "component_selection",
        ]
    )

    print("\nCHOSEN OPTIMIZER:")
    print(optimizer)

    assert optimizer["name"] == "basic"

    result = execute_best_optimizer(
        [
            "minimum_viable_match",
        ],
        {
            "target_gpm": 120,
        },
    )

    print("\nEXECUTION RESULT:")
    print(result)

    assert result["status"] == "success"

    print(
        "\nOptimizer strategy regression passed"
    )


if __name__ == "__main__":
    run()
