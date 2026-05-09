from component_library import get_component_library
from cost import estimate_cost_from_components
from branches import calculate_manifold, find_component_by_name
from hydraulic_intelligence import analyze_hydraulic_intelligence
from hydraulic_optimizer import optimize_hydraulic_design
from design_readiness import analyze_design_readiness
from design_direction import analyze_design_direction
from architecture_recommendations import analyze_architecture_recommendations
from bottleneck_intelligence import analyze_bottleneck_intelligence
from section_readiness import analyze_section_readiness
from design_maturity import evaluate_design_maturity
from design_maturity_v2 import evaluate_design_maturity_v2
from engineering_recommendations import generate_engineering_recommendations
from recommendation_actions import attach_recommendation_actions
from auto_update_actions import apply_auto_update_action
from builder_intelligence import build_builder_suggestions

def is_auto_select(value):
    if value is None:
        return False

    return str(value).startswith("Auto Select")

def add_optional_component(selected_components, library, category, selected_name, quantity=1):
    if is_auto_select(selected_name):
        return None

    component = find_component_by_name(library.get(category, []), selected_name)

    if component and quantity > 0:
        selected_components.append({
            "component": component,
            "quantity": quantity
        })

    return component


def add_multiple_components(selected_components, library, category, selected_items):
    selected = []

    for item in selected_items:
        name = item.get("name")
        quantity = int(item.get("quantity", 0))

        component = find_component_by_name(library.get(category, []), name)

        if component and quantity > 0:
            selected_components.append({
                "component": component,
                "quantity": quantity
            })

            selected.append({
                "component": component,
                "quantity": quantity
            })

    return selected


def add_branch_components(selected_components, library, branches):
    pipe_totals = {}
    device_totals = {}

    for branch in branches:
        if not branch.get("active"):
            continue

        pipe_name = branch.get("pipe_name")
        pipe_length = float(branch.get("pipe_length_ft", 0))

        if pipe_name and pipe_name != "None" and pipe_length > 0:
            pipe_totals[pipe_name] = pipe_totals.get(pipe_name, 0) + pipe_length

        for device_line in branch.get("devices", []):
            device_name = device_line.get("name")
            quantity = int(device_line.get("quantity", 0))

            if device_name and device_name != "None" and quantity > 0:
                device_totals[device_name] = device_totals.get(device_name, 0) + quantity

    for pipe_name, length in pipe_totals.items():
        pipe = find_component_by_name(library.get("pipes", []), pipe_name)
        if pipe:
            selected_components.append({
                "component": pipe,
                "quantity": length
            })

    for device_name, quantity in device_totals.items():
        device = find_component_by_name(library.get("devices", []), device_name)
        if device:
            selected_components.append({
                "component": device,
                "quantity": quantity
            })


def select_best_pump_for_manifold(input_data, library):
    pumps = library.get("pumps", [])
    branches = input_data.get("branches", [])
    minimum_pressure_margin_psi = input_data.get("minimum_pressure_margin_psi", 10)
    max_simultaneous_ports = int(input_data.get("max_simultaneous_ports", 1))
    selected_pump_name = input_data.get("pump_name", "Auto Select Pump")

    if selected_pump_name and selected_pump_name not in ["None", "Auto Select Pump"]:
        selected_pump = find_component_by_name(pumps, selected_pump_name)

        if not selected_pump:
            return {
                "pump": None,
                "manifold": None,
                "passed": False,
                "warnings": [f"Selected pump '{selected_pump_name}' was not found in the component library."]
            }

        manifold = calculate_manifold(
            branches,
            selected_pump,
            library,
            minimum_pressure_margin_psi,
            max_simultaneous_ports
        )

        flow_ok = selected_pump.max_flow_gpm >= manifold["total_flow_gpm"]
        passed = flow_ok and manifold["passed"]

        warnings = []

        if not passed:
            warnings.extend(manifold.get("warnings", []))

        if not flow_ok:
            warnings.append("Selected pump does not meet total active operating flow requirement.")

        return {
            "pump": selected_pump,
            "manifold": manifold,
            "passed": passed,
            "warnings": warnings
        }

    candidates = []

    for pump in pumps:
        manifold = calculate_manifold(
            branches,
            pump,
            library,
            minimum_pressure_margin_psi,
            max_simultaneous_ports
        )

        flow_ok = pump.max_flow_gpm >= manifold["total_flow_gpm"]
        passed = flow_ok and manifold["passed"]

        candidates.append({
            "pump": pump,
            "manifold": manifold,
            "flow_ok": flow_ok,
            "passed": passed,
            "score": pump.unit_cost
        })

    passing = [c for c in candidates if c["passed"]]

    if passing:
        selected = min(passing, key=lambda c: c["score"])
        return {
            "pump": selected["pump"],
            "manifold": selected["manifold"],
            "passed": True,
            "warnings": ["Pump was auto-selected as the lowest-cost passing pump."]
        }

    if not candidates:
        return {
            "pump": None,
            "manifold": None,
            "passed": False,
            "warnings": ["No pumps available in component library."]
        }

    best_available = max(
        candidates,
        key=lambda c: (
            c["flow_ok"],
            c["manifold"]["operating_modes"]["last_line_passed"],
            c["manifold"]["passing_branch_count"],
            c["manifold"]["total_flow_gpm"]
        )
    )

    warnings = ["No pump passed all manifold operating-mode requirements. Selected best available pump."]

    if not best_available["flow_ok"]:
        warnings.append("Selected pump does not meet total active operating flow requirement.")

    warnings.extend(best_available["manifold"]["warnings"])

    return {
        "pump": best_available["pump"],
        "manifold": best_available["manifold"],
        "passed": False,
        "warnings": warnings
    }


