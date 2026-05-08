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
    get_event_stream,
)


def run():
    clear_event_stream()

    execution = run_orchestration(
        [
            "minimum_viable_match",
        ],
        {
            "target_gpm": 240,
        },
    )

    print("\nEXECUTION:")
    print(execution)

    stream = get_event_stream()

    print("\nEVENT STREAM:")
    print(stream)

    assert len(stream) == 2

    assert (
        stream[0]["event_type"]
        == "orchestration_started"
    )

    assert (
        stream[1]["event_type"]
        == "optimizer_completed"
    )

    print(
        "\nOrchestration event stream regression passed"
    )


if __name__ == "__main__":
    run()
