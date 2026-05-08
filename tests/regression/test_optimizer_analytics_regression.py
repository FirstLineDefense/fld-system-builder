import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

root_str = str(ROOT)

if root_str not in sys.path:
    sys.path.insert(0, root_str)

from services.optimizer_execution_service import (
    run_optimizer,
)

from services.optimizer_analytics_service import (
    summarize_optimizer_performance,
    rank_optimizers,
)


def run():
    run_optimizer(
        "basic",
        {
            "target_gpm": 100,
        },
    )

    run_optimizer(
        "basic",
        {
            "target_gpm": 140,
        },
    )

    summary = summarize_optimizer_performance()

    print("\nSUMMARY:")
    print(summary)

    assert "basic" in summary

    basic = summary["basic"]

    assert basic["runs"] >= 2

    ranked = rank_optimizers()

    print("\nRANKED:")
    print(ranked)

    assert ranked[0][0] == "basic"

    print(
        "\nOptimizer analytics regression passed"
    )


if __name__ == "__main__":
    run()
