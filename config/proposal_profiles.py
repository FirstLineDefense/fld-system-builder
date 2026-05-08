from copy import deepcopy


DEFAULT_PROPOSAL_PROFILE = {
    "profile_name": "Default FLD Proposal Profile",
    "equipment_markup_percent": 35,

    "design_services": {
        "design_hours": 0,
        "design_hourly_rate": 0,
    },

    "maintenance_plan": {
        "maintenance_plan_fee": 0,
    },

    "subscription": {
        "subscription_fee": 0,
    },
}


def get_default_proposal_profile():
    return deepcopy(DEFAULT_PROPOSAL_PROFILE)


def flatten_proposal_profile(profile):
    profile = profile or get_default_proposal_profile()

    return {
        "markup_percent": profile.get("equipment_markup_percent", 0),
        "design_hours": profile.get("design_services", {}).get("design_hours", 0),
        "design_hourly_rate": profile.get("design_services", {}).get("design_hourly_rate", 0),
        "maintenance_plan_fee": profile.get("maintenance_plan", {}).get("maintenance_plan_fee", 0),
        "subscription_fee": profile.get("subscription", {}).get("subscription_fee", 0),
    }
