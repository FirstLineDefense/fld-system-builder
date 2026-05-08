_event_stream = []


def publish_event(
    session_id,
    event_type,
    payload,
):
    event = {
        "session_id": session_id,
        "event_type": event_type,
        "payload": payload,
    }

    _event_stream.append(event)

    return event


def get_event_stream():
    return list(_event_stream)


def clear_event_stream():
    _event_stream.clear()
