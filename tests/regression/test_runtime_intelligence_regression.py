import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

root_str = str(ROOT)

if root_str not in sys.path:
    sys.path.insert(0, root_str)

from runtime.runtime_intelligence_manager import (
    RuntimeIntelligenceManager,
)

from services.orchestration_execution_service import (
    run_orchestration,
)


def run():
    run_orchestration(
        [
            "minimum_viable_match",
        ],
        {
            "target_gpm": 250,
        },
    )

    manager = (
        RuntimeIntelligenceManager()
    )

    summary = (
        manager.build_runtime_summary()
    )

    print("\nRUNTIME SUMMARY:")
    print(summary)

    assert (
        "history_entries"
        in summary
    )

    assert (
        "metrics"
        in summary
    )

    assert (
        "optimizer_summary"
        in summary
    )

    retention = (
        manager.apply_retention()
    )

    print("\nRETENTION RESULT:")
    print(retention)

    print(
        "\nRuntime intelligence regression passed"
    )


if __name__ == "__main__":
    run()
