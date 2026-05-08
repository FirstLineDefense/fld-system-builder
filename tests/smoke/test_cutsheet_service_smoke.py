import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from services.presentation.cutsheet_service import (
    generate_cutsheet_references,
)


def main():
    refs = generate_cutsheet_references()

    if not refs:
        raise AssertionError("No cutsheet references generated.")

    required = {
        "component",
        "manufacturer",
        "document_type",
        "status",
    }

    for ref in refs:
        missing = required - set(ref.keys())

        if missing:
            raise AssertionError(
                f"Missing fields: {missing}"
            )

    print("Cutsheet service smoke test passed.")

    for ref in refs:
        print(ref)


if __name__ == "__main__":
    main()
