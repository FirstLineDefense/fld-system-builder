GOAL_WEIGHTS = {
    "balanced": {
        "hydraulics": 0.30,
        "pump_matching": 0.20,
        "runtime": 0.20,
        "resilience": 0.20,
        "cost_simplicity": 0.10
    },

    "wildfire_resilience": {
        "hydraulics": 0.30,
        "pump_matching": 0.15,
        "runtime": 0.20,
        "resilience": 0.30,
        "cost_simplicity": 0.05
    },

    "cost_sensitive": {
        "hydraulics": 0.25,
        "pump_matching": 0.20,
        "runtime": 0.15,
        "resilience": 0.15,
        "cost_simplicity": 0.25
    },

    "hydraulic_performance": {
        "hydraulics": 0.40,
        "pump_matching": 0.30,
        "runtime": 0.10,
        "resilience": 0.15,
        "cost_simplicity": 0.05
    }
}


def get_goal_weights(goal="balanced"):
    return GOAL_WEIGHTS.get(
        goal,
        GOAL_WEIGHTS["balanced"]
    )
