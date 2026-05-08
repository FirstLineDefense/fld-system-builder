import math


PSI_PER_FOOT_OF_HEAD = 0.433
FEET_OF_HEAD_PER_PSI = 2.31


def safe_float(value, default=0.0):
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def calculate_pipe_area_sq_ft(diameter_in):
    diameter_ft = safe_float(diameter_in) / 12

    if diameter_ft <= 0:
        return 0

    return math.pi * (diameter_ft / 2) ** 2


def calculate_velocity_fps(flow_gpm, diameter_in):
    flow_gpm = safe_float(flow_gpm)
    area_sq_ft = calculate_pipe_area_sq_ft(diameter_in)

    if flow_gpm <= 0 or area_sq_ft <= 0:
        return 0

    cubic_ft_per_second = flow_gpm * 0.002228
    return cubic_ft_per_second / area_sq_ft


def hazen_williams_friction_loss_ft(flow_gpm, pipe_length_ft, pipe_diameter_in, c_factor=150):
    flow_gpm = safe_float(flow_gpm)
    pipe_length_ft = safe_float(pipe_length_ft)
    pipe_diameter_in = safe_float(pipe_diameter_in)
    c_factor = safe_float(c_factor, 150)

    if flow_gpm <= 0 or pipe_length_ft <= 0 or pipe_diameter_in <= 0 or c_factor <= 0:
        return 0

    return (
        4.52
        * pipe_length_ft
        * (flow_gpm ** 1.85)
        / ((c_factor ** 1.85) * (pipe_diameter_in ** 4.87))
    )


def feet_head_to_psi(feet_head):
    return safe_float(feet_head) * PSI_PER_FOOT_OF_HEAD


def psi_to_feet_head(psi):
    return safe_float(psi) * FEET_OF_HEAD_PER_PSI


def calculate_pressure(input_data, flow_result=None):
    base_pressure_psi = safe_float(input_data.get("base_pressure_psi", 0))
    total_flow_gpm = safe_float(input_data.get("total_flow_gpm", 0))
    elevation_change_ft = safe_float(input_data.get("elevation_change_ft", 0))
    pipe_length_ft = safe_float(input_data.get("pipe_length_ft", 0))
    pipe_diameter_in = safe_float(input_data.get("pipe_diameter_in", 0))
    nominal_pipe_diameter_in = safe_float(
        input_data.get("nominal_pipe_diameter_in", pipe_diameter_in)
    )
    c_factor = safe_float(input_data.get("c_factor", 150))
    required_terminal_pressure_psi = safe_float(input_data.get("required_terminal_pressure_psi", 0))

    if flow_result:
        total_flow_gpm = safe_float(flow_result.get("total_flow_gpm", total_flow_gpm))

    friction_loss_ft = hazen_williams_friction_loss_ft(
        total_flow_gpm,
        pipe_length_ft,
        pipe_diameter_in,
        c_factor
    )

    friction_loss_psi = feet_head_to_psi(friction_loss_ft)

    elevation_loss_psi = feet_head_to_psi(elevation_change_ft)
    elevation_loss_ft = elevation_change_ft

    total_dynamic_head_ft = friction_loss_ft + elevation_loss_ft
    total_pressure_loss_psi = friction_loss_psi + elevation_loss_psi

    final_pressure_psi = base_pressure_psi - total_pressure_loss_psi
    pressure_margin_psi = final_pressure_psi - required_terminal_pressure_psi

    velocity_fps = calculate_velocity_fps(total_flow_gpm, pipe_diameter_in)

    return {
        "base_pressure_psi": base_pressure_psi,
        "total_flow_gpm": total_flow_gpm,
        "pipe_length_ft": pipe_length_ft,
        "pipe_diameter_in": pipe_diameter_in,
        "nominal_pipe_diameter_in": nominal_pipe_diameter_in,
        "c_factor": c_factor,

        "velocity_fps": velocity_fps,

        "friction_loss_ft": friction_loss_ft,
        "friction_loss_psi": friction_loss_psi,

        "elevation_change_ft": elevation_change_ft,
        "elevation_loss_ft": elevation_loss_ft,
        "elevation_loss_psi": elevation_loss_psi,

        "total_dynamic_head_ft": total_dynamic_head_ft,
        "total_pressure_loss_psi": total_pressure_loss_psi,

        "final_pressure_psi": final_pressure_psi,
        "required_terminal_pressure_psi": required_terminal_pressure_psi,
        "pressure_margin_psi": pressure_margin_psi,

        "passed_required_pressure": final_pressure_psi >= required_terminal_pressure_psi
    }