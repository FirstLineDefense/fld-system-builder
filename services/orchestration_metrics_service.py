from services.orchestration_event_stream_service import (
    get_event_stream,
)


def build_metrics_summary():
    events = get_event_stream()

    summary = {
        "total_events": len(events),
        "event_types": {},
        "sessions": set(),
    }

    for event in events:
        event_type = event[
            "event_type"
        ]

        summary["event_types"][
            event_type
        ] = (
            summary["event_types"].get(
                event_type,
                0,
            )
            + 1
        )

        summary["sessions"].add(
            event["session_id"]
        )

    summary["unique_sessions"] = len(
        summary["sessions"]
    )

    summary["sessions"] = sorted(
        list(summary["sessions"])
    )

    return summary
