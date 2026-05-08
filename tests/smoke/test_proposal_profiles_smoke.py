import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from config.proposal_profiles import get_default_proposal_profile, flatten_proposal_profile


def main():
    profile = get_default_proposal_profile()

    profile["design_services"]["design_hours"] = 10
    fresh_profile = get_default_proposal_profile()

    if fresh_profile["design_services"]["design_hours"] != 0:
        raise AssertionError("Default proposal profile was mutated.")

    flat = flatten_proposal_profile(profile)

    expected_keys = {
        "markup_percent",
        "design_hours",
        "design_hourly_rate",
        "maintenance_plan_fee",
        "subscription_fee",
    }

    missing = expected_keys - set(flat.keys())
    if missing:
        raise AssertionError(f"Missing flattened proposal keys: {missing}")

    if flat["markup_percent"] != 35:
        raise AssertionError("Markup percent did not flatten correctly.")

    if flat["design_hours"] != 10:
        raise AssertionError("Design hours did not flatten correctly.")

    print("Proposal profile smoke test passed.")


if __name__ == "__main__":
    main()
