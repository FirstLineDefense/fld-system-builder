from itertools import combinations
from hydraulics import calculate_pressure
from pump_curve import get_pump_pressure_at_flow, analyze_pump_operating_point


def find_component_by_name(component_list, name):
    if not name or name == "None":
        return None

    for component in component_list:
        if component.name == name:
            return component

    return None


def get_pipe_internal_diameter(pipe):
    return getattr(pipe, "internal_diameter_in", pipe.diameter_in)


def safe_float(value, default=0):
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value, default=0):
    try:
        if value is None or value == "":
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def calculate_equivalent_length_ft(branch):
    """
    Converts branch fitting counts into an equivalent straight-pipe length.

    These are intentionally conservative generic defaults for Phase 1 accuracy.
    Later, we can move these into the component database and make them pipe-size
    specific if needed.
    """

    elbow_90_qty = safe_int(branch.get("elbow_90_qty", 0))
    elbow_45_qty = safe_int(branch.get("elbow_45_qty", 0))
    sweep_bend_qty = safe_int(branch.get("sweep_bend_qty", 0))
    tee_qty = safe_int(branch.get("tee_qty", 0))
    valve_qty = safe_int(branch.get("valve_qty", 0))
    other_equivalent_length_ft = safe_float(
        branch.get("other_equivalent_length_ft", 0)
    )

    equivalent_length_ft = (
        (elbow_90_qty * 5.0) +
        (elbow_45_qty * 2.5) +
        (sweep_bend_qty * 1.5) +
        (tee_qty * 10.0) +
        (valve_qty * 2.0) +
        other_equivalent_length_ft
    )

    return max(equivalent_length_ft, 0)


def get_branch_fitting_counts(branch):
    return {
        "elbow_90_qty": safe_int(branch.get("elbow_90_qty", 0)),
        "elbow_45_qty": safe_int(branch.get("elbow_45_qty", 0)),
        "sweep_bend_qty": safe_int(branch.get("sweep_bend_qty", 0)),
        "tee_qty": safe_int(branch.get("tee_qty", 0)),
        "valve_qty": safe_int(branch.get("valve_qty", 0)),
        "other_equivalent_length_ft": safe_float(
            branch.get("other_equivalent_length_ft", 0)
        )
    }


def calculate_branch_flow(branch, library):
    device_lines = branch.get("devices", [])

    total_flow = 0
    total_device_count = 0
    device_breakdown = []
    required_pressures = []

    for line in device_lines:
        device_name = line.get("name")
        quantity = safe_int(line.get("quantity", 0))

        device = find_component_by_name(library.get("devices", []), device_name)

        if not device or quantity <= 0:
            continue

        line_flow = device.flow_gpm * quantity

        total_flow += line_flow
        total_device_count += quantity
        required_pressures.append(device.required_pressure_psi)

        device_breakdown.append({
            "name": device.name,
            "quantity": quantity,
            "flow_gpm_each": device.flow_gpm,
            "line_flow_gpm": line_flow,
            "required_pressure_psi": device.required_pressure_psi
        })

    required_terminal_pressure = max(required_pressures) if required_pressures else 0

    return {
        "branch_number": branch.get("branch_number"),
        "device_count": total_device_count,
        "total_flow_gpm": total_flow,
        "required_terminal_pressure_psi": required_terminal_pressure,
        "device_breakdown": device_breakdown
    }


