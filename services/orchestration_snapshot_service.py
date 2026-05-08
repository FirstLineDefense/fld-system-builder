import json
from pathlib import Path


SNAPSHOT_DIR = Path(
    "runtime_data/orchestration_snapshots"
)


def snapshot_path(session_id):
    return SNAPSHOT_DIR / (
        f"{session_id}.json"
    )


def save_snapshot(
    session_id,
    payload,
):
    path = snapshot_path(session_id)

    path.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
        )
    )

    return path


def load_snapshot(session_id):
    path = snapshot_path(session_id)

    if not path.exists():
        return None

    return json.loads(
        path.read_text()
    )
