import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

root_str = str(ROOT)

if root_str not in sys.path:
    sys.path.insert(0, root_str)

from services.orchestration_execution_service import (
    run_orchestration,
)

from services.orchestration_session_service import (
    get_session,
    summarize_session,
)


def run():
    execution = run_orchestration(
        [
            "minimum_viable_match",
        ],
        {
            "target_gpm": 180,
        },
    )

    print("\nEXECUTION:")
    print(execution)

    session_id = execution["session_id"]

    session = get_session(session_id)

    print("\nSESSION:")
    print(session)

    assert session is not None

    assert len(session["events"]) == 2

    summary = summarize_session(
        session_id
    )

    print("\nSUMMARY:")
    print(summary)

    assert summary["event_count"] == 2

    print(
        "\nOrchestration session regression passed"
    )


if __name__ == "__main__":
    run()
