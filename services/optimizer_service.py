def get_pump_recommendation(project):
    required_psi = project.get("required_pump_psi", 0)
    hydraulic_hp = project.get("hydraulic_hp", 0)

    if required_psi >= 140 or hydraulic_hp >= 20:
        return {
            "tier": "High-output pump package",
            "notes": "Current estimate suggests a stronger pump package is likely needed because pressure and HP demand are high.",
        }

    return {
        "tier": "Standard pump package",
        "notes": "Current estimate appears within a moderate operating range.",
    }
