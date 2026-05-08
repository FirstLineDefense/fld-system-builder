from copy import deepcopy

from config.proposal_profiles import DEFAULT_PROPOSAL_PROFILE


PROPOSAL_SCENARIOS = {
    "good": {
        **deepcopy(DEFAULT_PROPOSAL_PROFILE),
        "profile_name": "Good / Budget Install",
        "equipment_markup_percent": 25,
        "design_services": {
            "design_hours": 4,
            "design_hourly_rate": 125,
        },
        "maintenance_plan": {
            "maintenance_plan_fee": 750,
        },
        "subscription": {
            "subscription_fee": 0,
        },
    },

    "better": {
        **deepcopy(DEFAULT_PROPOSAL_PROFILE),
        "profile_name": "Better / Resilient Install",
        "equipment_markup_percent": 35,
        "design_services": {
            "design_hours": 8,
            "design_hourly_rate": 150,
        },
        "maintenance_plan": {
            "maintenance_plan_fee": 1250,
        },
        "subscription": {
            "subscription_fee": 0,
        },
    },

    "best": {
        **deepcopy(DEFAULT_PROPOSAL_PROFILE),
        "profile_name": "Best / Enterprise Autonomous Install",
        "equipment_markup_percent": 45,
        "design_services": {
            "design_hours": 16,
            "design_hourly_rate": 175,
        },
        "maintenance_plan": {
            "maintenance_plan_fee": 2500,
        },
        "subscription": {
            "subscription_fee": 1200,
        },
    },
}


def get_proposal_scenarios():
    return deepcopy(PROPOSAL_SCENARIOS)


def get_proposal_scenario(key):
    scenarios = get_proposal_scenarios()
    if key not in scenarios:
        raise KeyError(f"Unknown proposal scenario: {key}")
    return scenarios[key]
