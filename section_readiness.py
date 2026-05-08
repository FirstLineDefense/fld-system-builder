def has_selected(value):
    return value not in [None, "", "None"] and not str(value).startswith("Auto Select")


def is_auto(value):
    return str(value).startswith("Auto Select")


def readiness_item(section, status, summary, suggested_inputs=None):
    return {
        "section": section,
        "status": status,
        "summary": summary,
        "suggested_inputs": suggested_inputs or []
    }


def analyze_section_readiness(input_data):
    branches = input_data.get("branches", [])

    active_branches = [b for b in branches if b.get("active")]

    active_devices = 0
    branches_missing_pipe = []
    branches_missing_devices = []
    branches_missing_length = []

    for branch in active_branches:
        branch_number = branch.get("branch_number")

        if not has_selected(branch.get("pipe_name")):
            branches_missing_pipe.append(branch_number)

        if float(branch.get("pipe_length_ft", 0)) <= 0:
            branches_missing_length.append(branch_number)

        branch_device_count = 0

        for device in branch.get("devices", []):
            if has_selected(device.get("name")) and int(device.get("quantity", 0)) > 0:
                branch_device_count += int(device.get("quantity", 0))

        if branch_device_count == 0:
            branches_missing_devices.append(branch_number)

        active_devices += branch_device_count

    sections = []

    # System Drive
    drive_suggestions = []

    if is_auto(input_data.get("pump_name")):
        pump_status = "yellow"
        drive_suggestions.append("Pump is set to Auto Select. The system can suggest a pump after hydraulic demand is defined.")
    elif has_selected(input_data.get("pump_name")):
        pump_status = "green"
    else:
        pump_status = "red"
        drive_suggestions.append("Select a pump or choose Auto Select Pump.")

    engine_or_motor_known = (
        has_selected(input_data.get("engine_name"))
        or has_selected(input_data.get("motor_name"))
        or is_auto(input_data.get("engine_name"))
        or is_auto(input_data.get("motor_name"))
    )

    if not engine_or_motor_known:
        drive_suggestions.append("Select engine, motor, or Auto Select for one of them.")

    if pump_status == "green" and engine_or_motor_known:
        drive_status = "green"
        drive_summary = "Enough drive-side information exists to evaluate the selected architecture."
    elif pump_status in ["green", "yellow"] or engine_or_motor_known:
        drive_status = "yellow"
        drive_summary = "Partial drive-side information exists. The system can continue, but more detail improves recommendations."
    else:
        drive_status = "red"
        drive_summary = "Not enough drive-side information exists yet."

    sections.append(readiness_item(
        "System Drive",
        drive_status,
        drive_summary,
        drive_suggestions
    ))

    # Water + Runtime
    water = float(input_data.get("available_water_gallons", 0))
    runtime = float(input_data.get("required_runtime_minutes", 0))

    water_suggestions = []

    if water <= 0:
        water_suggestions.append("Enter available water gallons.")

    if runtime <= 0:
        water_suggestions.append("Enter required runtime minutes.")

    if is_auto(input_data.get("water_storage_name")):
        water_suggestions.append("Water storage is set to Auto Select. The system can size storage from flow and runtime.")

    if water > 0 and runtime > 0:
        water_status = "green"
        water_summary = "Enough information exists to estimate runtime and water demand."
    elif water > 0 or runtime > 0 or is_auto(input_data.get("water_storage_name")):
        water_status = "yellow"
        water_summary = "Partial water/runtime information exists."
    else:
        water_status = "red"
        water_summary = "Water and runtime information are missing."

    sections.append(readiness_item(
        "Water + Runtime",
        water_status,
        water_summary,
        water_suggestions
    ))

    # Manifold + Branches
    branch_suggestions = []

    if not active_branches:
        branch_suggestions.append("Add at least one active branch.")

    if branches_missing_pipe:
        branch_suggestions.append(f"Select pipe for branches: {branches_missing_pipe}")

    if branches_missing_length:
        branch_suggestions.append(f"Enter pipe length for branches: {branches_missing_length}")

    if branches_missing_devices:
        branch_suggestions.append(f"Add devices/sprinklers to branches: {branches_missing_devices}")

    if active_branches and active_devices > 0 and not branches_missing_pipe and not branches_missing_length:
        branch_status = "green"
        branch_summary = "Enough branch information exists for hydraulic calculations."
    elif active_branches:
        branch_status = "yellow"
        branch_summary = "Branch layout has started, but some information is still missing."
    else:
        branch_status = "red"
        branch_summary = "No active hydraulic branch demand has been defined."

    sections.append(readiness_item(
        "Manifold + Branches",
        branch_status,
        branch_summary,
        branch_suggestions
    ))

    # Controls
    selected_controls = input_data.get("selected_controls", [])

    if selected_controls:
        controls_status = "green"
        controls_summary = "Control selections exist."
        controls_suggestions = []
    else:
        controls_status = "yellow"
        controls_summary = "Controls are optional for hydraulic calculation, but needed for proposal-grade system architecture."
        controls_suggestions = ["Select controls if this is moving toward a proposal or V2/V3 design."]

    sections.append(readiness_item(
        "Controls",
        controls_status,
        controls_summary,
        controls_suggestions
    ))

    # Sensors
    selected_sensors = input_data.get("selected_sensors", [])

    if selected_sensors:
        sensors_status = "green"
        sensors_summary = "Sensor selections exist."
        sensors_suggestions = []
    else:
        sensors_status = "yellow"
        sensors_summary = "Sensors are optional for basic hydraulic calculations, but important for V3/V4 architecture."
        sensors_suggestions = ["Select sensors if this design includes automated or environmental intelligence features."]

    sections.append(readiness_item(
        "Sensors",
        sensors_status,
        sensors_summary,
        sensors_suggestions
    ))

    # Budget
    budget = float(input_data.get("max_budget", 0))

    if budget > 0:
        budget_status = "green"
        budget_summary = "Budget is available for cost checking."
        budget_suggestions = []
    else:
        budget_status = "yellow"
        budget_summary = "Budget is missing. The system can calculate design performance, but cannot judge affordability."
        budget_suggestions = ["Enter a max budget if cost filtering matters."]

    sections.append(readiness_item(
        "Budget",
        budget_status,
        budget_summary,
        budget_suggestions
    ))

    counts = {
        "green": len([s for s in sections if s["status"] == "green"]),
        "yellow": len([s for s in sections if s["status"] == "yellow"]),
        "red": len([s for s in sections if s["status"] == "red"])
    }

    if counts["red"] > 0:
        overall = "red"
    elif counts["yellow"] > 0:
        overall = "yellow"
    else:
        overall = "green"

    return {
        "overall_status": overall,
        "counts": counts,
        "sections": sections
    }