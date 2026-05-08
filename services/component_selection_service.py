from registries.component_loader import (
    get_registered_pumps,
    get_registered_motors,
)


def select_best_pump(target_gpm):
    pumps = get_registered_pumps()

    best_name = None
    best_component = None

    for name, component in pumps.items():
        gpm = component.get("gpm", 0)

        if gpm >= target_gpm:
            if best_component is None:
                best_name = name
                best_component = component
                continue

            if gpm < best_component.get("gpm", 0):
                best_name = name
                best_component = component

    return best_name, best_component


def select_best_motor(target_hp):
    motors = get_registered_motors()

    best_name = None
    best_component = None

    for name, component in motors.items():
        hp = component.get("hp", 0)

        if hp >= target_hp:
            if best_component is None:
                best_name = name
                best_component = component
                continue

            if hp < best_component.get("hp", 0):
                best_name = name
                best_component = component

    return best_name, best_component
