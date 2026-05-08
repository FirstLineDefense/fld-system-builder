import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from services.presentation.recommendation_engine_service import (
    generate_recommendation_summary,
)


def main():
    summary = generate_recommendation_summary(
        multi_scenario_proposals={
            "better": {
                "proposal_pricing": {
                    "proposal_total": 8093,
                }
            }
        }
    )

    required = [
        "FLD RECOMMENDED DEPLOYMENT STRATEGY",
        "BETTER / Resilient Install",
        "$8093.00",
        "Property slope",
        "Responder integration objectives",
    ]

    for phrase in required:
        if phrase not in summary:
            raise AssertionError(f"Missing phrase: {phrase}")

    print("Recommendation engine smoke test passed.")
    print(summary)


if __name__ == "__main__":
    main()
