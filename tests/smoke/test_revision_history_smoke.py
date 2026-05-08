import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from services.presentation.revision_history_service import (
    generate_revision_history,
)


def main():
    revisions = generate_revision_history()

    if not revisions:
        raise AssertionError("No revisions generated.")

    required = {
        "revision",
        "date",
        "author",
        "notes",
    }

    for revision in revisions:
        missing = required - set(revision.keys())

        if missing:
            raise AssertionError(
                f"Missing revision fields: {missing}"
            )

    print("Revision history smoke test passed.")

    for revision in revisions:
        print(revision)


if __name__ == "__main__":
    main()
