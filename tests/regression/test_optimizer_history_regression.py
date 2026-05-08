import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

root_str = str(ROOT)

if root_str not in sys.path:
    sys.path.insert(0, root_str)

from services.optimizer_execution_service import (
    run_optimizer,
)

from services.optimizer_history_service import (
    load_history,
    latest_history,
)


def run():
    run_optimizer(
        "basic",
        {
            "target_gpm": 140,
        },
    )

    history = load_history()

    print("\nHISTORY:")
    print(history)

    assert len(history) >= 1

    latest = latest_history()

    print("\nLATEST ENTRY:")
    print(latest)

    assert latest["optimizer"] == "basic"

    assert latest["score"] == 70

    print(
        "\nOptimizer history regression passed"
    )


if __name__ == "__main__":
    run()
