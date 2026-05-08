import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

root_str = str(ROOT)

if root_str not in sys.path:
    sys.path.insert(0, root_str)

from services.optimizer_execution_service import (
    run_optimizer,
)


def run():
    result = run_optimizer(
        "basic",
        {
            "target_gpm": 120,
        },
    )

    print("\nOPTIMIZER RESULT:")
    print(result)

    telemetry = result["telemetry"]

    assert telemetry["optimizer"] == "basic"

    assert telemetry["status"] == "success"

    assert telemetry["duration_seconds"] >= 0

    assert result["score"] == 60

    print(
        "\nOptimizer telemetry regression passed"
    )


if __name__ == "__main__":
    run()
