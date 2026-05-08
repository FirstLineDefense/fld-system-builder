import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

root_str = str(ROOT)

if root_str not in sys.path:
    sys.path.insert(0, root_str)

from services.orchestration_execution_service import (
    run_orchestration,
)

from services.orchestration_replay_service import (
    replay_snapshot,
)


def run():
    execution = run_orchestration(
        [
            "minimum_viable_match",
        ],
        {
            "target_gpm": 220,
        },
    )

    print("\nORIGINAL EXECUTION:")
    print(execution)

    session_id = execution["session_id"]

    replay = replay_snapshot(
        session_id
    )

    print("\nREPLAY RESULT:")
    print(replay)

    replay_result = replay[
        "replay_execution"
    ]["result"]

    assert replay_result["score"] == 100

    assert (
        replay["original_session_id"]
        == session_id
    )

    print(
        "\nOrchestration replay regression passed"
    )


if __name__ == "__main__":
    run()
