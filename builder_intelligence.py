from component_library import get_component_library


def get_component_name(component):
    if component is None:
        return ""

    if isinstance(component, dict):
        return component.get("name", "")

    return getattr(component, "name", "")


def get_component_number(component, field_name, default=0):
    if component is None:
        return default

    if isinstance(component, dict):
        return float(component.get(field_name, default) or default)

    return float(getattr(component, field_name, default) or default)


def suggest_engine_from_hydraulics(primary):
    library = get_component_library()
    engines = library.get("engines", [])

    manifold = primary.get("manifold", {})

    flow_gpm = float(manifold.get("total_flow_gpm", 0) or 0)
    pressure_psi = float(manifold.get("pump_operating_pressure_psi", 0) or 0)

    if flow_gpm <= 0 or pressure_psi <= 0:
        return {
            "suggested_value": "",
            "confidence": "red",
            "reason": "Not enough hydraulic demand exists yet to estimate engine horsepower.",
            "auto_selected": False,
        }

    pump_efficiency = 0.60
    safety_factor = 1.25

    water_hp = (flow_gpm * pressure_psi) / 1714
    brake_hp = water_hp / pump_efficiency
    required_engine_hp = brake_hp * safety_factor

    best_engine = None
    best_engine_hp = None

    for engine in engines:
        hp = get_component_number(engine, "horsepower", 0)

        if hp <= 0:
            hp = get_component_number(engine, "hp", 0)

        if hp >= required_engine_hp:
            if best_engine is None or hp < best_engine_hp:
                best_engine = engine
                best_engine_hp = hp

    if best_engine:
        return {
            "suggested_value": get_component_name(best_engine),
            "confidence": "yellow",
            "reason": (
                f"Estimated hydraulic load is {round(flow_gpm, 1)} GPM at "
                f"{round(pressure_psi, 1)} PSI. That equals about "
                f"{round(water_hp, 1)} water HP. Using 60% pump efficiency "
                f"and a 1.25 safety factor, the estimated engine requirement "
                f"is about {round(required_engine_hp, 1)} HP. This is a preliminary "
                f"engine match and should be confirmed against pump curve, coupling, "
                f"fuel type, elevation, and duty cycle."
            ),
            "auto_selected": True,
        }

    return {
        "suggested_value": "",
        "confidence": "red",
        "reason": (
            f"Estimated engine requirement is about {round(required_engine_hp, 1)} HP, "
            "but no engine in the current library appears to meet that requirement. "
            "Add a larger engine option or reduce hydraulic demand."
        ),
        "auto_selected": False,
    }




def suggest_motor_from_hydraulics(primary):
    library = get_component_library()
    motors = library.get("motors", [])

    manifold = primary.get("manifold", {})

    flow_gpm = float(manifold.get("total_flow_gpm", 0) or 0)
    pressure_psi = float(manifold.get("pump_operating_pressure_psi", 0) or 0)

    if flow_gpm <= 0 or pressure_psi <= 0:
        return {
            "suggested_value": "",
            "confidence": "red",
            "reason": "Not enough hydraulic demand exists yet to estimate motor size.",
            "auto_selected": False,
        }

    pump_efficiency = 0.60
    safety_factor = 1.25

    water_hp = (flow_gpm * pressure_psi) / 1714
    brake_hp = water_hp / pump_efficiency
    required_hp = brake_hp * safety_factor
    required_kw = required_hp * 0.746

    best_motor = None
    best_motor_kw = None

    for motor in motors:
        kw = get_component_number(motor, "kw", 0)

        if kw <= 0:
            kw = get_component_number(motor, "kilowatts", 0)

        if kw <= 0:
            kw = get_component_number(motor, "power_kw", 0)

        if kw <= 0:
            hp = get_component_number(motor, "horsepower", 0)

            if hp <= 0:
                hp = get_component_number(motor, "hp", 0)

            kw = hp * 0.746

        if kw >= required_kw:
            if best_motor is None or kw < best_motor_kw:
                best_motor = motor
                best_motor_kw = kw

    if best_motor:
        return {
            "suggested_value": get_component_name(best_motor),
            "confidence": "yellow",
            "reason": (
                f"Estimated hydraulic load is {round(flow_gpm, 1)} GPM at "
                f"{round(pressure_psi, 1)} PSI. This creates an estimated "
                f"motor requirement of about {round(required_kw, 1)} kW "
                f"after pump efficiency and safety factor. This is a preliminary "
                f"electric-drive match and should be confirmed against pump coupling, "
                f"available electrical service, duty cycle, surge/start current, and backup power plan."
            ),
            "auto_selected": True,
        }

    return {
        "suggested_value": "",
        "confidence": "red",
        "reason": (
            f"Estimated motor requirement is about {round(required_kw, 1)} kW, "
            "but no motor in the current library appears to meet that requirement. "
            "Add a larger motor option, reduce hydraulic demand, or use an engine-driven architecture."
        ),
        "auto_selected": False,
    }


