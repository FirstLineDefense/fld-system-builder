from domain.schemas import (
    build_system_input_dto,
    validate_system_input_dto,
)

from config.app_settings import (
    DEFAULT_PREFERRED_VELOCITY_FPS,
    DEFAULT_MAXIMUM_VELOCITY_FPS,
    DEFAULT_AVAILABLE_WATER_GALLONS,
    DEFAULT_REQUIRED_RUNTIME_MINUTES,
    DEFAULT_MINIMUM_PRESSURE_MARGIN_PSI,
    DEFAULT_MAX_SIMULTANEOUS_PORTS,
    DEFAULT_MAX_BUDGET,
)

from app import (
    parse_multi_lines,
    parse_branches,
)


def build_input_data_from_form(
    form
):
    selected_control_lines = parse_multi_lines(
        form,
        "control",
        3
    )

    selected_sensor_lines = parse_multi_lines(
        form,
        "sensor",
        5
    )

    branches = parse_branches(form)

    preferred_velocity_fps = float(
        form.get(
            "preferred_velocity_fps",
            [
                str(
                    DEFAULT_PREFERRED_VELOCITY_FPS
                )
            ]
        )[0]
    )

    maximum_velocity_fps = float(
        form.get(
            "maximum_velocity_fps",
            [
                str(
                    DEFAULT_MAXIMUM_VELOCITY_FPS
                )
            ]
        )[0]
    )

    for branch in branches:
        branch[
            "preferred_velocity_fps"
        ] = preferred_velocity_fps

        branch[
            "maximum_velocity_fps"
        ] = maximum_velocity_fps

    return {
        "branches": branches,

        "available_water_gallons": float(
            form.get(
                "available_water_gallons",
                [
                    str(
                        DEFAULT_AVAILABLE_WATER_GALLONS
                    )
                ]
            )[0]
        ),

        "required_runtime_minutes": float(
            form.get(
                "required_runtime_minutes",
                [
                    str(
                        DEFAULT_REQUIRED_RUNTIME_MINUTES
                    )
                ]
            )[0]
        ),

        "minimum_pressure_margin_psi": float(
            form.get(
                "minimum_pressure_margin_psi",
                [
                    str(
                        DEFAULT_MINIMUM_PRESSURE_MARGIN_PSI
                    )
                ]
            )[0]
        ),

        "preferred_velocity_fps":
            preferred_velocity_fps,

        "maximum_velocity_fps":
            maximum_velocity_fps,

        "max_simultaneous_ports": int(
            form.get(
                "max_simultaneous_ports",
                [
                    str(
                        DEFAULT_MAX_SIMULTANEOUS_PORTS
                    )
                ]
            )[0]
        ),

        "max_budget": float(
            form.get(
                "max_budget",
                [
                    str(
                        DEFAULT_MAX_BUDGET
                    )
                ]
            )[0]
        ),

        "pump_name":
            form.get(
                "pump_name",
                [
                    "Auto Select Pump"
                ]
            )[0],

        "engine_name":
            form.get(
                "engine_name",
                [
                    "None"
                ]
            )[0],

        "motor_name":
            form.get(
                "motor_name",
                [
                    "None"
                ]
            )[0],

        "water_storage_name":
            form.get(
                "water_storage_name",
                [
                    "None"
                ]
            )[0],

        "fuel_storage_name":
            form.get(
                "fuel_storage_name",
                [
                    "None"
                ]
            )[0],

        "battery_name":
            form.get(
                "battery_name",
                [
                    "None"
                ]
            )[0],

        "generator_name":
            form.get(
                "generator_name",
                [
                    "None"
                ]
            )[0],

        "selected_controls":
            selected_control_lines,

        "selected_sensors":
            selected_sensor_lines,
    }

def normalize_and_validate_system_input(raw_data):
    dto = build_system_input_dto(raw_data)
    valid, errors = validate_system_input_dto(dto)

    if not valid:
        raise ValueError(f'System DTO validation failed: {errors}')

    return dto
