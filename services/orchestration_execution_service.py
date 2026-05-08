from services.orchestration_session_service import (
    create_session,
    append_event,
    get_session,
)

from services.optimizer_strategy_service import (
    execute_best_optimizer,
)

from services.orchestration_snapshot_service import (
    save_snapshot,
)

from services.orchestration_event_stream_service import (
    publish_event,
)


def run_orchestration(
    required_capabilities,
    requirements,
):
    session = create_session(
        {
            "required_capabilities": (
                required_capabilities
            ),
        }
    )

    session_id = session["session_id"]

    start_payload = {
        "requirements": requirements,
    }

    append_event(
        session_id,
        "orchestration_started",
        start_payload,
    )

    publish_event(
        session_id,
        "orchestration_started",
        start_payload,
    )

    result = execute_best_optimizer(
        required_capabilities,
        requirements,
    )

    append_event(
        session_id,
        "optimizer_completed",
        result,
    )

    publish_event(
        session_id,
        "optimizer_completed",
        result,
    )

    final_session = get_session(
        session_id
    )

    save_snapshot(
        session_id,
        final_session,
    )

    return {
        "session_id": session_id,
        "result": result,
    }