def empty_branch_pressure_result(branch, warning):
    base_pipe_length_ft = safe_float(branch.get("pipe_length_ft", 0))
    equivalent_length_ft = calculate_equivalent_length_ft(branch)
    effective_pipe_length_ft = base_pipe_length_ft + equivalent_length_ft

    branch_flow = {
        "branch_number": branch.get("branch_number"),
        "device_count": 0,
        "total_flow_gpm": 0,
        "required_terminal_pressure_psi": 0,
        "device_breakdown": []
    }

    return {
        "branch_number": branch.get("branch_number"),
        "active": branch.get("active", False),
        "role": branch.get("role", "first_line"),
        "priority": safe_int(branch.get("priority", 2), 2),
        "pipe": None,
        "pipe_name": branch.get("pipe_name", "None"),
        "pipe_length_ft": effective_pipe_length_ft,
        "base_pipe_length_ft": base_pipe_length_ft,
        "equivalent_length_ft": equivalent_length_ft,
        "effective_pipe_length_ft": effective_pipe_length_ft,
        "fittings": get_branch_fitting_counts(branch),
        "elbow_90_qty": safe_int(branch.get("elbow_90_qty", 0)),
        "elbow_45_qty": safe_int(branch.get("elbow_45_qty", 0)),
        "sweep_bend_qty": safe_int(branch.get("sweep_bend_qty", 0)),
        "tee_qty": safe_int(branch.get("tee_qty", 0)),
        "valve_qty": safe_int(branch.get("valve_qty", 0)),
        "other_equivalent_length_ft": safe_float(
            branch.get("other_equivalent_length_ft", 0)
        ),
        "elevation_change_ft": safe_float(branch.get("elevation_change_ft", 0)),
        "flow": branch_flow,
        "pressure": {},
        "pump_operating_point": {},
        "flow_used_for_pressure_gpm": 0,
        "velocity_fps": 0,
        "friction_loss_ft": 0,
        "friction_loss_psi": 0,
        "elevation_loss_psi": 0,
        "total_dynamic_head_ft": 0,
        "total_pressure_loss_psi": 0,
        "final_pressure_psi": 0,
        "required_terminal_pressure_psi": 0,
        "pressure_margin_psi": -999999,
        "minimum_pressure_margin_psi": 0,
        "passed": False,
        "warnings": [warning]
    }


