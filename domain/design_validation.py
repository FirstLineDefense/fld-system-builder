def validate_primary(primary):
    errors = []

    if not isinstance(primary, dict):
        errors.append(
            "primary must be a dictionary"
        )
        return errors

    branches = primary.get("branches", [])

    if not isinstance(branches, list):
        errors.append(
            "branches must be a list"
        )

    pump = primary.get("pump", {})

    if not isinstance(pump, dict):
        errors.append(
            "pump must be a dictionary"
        )

    motor = primary.get("motor", {})

    if not isinstance(motor, dict):
        errors.append(
            "motor must be a dictionary"
        )

    return errors
