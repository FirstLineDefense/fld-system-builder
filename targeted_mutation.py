from copy import deepcopy

from component_targets import (
    identify_weak_components
)

from mutation_randomness import (
    random_multiplier
)

from mutation_context import (
    get_current_mutation_scale
)


def scaled_multiplier(
    minimum,
    maximum
):
    scale = get_current_mutation_scale()

    center = 1.0

    raw = random_multiplier(
        minimum,
        maximum
    )

    distance = raw - center

    adjusted = center + (
        distance * scale
    )

    return round(
        adjusted,
        3
    )


def apply_targeted_mutation(candidate):
    mutated = deepcopy(candidate)

    primary = (
        mutated.get("primary", {})
        or {}
    )

    weak = identify_weak_components(
        mutated
    )

    if "pump_capacity" in weak:
        pump = primary.get("pump", {}) or {}

        current_gpm = (
            pump.get("gpm", 0)
            or 0
        )

        pump["gpm"] = round(
            current_gpm
            * scaled_multiplier(
                1.05,
                1.25
            ),
            1
        )

        primary["pump"] = pump

    if "pump_oversized" in weak:
        pump = primary.get("pump", {}) or {}

        current_gpm = (
            pump.get("gpm", 0)
            or 0
        )

        pump["gpm"] = round(
            current_gpm
            * scaled_multiplier(
                0.80,
                0.98
            ),
            1
        )

        primary["pump"] = pump

    if "motor_power" in weak:
        motor = primary.get("motor", {}) or {}

        current_hp = (
            motor.get("hp", 0)
            or 0
        )

        motor["hp"] = round(
            current_hp
            * scaled_multiplier(
                1.05,
                1.35
            ),
            1
        )

        primary["motor"] = motor

    mutated["primary"] = primary
    mutated["mutation_targets"] = weak
    mutated["mutation_scale"] = (
        get_current_mutation_scale()
    )

    return mutated