def calculate_branch_pressure(
    branch,
    pump,
    library,
    minimum_pressure_margin_psi,
    combined_flow_gpm=None
):
    pipe = find_component_by_name(library.get("pipes", []), branch.get("pipe_name"))

    if not pipe:
        return empty_branch_pressure_result(
            branch,
            f"Branch {branch.get('branch_number')} has no valid pipe selected."
        )

    branch_flow = calculate_branch_flow(branch, library)

    flow_for_pressure = combined_flow_gpm
    if flow_for_pressure is None:
        flow_for_pressure = branch_flow["total_flow_gpm"]

    pump_operating_point = get_pump_pressure_at_flow(pump, flow_for_pressure)
    operating_pressure_psi = pump_operating_point["pressure_psi"]

    internal_pipe_diameter_in = get_pipe_internal_diameter(pipe)

    base_pipe_length_ft = safe_float(branch.get("pipe_length_ft", 0))
    equivalent_length_ft = calculate_equivalent_length_ft(branch)
    effective_pipe_length_ft = base_pipe_length_ft + equivalent_length_ft

    pressure_input = {
        "base_pressure_psi": operating_pressure_psi,
        "total_flow_gpm": flow_for_pressure,
        "elevation_change_ft": safe_float(branch.get("elevation_change_ft", 0)),
        "pipe_length_ft": effective_pipe_length_ft,
        "pipe_diameter_in": internal_pipe_diameter_in,
        "nominal_pipe_diameter_in": pipe.diameter_in,
        "c_factor": pipe.c_factor,
        "required_terminal_pressure_psi": branch_flow[
            "required_terminal_pressure_psi"
        ]
    }

    pressure = calculate_pressure(pressure_input, {
        "total_flow_gpm": flow_for_pressure
    })

    final_pressure = pressure.get("final_pressure_psi", 0)
    required_pressure = branch_flow["required_terminal_pressure_psi"]
    pressure_margin = final_pressure - required_pressure
    margin_passed = pressure_margin >= minimum_pressure_margin_psi

    warnings = []

    if branch_flow["total_flow_gpm"] <= 0:
        warnings.append(f"Branch {branch.get('branch_number')} has no active devices.")

    if not margin_passed:
        warnings.append(
            f"Branch {branch.get('branch_number')} does not meet minimum pressure margin."
        )

    if not margin_passed:
        warnings.append(
            f"Branch {branch.get('branch_number')} does not meet minimum pressure margin."
        )

    return {
        "branch_number": branch.get("branch_number"),
        "active": branch.get("active", False),
        "role": branch.get("role", "first_line"),
        "priority": safe_int(branch.get("priority", 2), 2),
        "pipe": pipe,
        "pipe_name": pipe.name,
        "pipe_length_ft": effective_pipe_length_ft,
        "base_pipe_length_ft": base_pipe_length_ft,
        "equivalent_length_ft": equivalent_length_ft,
        "effective_pipe_length_ft": effective_pipe_length_ft,
        "fittings": get_branch_fitting_counts(branch),
        "elbow_90_qty": safe_int(branch.get("elbow_90_qty", 0)),
        "elbow_45_qty": safe_int(branch.get("elbow_45_qty", 0)),
        "sweep_bend_qty": safe_int(branch.get("sweep_bend_qty", 0)),
        "tee_qty": safe_int(branch.get("tee_qty", 0)),
        "valve_qty": safe_int(branch.get("valve_qty", 0)),
        "other_equivalent_length_ft": safe_float(
            branch.get("other_equivalent_length_ft", 0)
        ),
        "elevation_change_ft": safe_float(branch.get("elevation_change_ft", 0)),
        "nominal_pipe_diameter_in": pipe.diameter_in,
        "internal_pipe_diameter_in": internal_pipe_diameter_in,
        "wall_type": getattr(pipe, "wall_type", ""),
        "pressure_rating_psi": getattr(pipe, "pressure_rating_psi", None),
        "flow": branch_flow,
        "pressure": pressure,
        "pump_operating_point": pump_operating_point,
        "flow_used_for_pressure_gpm": flow_for_pressure,
        "velocity_fps": pressure.get("velocity_fps", 0),
        "friction_loss_ft": pressure.get("friction_loss_ft", 0),
        "friction_loss_psi": pressure.get("friction_loss_psi", 0),
        "elevation_loss_psi": pressure.get("elevation_loss_psi", 0),
        "total_dynamic_head_ft": pressure.get("total_dynamic_head_ft", 0),
        "total_pressure_loss_psi": pressure.get("total_pressure_loss_psi", 0),
        "final_pressure_psi": final_pressure,
        "required_terminal_pressure_psi": required_pressure,
        "pressure_margin_psi": pressure_margin,
        "minimum_pressure_margin_psi": minimum_pressure_margin_psi,
        "passed": margin_passed and branch_flow["total_flow_gpm"] > 0,
        "warnings": warnings
    }


def calculate_mode_result(mode_name, branches, pump, library, minimum_pressure_margin_psi):
    active_branches = [b for b in branches if b.get("active")]

    total_flow = 0
    for branch in active_branches:
        branch_flow = calculate_branch_flow(branch, library)
        total_flow += branch_flow["total_flow_gpm"]

    pump_operating_analysis = analyze_pump_operating_point(pump, total_flow)

    branch_results = []
    all_warnings = []
    all_warnings.extend(pump_operating_analysis.get("warnings", []))

    for branch in active_branches:
        branch_result = calculate_branch_pressure(
            branch,
            pump,
            library,
            minimum_pressure_margin_psi,
            combined_flow_gpm=total_flow
        )

        branch_results.append(branch_result)
        all_warnings.extend(branch_result.get("warnings", []))

    flow_ok = pump.max_flow_gpm >= total_flow

    if not flow_ok:
        all_warnings.append(
            f"{mode_name}: Pump flow capacity is below mode flow requirement."
        )

    failing_branches = [b for b in branch_results if not b["passed"]]

    worst_branch = None
    if branch_results:
        worst_branch = min(branch_results, key=lambda b: b["pressure_margin_psi"])

    passed = len(active_branches) > 0 and flow_ok and len(failing_branches) == 0

    if len(active_branches) == 0:
        all_warnings.append(f"{mode_name}: No active branches in this mode.")

    return {
        "mode_name": mode_name,
        "branch_count": len(active_branches),
        "total_flow_gpm": total_flow,
        "pump_flow_capacity_gpm": pump.max_flow_gpm,
        "pump_operating_pressure_psi": pump_operating_analysis[
            "operating_pressure_psi"
        ],
        "pump_flow_utilization_fraction": pump_operating_analysis[
            "flow_utilization_fraction"
        ],
        "pump_operating_analysis": pump_operating_analysis,
        "flow_ok": flow_ok,
        "branch_results": branch_results,
        "failing_branch_count": len(failing_branches),
        "worst_branch": worst_branch,
        "passed": passed,
        "warnings": all_warnings
    }


