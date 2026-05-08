import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from services.presentation.scenario_matrix_service import (
    generate_scenario_matrix,
)


def main():
    matrix = generate_scenario_matrix(
        multi_scenario_proposals={
            "good": {
                "proposal_pricing": {
                    "proposal_total": 6500,
                }
            },
            "better": {
                "proposal_pricing": {
                    "proposal_total": 8200,
                }
            },
            "best": {
                "proposal_pricing": {
                    "proposal_total": 12500,
                }
            },
        }
    )

    if len(matrix) != 3:
        raise AssertionError("Expected 3 matrix entries.")

    labels = [row["label"] for row in matrix]

    required = {"GOOD", "BETTER", "BEST"}

    if set(labels) != required:
        raise AssertionError(f"Missing labels: {required - set(labels)}")

    print("Scenario matrix smoke test passed.")

    for row in matrix:
        print(row)


if __name__ == "__main__":
    main()
