import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from services.presentation.bom_summary_service import (
    generate_bom_summary,
)


def main():
    items = generate_bom_summary()

    if not items:
        raise AssertionError("No BOM items generated.")

    required = {
        "category",
        "item",
        "quantity",
        "estimated_cost",
    }

    for item in items:
        missing = required - set(item.keys())

        if missing:
            raise AssertionError(
                f"Missing fields: {missing}"
            )

    print("BOM summary smoke test passed.")

    for item in items:
        print(item)


if __name__ == "__main__":
    main()
