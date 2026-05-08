import sys
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

root_str = str(ROOT)

if root_str not in sys.path:
    sys.path.insert(0, root_str)

from services.runtime_retention_service import (
    prune_optimizer_history,
)


def run():
    path = Path(
        "runtime_data/optimizer_history.json"
    )

    original = []

    if path.exists():
        original = json.loads(
            path.read_text()
        )

    oversized = []

    for i in range(400):
        oversized.append(
            {
                "optimizer": "basic",
                "score": i,
            }
        )

    path.write_text(
        json.dumps(
            oversized,
            indent=2,
        )
    )

    result = prune_optimizer_history()

    updated = json.loads(
        path.read_text()
    )

    print("\nRETENTION RESULT:")
    print(result)

    print("\nFINAL ENTRY COUNT:")
    print(len(updated))

    assert (
        result["status"]
        == "pruned"
    )

    assert (
        len(updated)
        == 250
    )

    path.write_text(
        json.dumps(
            original,
            indent=2,
        )
    )

    print(
        "\nRuntime retention regression passed"
    )


if __name__ == "__main__":
    run()
