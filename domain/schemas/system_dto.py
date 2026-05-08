def normalize_number(value, default=0.0):
    if value is None or value == "":
        return default

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def normalize_string(value, default=""):
    if value is None:
        return default

    return str(value).strip()


def normalize_list(value):
    if value is None:
        return []

    if isinstance(value, list):
        return value

    return [value]


def build_system_input_dto(raw):
    raw = raw or {}

    dto = {
        "project_name": normalize_string(raw.get("project_name"), "Untitled Project"),
        "water_source": normalize_string(raw.get("water_source")),
        "pump": raw.get("pump") or {},
        "motor": raw.get("motor") or {},
        "manifold": raw.get("manifold") or {},
        "branches": normalize_list(raw.get("branches")),
        "constraints": raw.get("constraints") or {},
        "metadata": raw.get("metadata") or {},
    }

    return dto


def validate_system_input_dto(dto):
    errors = []

    if not isinstance(dto, dict):
        return False, ["DTO must be a dictionary"]

    if not dto.get("project_name"):
        errors.append("project_name is required")

    if not isinstance(dto.get("branches"), list):
        errors.append("branches must be a list")

    if not isinstance(dto.get("pump"), dict):
        errors.append("pump must be a dictionary")

    if not isinstance(dto.get("motor"), dict):
        errors.append("motor must be a dictionary")

    if not isinstance(dto.get("manifold"), dict):
        errors.append("manifold must be a dictionary")

    if not isinstance(dto.get("constraints"), dict):
        errors.append("constraints must be a dictionary")

    return len(errors) == 0, errors
