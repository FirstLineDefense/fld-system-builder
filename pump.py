def select_pump(input_data, flow_result, pressure_result, component_library):
    """
    Selects the lowest-cost pump from the component library that can meet:
    - required total flow
    - required total pump pressure

    Required pump pressure includes:
    - required terminal pressure
    - static pressure from elevation
    - pipe friction pressure
    """

    required_flow = flow_result.get("total_flow_gpm", 0)

    required_terminal_pressure = pressure_result.get("required_terminal_pressure_psi", 0)
    static_pressure = pressure_result.get("static_pressure_psi", 0)
    pipe_friction = pressure_result.get("pipe_friction_psi", 0)

    required_pump_pressure = required_terminal_pressure + static_pressure + pipe_friction

    available_pumps = component_library.get("pumps", [])
    passing_pumps = []

    for pump in available_pumps:
        flow_ok = pump.max_flow_gpm >= required_flow
        pressure_ok = pump.max_pressure_psi >= required_pump_pressure

        if flow_ok and pressure_ok:
            passing_pumps.append(pump)

    if not passing_pumps:
        return {
            "selected_pump": None,
            "passed_pump_check": False,
            "warnings": [
                "No pump in the component library can meet the required flow and total system pressure."
            ],
            "required_flow_gpm": required_flow,
            "required_terminal_pressure_psi": required_terminal_pressure,
            "static_pressure_psi": static_pressure,
            "pipe_friction_psi": pipe_friction,
            "required_pump_pressure_psi": required_pump_pressure
        }

    selected_pump = min(passing_pumps, key=lambda pump: pump.unit_cost)

    return {
        "selected_pump": selected_pump,
        "passed_pump_check": True,
        "warnings": [],
        "required_flow_gpm": required_flow,
        "required_terminal_pressure_psi": required_terminal_pressure,
        "static_pressure_psi": static_pressure,
        "pipe_friction_psi": pipe_friction,
        "required_pump_pressure_psi": required_pump_pressure
    }