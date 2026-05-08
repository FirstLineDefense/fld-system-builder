from config.proposal_profiles import flatten_proposal_profile
from config.proposal_scenarios import get_proposal_scenarios
from services.output.proposal_pricing_service import generate_proposal_pricing


def generate_multi_scenario_proposals(cost_summary):
    scenarios = get_proposal_scenarios()

    results = {}

    for scenario_key, profile in scenarios.items():
        proposal_inputs = flatten_proposal_profile(profile)

        pricing = generate_proposal_pricing(
            cost_summary=cost_summary,
            markup_percent=proposal_inputs.get("markup_percent", 0),
            design_hours=proposal_inputs.get("design_hours", 0),
            design_hourly_rate=proposal_inputs.get("design_hourly_rate", 0),
            maintenance_plan_fee=proposal_inputs.get("maintenance_plan_fee", 0),
            subscription_fee=proposal_inputs.get("subscription_fee", 0),
        )

        results[scenario_key] = {
            "profile_name": profile.get("profile_name"),
            "proposal_profile": profile,
            "proposal_inputs": proposal_inputs,
            "proposal_pricing": pricing,
        }

    return results