def analyze_fuel_runtime(input_data, selected_engine, selected_fuel_storage):
    required_runtime_hours = input_data.get("required_runtime_minutes", 0) / 60

    if not selected_engine or not selected_fuel_storage:
        return {
            "passed": None,
            "runtime_hours": None,
            "required_runtime_hours": required_runtime_hours,
            "warnings": []
        }

    if selected_engine.fuel_type != selected_fuel_storage.fuel_type:
        return {
            "passed": False,
            "runtime_hours": 0,
            "required_runtime_hours": required_runtime_hours,
            "warnings": ["Engine fuel type does not match selected fuel storage."]
        }

    if selected_engine.fuel_burn_gph <= 0:
        return {
            "passed": False,
            "runtime_hours": 0,
            "required_runtime_hours": required_runtime_hours,
            "warnings": ["Engine fuel burn rate is missing or invalid."]
        }

    runtime_hours = selected_fuel_storage.capacity_gallons / selected_engine.fuel_burn_gph
    passed = runtime_hours >= required_runtime_hours

    warnings = []
    if not passed:
        warnings.append("Fuel storage does not support required runtime.")

    return {
        "passed": passed,
        "runtime_hours": runtime_hours,
        "required_runtime_hours": required_runtime_hours,
        "warnings": warnings
    }


def analyze_battery_runtime(input_data, selected_motor, selected_battery):
    required_runtime_hours = input_data.get("required_runtime_minutes", 0) / 60

    if not selected_motor or not selected_battery:
        return {
            "passed": None,
            "runtime_hours": None,
            "required_runtime_hours": required_runtime_hours,
            "motor_kw_required": None,
            "warnings": []
        }

    efficiency = selected_motor.efficiency if selected_motor.efficiency > 0 else 0.9
    motor_kw_required = selected_motor.horsepower * 0.746 / efficiency
    usable_kwh = selected_battery.capacity_kwh * selected_battery.usable_fraction

    runtime_hours = usable_kwh / motor_kw_required if motor_kw_required > 0 else 0
    passed = runtime_hours >= required_runtime_hours

    warnings = []
    if not passed:
        warnings.append("Battery capacity does not support required runtime.")

    return {
        "passed": passed,
        "runtime_hours": runtime_hours,
        "required_runtime_hours": required_runtime_hours,
        "motor_kw_required": motor_kw_required,
        "warnings": warnings
    }


def analyze_generator_support(selected_motor, selected_generator):
    if not selected_motor or not selected_generator:
        return {
            "passed": None,
            "motor_kw_required": None,
            "generator_kw": None,
            "warnings": []
        }

    efficiency = selected_motor.efficiency if selected_motor.efficiency > 0 else 0.9
    motor_kw_required = selected_motor.horsepower * 0.746 / efficiency
    generator_kw = selected_generator.continuous_kw
    passed = generator_kw >= motor_kw_required

    warnings = []
    if not passed:
        warnings.append("Generator continuous kW is below motor estimated running requirement.")

    return {
        "passed": passed,
        "motor_kw_required": motor_kw_required,
        "generator_kw": generator_kw,
        "warnings": warnings
    }

def auto_select_water_storage(input_data, library, total_flow_gpm):
    selected_name = input_data.get("water_storage_name")

    if selected_name != "Auto Select Water Storage":
        return find_component_by_name(
            library.get("water_storage", []),
            selected_name
        )

    required_runtime_minutes = float(
        input_data.get("required_runtime_minutes", 0)
    )

    required_gallons = total_flow_gpm * required_runtime_minutes

    candidates = []

    for tank in library.get("water_storage", []):
        if tank.capacity_gallons >= required_gallons:
            candidates.append(tank)

    if candidates:
        return min(candidates, key=lambda tank: tank.capacity_gallons)

    if library.get("water_storage"):
        return max(
            library.get("water_storage", []),
            key=lambda tank: tank.capacity_gallons
        )

    return None

