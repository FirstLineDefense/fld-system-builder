import math


def calculate_velocity_fps(gpm, diameter_in):
    if gpm <= 0 or diameter_in <= 0:
        return 0

    area_sq_in = math.pi * (diameter_in / 2) ** 2

    return round(
        (gpm * 0.4085) / area_sq_in,
        2
    )


def calculate_hazen_williams_friction_loss_psi(
    gpm,
    diameter_in,
    length_ft,
    c_factor=150
):
    if gpm <= 0 or diameter_in <= 0 or length_ft <= 0:
        return 0

    head_loss_ft = (
        10.67
        * length_ft
        * (gpm ** 1.852)
        / ((c_factor ** 1.852) * (diameter_in ** 4.871))
    )

    psi_loss = head_loss_ft * 0.433

    return round(psi_loss, 2)


def calculate_elevation_pressure_psi(elevation_change_ft):
    return round(elevation_change_ft * 0.433, 2)


def calculate_total_pressure_loss_psi(
    gpm,
    diameter_in,
    length_ft,
    elevation_change_ft=0,
    c_factor=150
):
    friction_loss = calculate_hazen_williams_friction_loss_psi(
        gpm,
        diameter_in,
        length_ft,
        c_factor
    )

    elevation_loss = calculate_elevation_pressure_psi(
        elevation_change_ft
    )

    total_loss = friction_loss + elevation_loss

    return {
        "velocity_fps": calculate_velocity_fps(gpm, diameter_in),
        "friction_loss_psi": friction_loss,
        "elevation_loss_psi": elevation_loss,
        "total_pressure_loss_psi": round(total_loss, 2)
    }
