import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from services.presentation.executive_summary_service import generate_executive_summary


def main():
    summary = generate_executive_summary(
        project={"name": "Test Property"},
        cost_summary={"total_cost": 4180},
        multi_scenario_proposals={"good": {}, "better": {}, "best": {}},
    )

    required_phrases = [
        "FLD EXECUTIVE SUMMARY",
        "Test Property",
        "layered wildfire protection infrastructure",
        "3 proposal scenarios",
        "attack hose connection points",
    ]

    for phrase in required_phrases:
        if phrase not in summary:
            raise AssertionError(f"Missing executive summary phrase: {phrase}")

    print("Executive summary smoke test passed.")
    print(summary)


if __name__ == "__main__":
    main()
