import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

root_str = str(ROOT)

if root_str not in sys.path:
    sys.path.insert(0, root_str)

from services.orchestration_execution_service import (
    run_orchestration,
)

from services.orchestration_snapshot_service import (
    load_snapshot,
)


def run():
    execution = run_orchestration(
        [
            "minimum_viable_match",
        ],
        {
            "target_gpm": 200,
        },
    )

    print("\nEXECUTION:")
    print(execution)

    session_id = execution["session_id"]

    snapshot = load_snapshot(
        session_id
    )

    print("\nSNAPSHOT:")
    print(snapshot)

    assert snapshot is not None

    assert snapshot["session_id"] == session_id

    assert len(snapshot["events"]) == 2

    print(
        "\nOrchestration snapshot regression passed"
    )


if __name__ == "__main__":
    run()
