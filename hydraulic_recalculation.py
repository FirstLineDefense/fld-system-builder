from hydraulic_math import (
    calculate_total_pressure_loss_psi,
)


def recalculate_branch_hydraulics(branch):
    gpm = float(
        branch.get("target_gpm", 0) or 0
    )

    diameter = float(
        branch.get("pipe_diameter_in", 1.0) or 1.0
    )

    length_ft = float(
        branch.get("effective_pipe_length_ft")
        or branch.get("pipe_length_ft")
        or branch.get("length_ft")
        or 100
    )

    elevation_change_ft = float(
        branch.get("elevation_change_ft", 0) or 0
    )

    c_factor = float(
        branch.get("c_factor", 150) or 150
    )

    hydraulic_result = calculate_total_pressure_loss_psi(
        gpm=gpm,
        diameter_in=diameter,
        length_ft=length_ft,
        elevation_change_ft=elevation_change_ft,
        c_factor=c_factor
    )

    branch["velocity_fps"] = hydraulic_result["velocity_fps"]
    branch["friction_loss_psi"] = hydraulic_result["friction_loss_psi"]
    branch["elevation_loss_psi"] = hydraulic_result["elevation_loss_psi"]
    branch["total_pressure_loss_psi"] = hydraulic_result["total_pressure_loss_psi"]
    branch["hydraulic_length_ft"] = length_ft
    branch["hydraulic_c_factor"] = c_factor

    return branch


def recalculate_candidate_hydraulics(candidate):
    from candidate_utils import get_primary

    primary = get_primary(candidate)

    branches = primary.get("branches", []) or []

    updated = []

    for branch in branches:
        updated.append(
            recalculate_branch_hydraulics(branch)
        )

    primary["branches"] = updated
    candidate["primary"] = primary

    return candidate
