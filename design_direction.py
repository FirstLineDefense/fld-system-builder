def has_selected(value):
    return value not in [None, "", "None"]


def count_active_branches(branches):
    return len([branch for branch in branches if branch.get("active")])


def count_active_devices(branches):
    total = 0

    for branch in branches:
        if not branch.get("active"):
            continue

        for device in branch.get("devices", []):
            if has_selected(device.get("name")):
                total += int(device.get("quantity", 0))

    return total


def count_selected_pipe_branches(branches):
    return len([
        branch for branch in branches
        if branch.get("active") and has_selected(branch.get("pipe_name"))
    ])


def analyze_design_direction(input_data):
    branches = input_data.get("branches", [])

    active_branch_count = count_active_branches(branches)
    active_device_count = count_active_devices(branches)
    pipe_branch_count = count_selected_pipe_branches(branches)

    has_engine = has_selected(input_data.get("engine_name"))
    has_motor = has_selected(input_data.get("motor_name"))
    has_drive = has_engine or has_motor

    has_water = float(input_data.get("available_water_gallons", 0)) > 0
    has_runtime = float(input_data.get("required_runtime_minutes", 0)) > 0

    has_hydraulic_demand = active_branch_count > 0 and active_device_count > 0
    has_pipe_layout = active_branch_count > 0 and pipe_branch_count == active_branch_count
    has_supply_architecture = has_drive
    has_runtime_target = has_water and has_runtime

    if has_supply_architecture and has_hydraulic_demand and has_pipe_layout:
        direction = "validate_known_system"
        summary = "You have selected a supply architecture and enough branch demand to validate whether this system works."
        next_action = "Run hydraulic validation, review warnings, then optimize pipe sizing and staging."

    elif has_hydraulic_demand and not has_supply_architecture:
        direction = "demand_to_supply"
        summary = "You have defined sprinkler/zone demand, but not the supply architecture."
        next_action = "Use active flow, pressure, pipe losses, and runtime targets to recommend pump, engine or motor, water, fuel, and power requirements."

    elif has_supply_architecture and not has_hydraulic_demand:
        direction = "supply_to_demand"
        summary = "You have selected part of the supply system, but not enough sprinkler/zone demand."
        next_action = "Define active branches, sprinkler devices, pipe length, and elevation so the tool can determine what the selected pump/drive can realistically support."

    elif active_branch_count > 0:
        direction = "partial_branch_layout"
        summary = "You have started defining branches, but the hydraulic demand is incomplete."
        next_action = "Add pipe selections and sprinkler/device quantities for each active branch."

    else:
        direction = "concept_start"
        summary = "The design is still at concept stage."
        next_action = "Start by defining either the supply side or the demand side: pump/engine first, or zones/sprinklers first."

    missing = []

    if not has_hydraulic_demand:
        missing.append("Active branches with sprinkler/device quantities")

    if active_branch_count > 0 and not has_pipe_layout:
        missing.append("Pipe selection for every active branch")

    if not has_supply_architecture:
        missing.append("Engine or motor selection")

    if not has_runtime_target:
        missing.append("Available water and required runtime")

    return {
        "direction": direction,
        "summary": summary,
        "next_action": next_action,
        "active_branch_count": active_branch_count,
        "active_device_count": active_device_count,
        "pipe_branch_count": pipe_branch_count,
        "has_hydraulic_demand": has_hydraulic_demand,
        "has_pipe_layout": has_pipe_layout,
        "has_supply_architecture": has_supply_architecture,
        "has_runtime_target": has_runtime_target,
        "missing": missing
    }