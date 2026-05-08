from pathlib import Path
import json


MAX_HISTORY_ENTRIES = 250


def prune_optimizer_history():
    path = Path(
        "runtime_data/optimizer_history.json"
    )

    if not path.exists():
        return {
            "status": "missing",
            "entries_removed": 0,
        }

    history = json.loads(
        path.read_text()
    )

    original_count = len(history)

    if original_count <= MAX_HISTORY_ENTRIES:
        return {
            "status": "unchanged",
            "entries_removed": 0,
            "current_entries": original_count,
        }

    trimmed = history[
        -MAX_HISTORY_ENTRIES:
    ]

    path.write_text(
        json.dumps(
            trimmed,
            indent=2,
        )
    )

    return {
        "status": "pruned",
        "entries_removed": (
            original_count
            - len(trimmed)
        ),
        "current_entries": len(trimmed),
    }
