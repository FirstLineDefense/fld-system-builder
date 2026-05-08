import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from services.output.multi_scenario_proposal_service import (
    generate_multi_scenario_proposals,
)


def main():
    cost_summary = {"total_cost": 5000}

    results = generate_multi_scenario_proposals(cost_summary)

    required = {"good", "better", "best"}
    missing = required - set(results.keys())

    if missing:
        raise AssertionError(f"Missing proposal scenarios: {missing}")

    for key, result in results.items():
        pricing = result.get("proposal_pricing", {})
        total = pricing.get("proposal_total", 0)

        if total <= 0:
            raise AssertionError(f"{key} scenario has invalid total.")

    good_total = results["good"]["proposal_pricing"]["proposal_total"]
    better_total = results["better"]["proposal_pricing"]["proposal_total"]
    best_total = results["best"]["proposal_pricing"]["proposal_total"]

    if not (good_total < better_total < best_total):
        raise AssertionError("Expected good < better < best proposal totals.")

    print("Multi-scenario proposal smoke test passed.")
    print("Good:", good_total)
    print("Better:", better_total)
    print("Best:", best_total)


if __name__ == "__main__":
    main()
