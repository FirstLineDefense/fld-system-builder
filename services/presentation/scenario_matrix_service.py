def generate_scenario_matrix(
    multi_scenario_proposals=None,
):
    multi_scenario_proposals = multi_scenario_proposals or {}

    matrix = []

    metadata = {
        "good": {
            "label": "GOOD",
            "badge": "Entry Tier",
            "automation": "Basic",
            "resilience": "Foundational",
            "off_grid": "Limited",
            "sensor_support": "Future-ready",
            "responder_integration": "Planned",
            "maintenance_support": "Basic plan",
            "upgrade_path": "V2 foundation",
        },
        "better": {
            "label": "BETTER",
            "badge": "Recommended",
            "automation": "Moderate",
            "resilience": "Enhanced",
            "off_grid": "Strong",
            "sensor_support": "V3-ready",
            "responder_integration": "Mapped access planning",
            "maintenance_support": "Enhanced plan",
            "upgrade_path": "V2 to V3 pathway",
        },
        "best": {
            "label": "BEST",
            "badge": "Maximum Resilience",
            "automation": "Advanced",
            "resilience": "Maximum",
            "off_grid": "Enterprise",
            "sensor_support": "V4 automation-ready",
            "responder_integration": "Full responder packet planning",
            "maintenance_support": "Premium plan",
            "upgrade_path": "V2 to V3 to V4 pathway",
        },
    }

    for key, scenario in multi_scenario_proposals.items():
        pricing = scenario.get("proposal_pricing", {})
        meta = metadata.get(key, {})

        matrix.append(
            {
                "scenario_key": key,
                "label": meta.get("label", key.upper()),
                "proposal_total": pricing.get("proposal_total", 0),
                "badge": meta.get("badge"),
                "automation_level": meta.get("automation"),
                "resilience_level": meta.get("resilience"),
                "off_grid_capability": meta.get("off_grid"),
                "sensor_support": meta.get("sensor_support"),
                "responder_integration": meta.get("responder_integration"),
                "maintenance_support": meta.get("maintenance_support"),
                "upgrade_path": meta.get("upgrade_path"),
            }
        )

    return matrix
