import uuid
from datetime import datetime


_active_sessions = {}


def create_session(context=None):
    session_id = str(uuid.uuid4())

    session = {
        "session_id": session_id,
        "created_at": datetime.utcnow().isoformat(),
        "context": context or {},
        "events": [],
    }

    _active_sessions[session_id] = session

    return session


def get_session(session_id):
    return _active_sessions.get(session_id)


def append_event(
    session_id,
    event_type,
    payload,
):
    session = get_session(session_id)

    if session is None:
        raise ValueError(
            f"Unknown session: {session_id}"
        )

    session["events"].append(
        {
            "event_type": event_type,
            "payload": payload,
            "timestamp": datetime.utcnow().isoformat(),
        }
    )

    return session


def summarize_session(session_id):
    session = get_session(session_id)

    if session is None:
        return None

    return {
        "session_id": session["session_id"],
        "created_at": session["created_at"],
        "event_count": len(
            session["events"]
        ),
        "context": session["context"],
    }
