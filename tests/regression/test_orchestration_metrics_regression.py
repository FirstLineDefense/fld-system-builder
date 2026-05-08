import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

root_str = str(ROOT)

if root_str not in sys.path:
    sys.path.insert(0, root_str)

from services.orchestration_execution_service import (
    run_orchestration,
)

from services.orchestration_event_stream_service import (
    clear_event_stream,
)

from services.orchestration_metrics_service import (
    build_metrics_summary,
)


def run():
    clear_event_stream()

    run_orchestration(
        [
            "minimum_viable_match",
        ],
        {
            "target_gpm": 180,
        },
    )

    run_orchestration(
        [
            "minimum_viable_match",
        ],
        {
            "target_gpm": 220,
        },
    )

    summary = build_metrics_summary()

    print("\nMETRICS SUMMARY:")
    print(summary)

    assert (
        summary["total_events"]
        == 4
    )

    assert (
        summary["event_types"][
            "orchestration_started"
        ]
        == 2
    )

    assert (
        summary["event_types"][
            "optimizer_completed"
        ]
        == 2
    )

    assert (
        summary["unique_sessions"]
        == 2
    )

    print(
        "\nOrchestration metrics regression passed"
    )


if __name__ == "__main__":
    run()