def analyze_water_storage(input_data, selected_water_storage, total_flow_gpm):
    required_runtime_minutes = float(input_data.get("required_runtime_minutes", 0))
    required_gallons = total_flow_gpm * required_runtime_minutes

    available_water_gallons = float(input_data.get("available_water_gallons", 0))

    capacity_gallons = available_water_gallons

    if selected_water_storage:
        capacity_gallons = max(
            available_water_gallons,
            float(getattr(selected_water_storage, "capacity_gallons", 0))
        )

    margin_gallons = capacity_gallons - required_gallons
    passed = capacity_gallons >= required_gallons if required_gallons > 0 else None

    warnings = []

    if required_gallons > 0 and not passed:
        warnings.append("Water storage does not meet required runtime demand.")

    return {
        "passed": passed,
        "capacity_gallons": capacity_gallons,
        "required_gallons": required_gallons,
        "margin_gallons": margin_gallons,
        "warnings": warnings
    }

def evaluate_system(input_data, library):
    pump_selection = select_best_pump_for_manifold(input_data, library)
    selected_pump = pump_selection["pump"]
    manifold = pump_selection["manifold"]

    selected_components = []

    if selected_pump:
        selected_components.append({
            "component": selected_pump,
            "quantity": 1
        })

    add_branch_components(
        selected_components,
        library,
        input_data.get("branches", [])
    )

    total_flow_gpm = manifold["total_flow_gpm"] if manifold else 0

    selected_engine = add_optional_component(selected_components, library, "engines", input_data.get("engine_name"))
    selected_motor = add_optional_component(selected_components, library, "motors", input_data.get("motor_name"))

    selected_water_storage = auto_select_water_storage(
        input_data,
        library,
        total_flow_gpm
    )

    if selected_water_storage:
        selected_components.append({
            "component": selected_water_storage,
            "quantity": 1
        })

    selected_fuel_storage = add_optional_component(selected_components, library, "fuel_storage", input_data.get("fuel_storage_name"))
    selected_battery = add_optional_component(selected_components, library, "batteries", input_data.get("battery_name"))
    selected_generator = add_optional_component(selected_components, library, "generators", input_data.get("generator_name"))

    selected_controls = add_multiple_components(
        selected_components,
        library,
        "controls",
        input_data.get("selected_controls", [])
    )

    selected_sensors = add_multiple_components(
        selected_components,
        library,
        "sensors",
        input_data.get("selected_sensors", [])
    )

    cost = estimate_cost_from_components(selected_components)

    runtime_minutes = 0

    if total_flow_gpm > 0:
        runtime_minutes = input_data.get("available_water_gallons", 0) / total_flow_gpm

    runtime_passed = runtime_minutes >= input_data.get("required_runtime_minutes", 0)

    water_storage_analysis = analyze_water_storage(input_data, selected_water_storage, total_flow_gpm)
    fuel_runtime_analysis = analyze_fuel_runtime(input_data, selected_engine, selected_fuel_storage)
    battery_runtime_analysis = analyze_battery_runtime(input_data, selected_motor, selected_battery)
    generator_analysis = analyze_generator_support(selected_motor, selected_generator)

    system_warnings = []
    system_warnings.extend(pump_selection["warnings"])

    if not runtime_passed:
        system_warnings.append("Water runtime is below required runtime.")

    system_warnings.extend(water_storage_analysis["warnings"])
    system_warnings.extend(fuel_runtime_analysis["warnings"])
    system_warnings.extend(battery_runtime_analysis["warnings"])
    system_warnings.extend(generator_analysis["warnings"])

    max_budget = input_data.get("max_budget", None)
    total_cost = cost["total_cost"]

    if max_budget is None:
        within_budget = None
        budget_margin = None
    else:
        within_budget = total_cost <= max_budget
        budget_margin = max_budget - total_cost

        if not within_budget:
            system_warnings.append("Selected system exceeds budget.")

    system_passed = (
        pump_selection["passed"]
        and runtime_passed
        and within_budget is not False
        and water_storage_analysis["passed"] is not False
        and fuel_runtime_analysis["passed"] is not False
        and battery_runtime_analysis["passed"] is not False
        and generator_analysis["passed"] is not False
    )

    summary = {
        "system_passed": system_passed,
        "runtime_passed": runtime_passed,
        "selection_passed": pump_selection["passed"],
        "within_budget": within_budget,
        "budget_margin": budget_margin,
        "warning_count": len(system_warnings),
        "warnings": system_warnings
    }

    runtime = {
        "runtime_minutes": runtime_minutes,
        "runtime_hours": runtime_minutes / 60 if runtime_minutes else 0,
        "required_runtime_minutes": input_data.get("required_runtime_minutes", 0),
        "passed_runtime_check": runtime_passed
    }

    system_result = {
        "summary": summary,
        "pump": selected_pump,
        "manifold": manifold,
        "runtime": runtime,
        "cost": cost,
        "selected_components": selected_components,
        "engine": selected_engine,
        "motor": selected_motor,
        "water_storage": selected_water_storage,
        "fuel_storage": selected_fuel_storage,
        "battery": selected_battery,
        "generator": selected_generator,
        "controls": selected_controls,
        "sensors": selected_sensors,
        "water_storage_analysis": water_storage_analysis,
        "fuel_runtime_analysis": fuel_runtime_analysis,
        "battery_runtime_analysis": battery_runtime_analysis,
        "generator_analysis": generator_analysis,
        "available_pipes": library.get("pipes", []),
        "auto_selected": {
            "pump": input_data.get("pump_name") == "Auto Select Pump",
            "water_storage": input_data.get("water_storage_name") == "Auto Select Water Storage",
            "engine": str(input_data.get("engine_name", "")).startswith("Auto Select"),
            "motor": str(input_data.get("motor_name", "")).startswith("Auto Select"),
            "fuel_storage": str(input_data.get("fuel_storage_name", "")).startswith("Auto Select"),
            "battery": str(input_data.get("battery_name", "")).startswith("Auto Select"),
            "generator": str(input_data.get("generator_name", "")).startswith("Auto Select")
        }
    }

    system_result["design_direction"] = analyze_design_direction(input_data)
    system_result["design_readiness"] = analyze_design_readiness(input_data)
    system_result["section_readiness"] = analyze_section_readiness(input_data)
    system_result["hydraulic_intelligence"] = analyze_hydraulic_intelligence(system_result)

    system_result["hydraulic_optimizer"] = optimize_hydraulic_design(
        input_data,
        library,
        selected_pump,
        manifold
    )

    system_result["architecture_recommendations"] = (
        analyze_architecture_recommendations(system_result)
    )

    system_result["bottleneck_intelligence"] = (
        analyze_bottleneck_intelligence(system_result)
    )

    return system_result


