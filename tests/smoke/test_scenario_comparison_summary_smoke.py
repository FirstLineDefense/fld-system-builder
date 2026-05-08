import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from services.presentation.scenario_comparison_service import (
    generate_scenario_comparison_summary,
)


def main():
    summary = generate_scenario_comparison_summary(
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

    required = [
        "GOOD / Budget Install",
        "BETTER / Resilient Install",
        "BEST / Enterprise Autonomous Install",
        "$6500.00",
        "$8200.00",
        "$12500.00",
        "same core engineering design foundation",
    ]

    for phrase in required:
        if phrase not in summary:
            raise AssertionError(f"Missing phrase: {phrase}")

    print("Scenario comparison summary smoke test passed.")
    print(summary)


if __name__ == "__main__":
    main()
