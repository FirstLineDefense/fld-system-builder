from services.orchestration_snapshot_service import (
    load_snapshot,
)

from services.orchestration_execution_service import (
    run_orchestration,
)


def replay_snapshot(session_id):
    snapshot = load_snapshot(session_id)

    if snapshot is None:
        raise ValueError(
            f"Unknown snapshot: {session_id}"
        )

    context = snapshot.get(
        "context",
        {},
    )

    required_capabilities = context.get(
        "required_capabilities",
        [],
    )

    events = snapshot.get(
        "events",
        [],
    )

    start_event = None

    for event in events:
        if (
            event["event_type"]
            == "orchestration_started"
        ):
            start_event = event
            break

    if start_event is None:
        raise ValueError(
            "Missing orchestration_started event"
        )

    requirements = start_event[
        "payload"
    ]["requirements"]

    replay_result = run_orchestration(
        required_capabilities,
        requirements,
    )

    return {
        "original_session_id": session_id,
        "replay_execution": replay_result,
    }
