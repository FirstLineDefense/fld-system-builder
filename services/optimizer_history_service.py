import json
from pathlib import Path


HISTORY_PATH = Path(
    "runtime_data/optimizer_history.json"
)


def load_history():
    if not HISTORY_PATH.exists():
        return []

    return json.loads(
        HISTORY_PATH.read_text()
    )


def append_history(entry):
    history = load_history()

    history.append(entry)

    HISTORY_PATH.write_text(
        json.dumps(
            history,
            indent=2,
            sort_keys=True,
        )
    )

    return history


def latest_history():
    history = load_history()

    if not history:
        return None

    return history[-1]
