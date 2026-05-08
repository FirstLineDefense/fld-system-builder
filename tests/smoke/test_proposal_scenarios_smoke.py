import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from config.proposal_profiles import flatten_proposal_profile
from config.proposal_scenarios import get_proposal_scenarios, get_proposal_scenario


def main():
    scenarios = get_proposal_scenarios()

    required = {"good", "better", "best"}
    missing = required - set(scenarios.keys())

    if missing:
        raise AssertionError(f"Missing proposal scenarios: {missing}")

    for key in ["good", "better", "best"]:
        profile = get_proposal_scenario(key)
        flat = flatten_proposal_profile(profile)

        if flat["markup_percent"] <= 0:
            raise AssertionError(f"{key} scenario has invalid markup.")

        if "profile_name" not in profile:
            raise AssertionError(f"{key} scenario missing profile_name.")

    print("Proposal scenarios smoke test passed.")


if __name__ == "__main__":
    main()