def filter_branches_by_role(branches, roles):
    return [
        branch for branch in branches
        if branch.get("active") and branch.get("role") in roles
    ]


def find_worst_combinations(branches, max_simultaneous_ports):
    active_branches = [b for b in branches if b.get("active")]

    if max_simultaneous_ports <= 0:
        return []

    if len(active_branches) <= max_simultaneous_ports:
        return [active_branches]

    combos = []

    sorted_by_priority = sorted(
        active_branches,
        key=lambda b: safe_int(b.get("priority", 2), 2)
    )

    priority_combo = sorted_by_priority[:max_simultaneous_ports]
    combos.append(priority_combo)

    for combo in combinations(active_branches, max_simultaneous_ports):
        combos.append(list(combo))

    return combos


def calculate_max_simultaneous_mode(
    branches,
    pump,
    library,
    minimum_pressure_margin_psi,
    max_simultaneous_ports
):
    combos = find_worst_combinations(branches, max_simultaneous_ports)

    if not combos:
        return {
            "mode_name": "Max Simultaneous Ports",
            "branch_count": 0,
            "total_flow_gpm": 0,
            "passed": False,
            "warnings": [
                "No branch combinations available for max simultaneous port check."
            ],
            "branch_results": [],
            "worst_branch": None
        }

    mode_results = []

    for index, combo in enumerate(combos):
        result = calculate_mode_result(
            f"Max Simultaneous Combo {index + 1}",
            combo,
            pump,
            library,
            minimum_pressure_margin_psi
        )

        mode_results.append(result)

    failing = [m for m in mode_results if not m["passed"]]

    worst_mode = min(
        mode_results,
        key=lambda m: (
            m["worst_branch"]["pressure_margin_psi"]
            if m["worst_branch"]
            else 999999
        )
    )

    warnings = []

    if failing:
        warnings.append(
            "At least one max-simultaneous branch combination fails."
        )

    return {
        "mode_name": "Max Simultaneous Ports",
        "branch_count": max_simultaneous_ports,
        "total_flow_gpm": worst_mode["total_flow_gpm"],
        "passed": len(failing) == 0,
        "warnings": warnings,
        "worst_mode": worst_mode,
        "mode_results": mode_results,
        "branch_results": worst_mode["branch_results"],
        "worst_branch": worst_mode["worst_branch"],
        "pump_operating_pressure_psi": worst_mode.get(
            "pump_operating_pressure_psi",
            0
        ),
        "pump_flow_utilization_fraction": worst_mode.get(
            "pump_flow_utilization_fraction",
            0
        ),
    }


