from component_library import get_component_library


def _safe_float(value, default=0):
    try:
        if value in [None, ""]:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _find_pipe_diameter(pipe_name):
    library = get_component_library()
    pipes = library.get("pipes", [])

    for pipe in pipes:
        if getattr(pipe, "name", "") == pipe_name:
            return _safe_float(
                getattr(
                    pipe,
                    "internal_diameter_in",
                    getattr(pipe, "diameter_in", 1.0)
                ),
                1.0
            )

    return 1.0


def _find_device_flow(device_name):
    library = get_component_library()
    devices = library.get("devices", [])

    for device in devices:
        if getattr(device, "name", "") == device_name:
            return _safe_float(
                getattr(device, "flow_gpm", 0),
                0
            )

    return 0


def _branch_device_flow(branch):
    total_flow = 0

    for device_line in branch.get("devices", []) or []:
        device_name = device_line.get("device_name", "")
        quantity = _safe_float(
            device_line.get("quantity", 0),
            0
        )

        total_flow += _find_device_flow(device_name) * quantity

    return total_flow


def build_optimizer_candidate_from_input(input_data):
    branches = input_data.get("branches", []) or []
    optimizer_branches = []

    preferred_velocity = _safe_float(
        input_data.get("preferred_velocity_fps"),
        8
    )

    for branch in branches:
        target_gpm = _safe_float(
            branch.get("target_gpm")
            or branch.get("flow_gpm")
            or branch.get("gpm"),
            0
        )

        if target_gpm <= 0:
            target_gpm = _branch_device_flow(branch)

        if target_gpm <= 0:
            continue

        pipe_diameter = _safe_float(
            branch.get("pipe_diameter_in")
            or branch.get("diameter_in"),
            0
        )

        if pipe_diameter <= 0:
            pipe_diameter = _find_pipe_diameter(
                branch.get("pipe_name", "")
            )

        velocity = _safe_float(
            branch.get("velocity_fps")
            or branch.get("velocity"),
            0
        )

        if velocity <= 0:
            velocity = preferred_velocity

        optimizer_branches.append({
            "target_gpm": target_gpm,
            "velocity_fps": velocity,
            "pipe_diameter_in": pipe_diameter
        })

    if not optimizer_branches:
        optimizer_branches = [
            {
                "target_gpm": 120,
                "velocity_fps": preferred_velocity,
                "pipe_diameter_in": 1.0
            }
        ]

    total_branch_gpm = sum(
        branch.get("target_gpm", 0)
        for branch in optimizer_branches
    )

    return {
        "primary": {
            "pump": {
                "gpm": _safe_float(
                    input_data.get("pump_gpm")
                    or input_data.get("target_pump_gpm"),
                    total_branch_gpm or 300
                )
            },

            "motor": {
                "hp": _safe_float(
                    input_data.get("motor_hp"),
                    10
                )
            },

            "runtime_minutes":
                _safe_float(
                    input_data.get("required_runtime_minutes")
                    or input_data.get("runtime_minutes"),
                    60
                ),

            "water_gallons":
                _safe_float(
                    input_data.get("available_water_gallons")
                    or input_data.get("water_gallons"),
                    5000
                ),

            "branches":
                optimizer_branches
        }
    }
