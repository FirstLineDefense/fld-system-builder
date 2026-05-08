def has_selected(value):
    return value not in [None, "", "None"]


def count_active_branches(branches):
    return len([branch for branch in branches if branch.get("active")])


def count_active_devices(branches):
    count = 0

    for branch in branches:
        if not branch.get("active"):
            continue

        for device in branch.get("devices", []):
            quantity = int(device.get("quantity", 0))
            if has_selected(device.get("name")) and quantity > 0:
                count += quantity

    return count


def active_branches_missing_pipe(branches):
    missing = []

    for branch in branches:
        if not branch.get("active"):
            continue

        if not has_selected(branch.get("pipe_name")):
            missing.append(branch.get("branch_number"))

    return missing


def active_branches_missing_devices(branches):
    missing = []

    for branch in branches:
        if not branch.get("active"):
            continue

        branch_has_device = False

        for device in branch.get("devices", []):
            quantity = int(device.get("quantity", 0))
            if has_selected(device.get("name")) and quantity > 0:
                branch_has_device = True

        if not branch_has_device:
            missing.append(branch.get("branch_number"))

    return missing


def has_last_line_branch(branches):
    for branch in branches:
        if not branch.get("active"):
            continue

        if branch.get("role") in ["last_line", "structure_eaves"]:
            return True

    return False


def readiness_item(name, status, message, missing=None):
    return {
        "name": name,
        "status": status,
        "message": message,
        "missing": missing or []
    }


def analyze_design_readiness(input_data):
    branches = input_data.get("branches", [])

    active_branch_count = count_active_branches(branches)
    active_device_count = count_active_devices(branches)

    missing_pipe_branches = active_branches_missing_pipe(branches)
    missing_device_branches = active_branches_missing_devices(branches)

    pump_known = False
    engine_or_motor_known = (
        has_selected(input_data.get("engine_name"))
        or has_selected(input_data.get("motor_name"))
    )

    water_known = float(input_data.get("available_water_gallons", 0)) > 0
    runtime_known = float(input_data.get("required_runtime_minutes", 0)) > 0

    fuel_known = has_selected(input_data.get("fuel_storage_name"))
    battery_known = has_selected(input_data.get("battery_name"))
    generator_known = has_selected(input_data.get("generator_name"))

    items = []

    if active_branch_count > 0 and not missing_pipe_branches and not missing_device_branches:
        items.append(readiness_item(
            "Branch hydraulic calculation",
            "ready",
            "Enough information exists to calculate branch flow, velocity, friction loss, and pressure."
        ))
    else:
        missing = []

        if active_branch_count == 0:
            missing.append("At least one active branch")

        if missing_pipe_branches:
            missing.append(f"Pipe selection for branches: {missing_pipe_branches}")

        if missing_device_branches:
            missing.append(f"Device selection for branches: {missing_device_branches}")

        items.append(readiness_item(
            "Branch hydraulic calculation",
            "missing",
            "Branch hydraulics are not meaningful yet.",
            missing
        ))

    if active_branch_count > 0 and active_device_count > 0:
        items.append(readiness_item(
            "Pipe sizing recommendation",
            "ready",
            "Enough information exists to recommend pipe sizing and flag excessive velocity."
        ))
    else:
        items.append(readiness_item(
            "Pipe sizing recommendation",
            "missing",
            "Pipe recommendations need active branches with selected devices.",
            ["Active branches", "Selected sprinklers/devices"]
        ))

    if active_branch_count > 0 and active_device_count > 0:
        items.append(readiness_item(
            "Pump recommendation",
            "ready",
            "Enough demand information exists to compare pumps against required flow and pressure."
        ))
    else:
        items.append(readiness_item(
            "Pump recommendation",
            "missing",
            "Pump recommendation needs known hydraulic demand first.",
            ["Active branches", "Selected sprinklers/devices", "Pipe lengths/elevation"]
        ))

    if engine_or_motor_known:
        items.append(readiness_item(
            "Drive system check",
            "ready",
            "Engine or motor selection exists, so drive-side feasibility can be checked."
        ))
    else:
        items.append(readiness_item(
            "Drive system check",
            "partial",
            "No engine or motor selected. The tool can still suggest hydraulic demand, but cannot validate drive architecture yet.",
            ["Engine or motor selection"]
        ))

    if water_known and runtime_known and active_device_count > 0:
        items.append(readiness_item(
            "Water runtime estimate",
            "ready",
            "Enough information exists to estimate runtime from available water and active flow."
        ))
    else:
        missing = []

        if not water_known:
            missing.append("Available water gallons")

        if not runtime_known:
            missing.append("Required runtime minutes")

        if active_device_count == 0:
            missing.append("Active device flow")

        items.append(readiness_item(
            "Water runtime estimate",
            "missing",
            "Water runtime estimate is not meaningful yet.",
            missing
        ))

    if has_selected(input_data.get("engine_name")) and fuel_known:
        items.append(readiness_item(
            "Fuel runtime estimate",
            "ready",
            "Engine and fuel storage are selected, so fuel runtime can be checked."
        ))
    elif has_selected(input_data.get("engine_name")):
        items.append(readiness_item(
            "Fuel runtime estimate",
            "partial",
            "Engine is selected, but fuel storage is missing.",
            ["Fuel storage selection"]
        ))
    else:
        items.append(readiness_item(
            "Fuel runtime estimate",
            "partial",
            "Fuel runtime requires an engine-driven architecture.",
            ["Engine selection", "Fuel storage selection"]
        ))

    if has_selected(input_data.get("motor_name")) and battery_known:
        items.append(readiness_item(
            "Battery runtime estimate",
            "ready",
            "Motor and battery are selected, so battery runtime can be checked."
        ))
    elif has_selected(input_data.get("motor_name")):
        items.append(readiness_item(
            "Battery runtime estimate",
            "partial",
            "Motor is selected, but battery storage is missing.",
            ["Battery selection"]
        ))
    else:
        items.append(readiness_item(
            "Battery runtime estimate",
            "partial",
            "Battery runtime requires an electric motor architecture.",
            ["Motor selection", "Battery selection"]
        ))

    if has_last_line_branch(branches):
        items.append(readiness_item(
            "Last-line defense validation",
            "ready",
            "A last-line or structure/eaves branch exists, so structure-defense validation can run."
        ))
    else:
        items.append(readiness_item(
            "Last-line defense validation",
            "partial",
            "No last-line or structure/eaves branch is currently defined. This limits proposal-grade confidence.",
            ["At least one last-line or structure/eaves branch"]
        ))

    ready_count = len([item for item in items if item["status"] == "ready"])
    partial_count = len([item for item in items if item["status"] == "partial"])
    missing_count = len([item for item in items if item["status"] == "missing"])

    if missing_count == 0 and partial_count <= 1:
        overall_status = "ready"
    elif ready_count >= 3:
        overall_status = "partial"
    else:
        overall_status = "missing"

    if overall_status == "ready":
        summary = "Enough information exists to produce a meaningful design result."
    elif overall_status == "partial":
        summary = "Enough information exists for useful preliminary guidance, but some design areas are still incomplete."
    else:
        summary = "More information is needed before the system can produce meaningful design guidance."

    return {
        "overall_status": overall_status,
        "summary": summary,
        "ready_count": ready_count,
        "partial_count": partial_count,
        "missing_count": missing_count,
        "items": items
    }