from design_maturity import evaluate_design_maturity


def run_system(input_data):
    library = get_component_library()

    primary = evaluate_system(input_data, library)

    design_maturity = evaluate_design_maturity_v2(
        input_data=input_data,
        primary=primary
    )

    engineering_recommendations = generate_engineering_recommendations(
        input_data=input_data,
        primary=primary,
        design_maturity=design_maturity
    )

    engineering_recommendations = attach_recommendation_actions(
        engineering_recommendations
    )

    builder_suggestions = build_builder_suggestions(
        input_data=input_data,
        result={
            "primary": primary,
            "design_maturity": design_maturity,
            "engineering_recommendations": engineering_recommendations
        }
    )

    try:
        from pump_curve import get_pump_curve_points
        if primary.get("pump"):
            primary["pump_curve_analysis"] = get_pump_curve_points(primary.get("pump"))
    except Exception as e:
        primary["pump_curve_analysis"] = {
            "curve_source": "curve_analysis_error",
            "curve_points": [],
            "validation_warnings": [str(e)]
        }

    return {
        "primary": primary,
        "scenarios": [],
        "design_maturity": design_maturity,
        "engineering_recommendations": engineering_recommendations,
        "builder_suggestions": builder_suggestions
    }



def run_auto_update(input_data, action_code):
    update_result = apply_auto_update_action(
        input_data=input_data,
        action_code=action_code
    )

    updated_input_data = update_result.get("updated_input_data", input_data)

    recalculated_result = run_system(updated_input_data)

    return {
        "success": update_result.get("success", False),
        "changes": update_result.get("changes", []),
        "updated_input_data": updated_input_data,
        "result": recalculated_result
    }

if __name__ == "__main__":
    sample_input = {
        "branches": [
            {
                "branch_number": 1,
                "active": True,
                "role": "last_line",
                "priority": 1,
                "pipe_name": '2" PVC',
                "pipe_length_ft": 200,
                "elevation_change_ft": 100,
                "devices": [
                    {"name": "Sprinkler Standard", "quantity": 3}
                ]
            }
        ],
        "available_water_gallons": 5000,
        "required_runtime_minutes": 60,
        "minimum_pressure_margin_psi": 20,
        "max_simultaneous_ports": 1,
        "max_budget": 4000
    }

    result = run_system(sample_input)
    print(result)