def build_builder_suggestions(input_data, result):
    suggestions = {}

    primary = result.get("primary", {})
    auto_selected = primary.get("auto_selected", {})

    pump = primary.get("pump")
    water_storage = primary.get("water_storage")

    branches = input_data.get("branches", [])

    has_branches = any(
        branch.get("active")
        for branch in branches
    )

    has_water = float(
        input_data.get("available_water_gallons", 0) or 0
    ) > 0

    has_runtime = float(
        input_data.get("required_runtime_minutes", 0) or 0
    ) > 0

    manifold = primary.get("manifold", {})

    if pump:
        confidence = "green"

        if not has_water or not has_runtime:
            confidence = "yellow"

        total_flow_gpm = float(manifold.get("total_flow_gpm", 0) or 0)
        pump_pressure_psi = float(
            manifold.get("pump_operating_pressure_psi", 0) or 0
        )
        failing_branch_count = int(
            manifold.get("failing_branch_count", 0) or 0
        )

        if failing_branch_count > 0:
            confidence = "yellow"

        suggestions["pump_name"] = {
            "suggested_value": get_component_name(pump),
            "confidence": confidence,
            "reason": (
                f"The builder selected this pump from the current hydraulic demand: "
                f"{round(total_flow_gpm, 1)} GPM at approximately "
                f"{round(pump_pressure_psi, 1)} PSI. "
                f"Failing branches: {failing_branch_count}. "
                f"Confidence is lower if any branch or operating mode still fails."
            ),
            "auto_selected": auto_selected.get("pump", False),
        }

    else:
        suggestions["pump_name"] = {
            "suggested_value": "",
            "confidence": "red",
            "reason": "Not enough information to recommend a pump yet.",
            "auto_selected": False,
        }

    suggestions["engine_name"] = suggest_engine_from_hydraulics(primary)

    suggestions["motor_name"] = suggest_motor_from_hydraulics(primary)

    if suggestions["engine_name"].get("suggested_value"):
        suggestions["fuel_storage_name"] = {
            "suggested_value": "500 Gallon Propane Tank",
            "confidence": "yellow",
            "reason": "Fuel storage estimated from preliminary engine-driven runtime assumptions.",
            "auto_selected": True,
        }

    else:
        suggestions["fuel_storage_name"] = {
            "suggested_value": "",
            "confidence": "red",
            "reason": "No engine suggestion exists yet, so fuel storage cannot be estimated.",
            "auto_selected": False,
        }

    suggestions["generator_name"] = {
        "suggested_value": "",
        "confidence": "red",
        "reason": "Generator recommendations not yet implemented.",
        "auto_selected": False,
    }

    suggestions["battery_name"] = {
        "suggested_value": "",
        "confidence": "red",
        "reason": "Battery recommendations not yet implemented.",
        "auto_selected": False,
    }

    required_runtime_minutes = float(
        input_data.get("required_runtime_minutes", 0) or 0
    )

    manifold = primary.get("manifold", {})
    total_flow_gpm = float(manifold.get("total_flow_gpm", 0) or 0)

    required_water_gallons = total_flow_gpm * required_runtime_minutes

    if required_water_gallons > 0:
        library = get_component_library()
        water_options = library.get("water_storage", [])

        best_water_storage = None
        best_capacity = None

        for option in water_options:
            capacity = get_component_number(
                option,
                "capacity_gallons",
                0
            )

            if capacity <= 0:
                capacity = get_component_number(
                    option,
                    "gallons",
                    0
                )

            if capacity >= required_water_gallons:
                if best_water_storage is None or capacity < best_capacity:
                    best_water_storage = option
                    best_capacity = capacity

        if best_water_storage:
            suggestions["water_storage_name"] = {
                "suggested_value": get_component_name(best_water_storage),
                "confidence": "green",
                "reason": (
                    f"Estimated water demand is {round(total_flow_gpm, 1)} GPM "
                    f"for {round(required_runtime_minutes, 1)} minutes, requiring "
                    f"about {round(required_water_gallons, 0)} gallons. The suggested "
                    f"storage option is the smallest available tank that meets or exceeds "
                    f"that demand."
                ),
                "auto_selected": True,
            }

        else:
            suggestions["water_storage_name"] = {
                "suggested_value": "",
                "confidence": "red",
                "reason": (
                    f"Estimated water demand is {round(required_water_gallons, 0)} gallons, "
                    "but no water storage option in the current library meets that requirement. "
                    "Add a larger tank option, reduce active flow, reduce simultaneous zones, "
                    "or reduce runtime target."
                ),
                "auto_selected": False,
            }

    else:
        suggestions["water_storage_name"] = {
            "suggested_value": "",
            "confidence": "red",
            "reason": (
                "Not enough flow/runtime information exists yet to recommend water storage."
            ),
            "auto_selected": False,
        }


    selected_controls = input_data.get("selected_controls", [])

    if selected_controls:
        suggestions["selected_controls"] = {
            "suggested_value": "",
            "confidence": "green",
            "reason": "Control selections already exist.",
            "auto_selected": False,
        }

    else:
        suggestions["selected_controls"] = {
            "suggested_value": "Automation Ready Control Panel",
            "confidence": "yellow",
            "reason": "A control panel is recommended once hydraulic demand exists.",
            "auto_selected": True,
        }

    selected_sensors = input_data.get("selected_sensors", [])

    if selected_sensors:
        suggestions["selected_sensors"] = {
            "suggested_value": "",
            "confidence": "green",
            "reason": "Sensor selections already exist.",
            "auto_selected": False,
        }

    else:
        suggestions["selected_sensors"] = {
            "suggested_value": "Tank Level Sensor",
            "confidence": "yellow",
            "reason": "A tank level sensor is recommended once water/runtime planning exists.",
            "auto_selected": True,
        }

    branch_suggestions = []

    branch_results = manifold.get("branch_results", [])

    for branch_result in branch_results:
        branch_number = branch_result.get("branch_number", "")
        passed = branch_result.get("passed", False)
        margin = float(branch_result.get("pressure_margin_psi", 0) or 0)
        final_psi = float(branch_result.get("final_pressure_psi", 0) or 0)
        required_psi = float(branch_result.get("required_pressure_psi", 0) or 0)
        velocity = float(branch_result.get("velocity_fps", 0) or 0)
        pipe_name = branch_result.get("pipe_name", "")

        if passed:
            confidence = "green"
            title = f"Branch {branch_number} passes"
            reason = (
                f"Branch {branch_number} currently passes with "
                f"{round(margin, 1)} PSI pressure margin using {pipe_name}."
            )
        else:
            confidence = "red"
            title = f"Branch {branch_number} needs work"
            reason = (
                f"Branch {branch_number} does not pass. Final pressure is "
                f"{round(final_psi, 1)} PSI, required pressure is "
                f"{round(required_psi, 1)} PSI, and pressure margin is "
                f"{round(margin, 1)} PSI. Consider upsizing pipe, reducing device demand, "
                f"reducing simultaneous branches, reducing elevation penalty, or selecting "
                f"a stronger pump."
            )

        if velocity > 8:
            confidence = "yellow" if passed else "red"
            reason += (
                f" Velocity is {round(velocity, 1)} ft/s, which is above the preferred target."
            )

        action_code = ""
        action_label = ""

        if not passed:
            action_code = f"UPSIZE_BRANCH_PIPE:{branch_number}"
            action_label = "Suggest Pipe Upsize"

        branch_suggestions.append({
            "branch_number": branch_number,
            "confidence": confidence,
            "title": title,
            "reason": reason,
            "action_code": action_code,
            "action_label": action_label,
        })

    if has_branches:
        suggestions["manifold_branches"] = {
            "confidence": "green",
            "reason": "Branch information exists and can drive hydraulic calculations.",
            "branch_suggestions": branch_suggestions,
        }

    else:
        suggestions["manifold_branches"] = {
            "confidence": "red",
            "reason": "No active branches defined yet.",
            "branch_suggestions": [],
        }

    return suggestions
