from copy import deepcopy


def normalize_candidate(candidate):
    candidate = deepcopy(candidate)

    if "primary" not in candidate:
        candidate = {
            "primary": candidate
        }

    primary = candidate.get("primary", {}) or {}

    primary.setdefault("pump", {})
    primary.setdefault("motor", {})
    primary.setdefault("engine", {})
    primary.setdefault("branches", [])

    candidate["primary"] = primary

    return candidate


def get_primary(candidate):
    candidate = normalize_candidate(candidate)

    return candidate["primary"]


def set_primary(candidate, primary):
    candidate = normalize_candidate(candidate)

    candidate["primary"] = primary

    return candidate


def get_branches(candidate):
    primary = get_primary(candidate)

    return primary.get("branches", []) or []


def set_branches(candidate, branches):
    candidate = normalize_candidate(candidate)

    candidate["primary"]["branches"] = branches

    return candidate


def get_pump(candidate):
    primary = get_primary(candidate)

    return primary.get("pump", {}) or {}


def set_pump(candidate, pump):
    candidate = normalize_candidate(candidate)

    candidate["primary"]["pump"] = pump

    return candidate


def get_motor(candidate):
    primary = get_primary(candidate)

    return primary.get("motor", {}) or {}


def set_motor(candidate, motor):
    candidate = normalize_candidate(candidate)

    candidate["primary"]["motor"] = motor

    return candidate