def calculate_operating_modes(
    branches,
    pump,
    library,
    minimum_pressure_margin_psi,
    max_simultaneous_ports
):
    active_branches = [b for b in branches if b.get("active")]

    all_active_mode = calculate_mode_result(
        "All Active Branches",
        active_branches,
        pump,
        library,
        minimum_pressure_margin_psi
    )

    first_line_branches = filter_branches_by_role(
        branches,
        ["first_line", "auxiliary"]
    )

    first_line_mode = calculate_mode_result(
        "First Line Defense Mode",
        first_line_branches,
        pump,
        library,
        minimum_pressure_margin_psi
    )

    last_line_branches = filter_branches_by_role(
        branches,
        ["last_line", "structure_eaves"]
    )

    last_line_mode = calculate_mode_result(
        "Last Line / Structure Defense Mode",
        last_line_branches,
        pump,
        library,
        minimum_pressure_margin_psi
    )

    foam_branches = filter_branches_by_role(
        branches,
        ["foam"]
    )

    foam_mode = calculate_mode_result(
        "Foam Mode",
        foam_branches,
        pump,
        library,
        minimum_pressure_margin_psi
    )

    max_simultaneous_mode = calculate_max_simultaneous_mode(
        branches,
        pump,
        library,
        minimum_pressure_margin_psi,
        max_simultaneous_ports
    )

    modes = [
        all_active_mode,
        first_line_mode,
        last_line_mode,
        foam_mode,
        max_simultaneous_mode
    ]

    warnings = []

    for mode in modes:
        warnings.extend(mode.get("warnings", []))

    last_line_passed = last_line_mode["passed"]

    if not last_line_passed:
        warnings.append(
            "Last Line / Structure Defense Mode does not pass. Treat this as a critical design failure."
        )

    return {
        "modes": modes,
        "all_active_mode": all_active_mode,
        "first_line_mode": first_line_mode,
        "last_line_mode": last_line_mode,
        "foam_mode": foam_mode,
        "max_simultaneous_mode": max_simultaneous_mode,
        "last_line_passed": last_line_passed,
        "passed": last_line_passed and max_simultaneous_mode["passed"],
        "warnings": warnings
    }


def calculate_manifold(
    branches,
    pump,
    library,
    minimum_pressure_margin_psi,
    max_simultaneous_ports=1
):
    active_branches = [b for b in branches if b.get("active")]

    branch_results = []
    total_installed_flow = 0
    all_warnings = []

    for branch in active_branches:
        branch_result = calculate_branch_pressure(
            branch,
            pump,
            library,
            minimum_pressure_margin_psi
        )

        branch_results.append(branch_result)
        total_installed_flow += branch_result.get("flow", {}).get(
            "total_flow_gpm",
            0
        )
        all_warnings.extend(branch_result.get("warnings", []))

    if not active_branches:
        all_warnings.append("No active manifold branches selected.")

    passing_branches = [b for b in branch_results if b["passed"]]
    failing_branches = [b for b in branch_results if not b["passed"]]

    worst_branch = None
    best_branch = None

    if branch_results:
        worst_branch = min(branch_results, key=lambda b: b["pressure_margin_psi"])
        best_branch = max(branch_results, key=lambda b: b["pressure_margin_psi"])

    operating_modes = calculate_operating_modes(
        branches,
        pump,
        library,
        minimum_pressure_margin_psi,
        max_simultaneous_ports
    )

    all_warnings.extend(operating_modes["warnings"])

    max_mode = operating_modes.get("max_simultaneous_mode", {})

    return {
        "active_branch_count": len(active_branches),
        "max_simultaneous_ports": max_simultaneous_ports,
        "total_installed_flow_gpm": total_installed_flow,
        "total_flow_gpm": max_mode.get("total_flow_gpm", 0),
        "pump_operating_pressure_psi": max_mode.get(
            "pump_operating_pressure_psi",
            0
        ),
        "pump_flow_utilization_fraction": max_mode.get(
            "pump_flow_utilization_fraction",
            0
        ),
        "branch_results": branch_results,
        "passing_branch_count": len(passing_branches),
        "failing_branch_count": len(failing_branches),
        "worst_branch": worst_branch,
        "best_branch": best_branch,
        "operating_modes": operating_modes,
        "passed": len(active_branches) > 0 and operating_modes["passed"],
        "warnings": all_warnings
    }