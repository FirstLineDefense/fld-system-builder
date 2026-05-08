def estimate_runtime(input_data, flow_result):
    """
    Estimates water runtime based on available water and total flow.
    Adds a pass/fail check against required runtime.
    """

    total_flow_gpm = flow_result.get("total_flow_gpm", 0)
    available_water_gallons = input_data.get("available_water_gallons", 0)
    required_runtime_minutes = input_data.get("required_runtime_minutes", 60)

    if total_flow_gpm <= 0:
        return {
            "available_water_gallons": available_water_gallons,
            "total_flow_gpm": total_flow_gpm,
            "runtime_minutes": None,
            "runtime_hours": None,
            "required_runtime_minutes": required_runtime_minutes,
            "runtime_margin_minutes": None,
            "passed_runtime_check": False,
            "warnings": ["Cannot calculate runtime because total flow is zero."]
        }

    runtime_minutes = available_water_gallons / total_flow_gpm
    runtime_hours = runtime_minutes / 60
    runtime_margin_minutes = runtime_minutes - required_runtime_minutes

    warnings = []

    if runtime_minutes < required_runtime_minutes:
        warnings.append("Water runtime is below required runtime.")

    return {
        "available_water_gallons": available_water_gallons,
        "total_flow_gpm": total_flow_gpm,
        "runtime_minutes": runtime_minutes,
        "runtime_hours": runtime_hours,
        "required_runtime_minutes": required_runtime_minutes,
        "runtime_margin_minutes": runtime_margin_minutes,
        "passed_runtime_check": runtime_minutes >= required_runtime_minutes,
        "warnings": warnings,
        "notes": "Water runtime = available water divided by total flow."
    }