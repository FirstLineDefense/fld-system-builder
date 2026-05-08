import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from services.presentation.component_spec_service import (
    generate_component_spec_cards,
)


def main():
    cards = generate_component_spec_cards()

    if not cards:
        raise AssertionError("No component spec cards generated.")

    for card in cards:
        required = {
            "category",
            "title",
            "summary",
            "features",
        }

        missing = required - set(card.keys())

        if missing:
            raise AssertionError(
                f"Missing keys: {missing}"
            )

    print("Component spec service smoke test passed.")

    for card in cards:
        print(card["title"])


if __name__ == "__main__":
    main()
