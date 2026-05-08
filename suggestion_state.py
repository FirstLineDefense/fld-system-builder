def init_suggestion_state(primary):
    if "suggestion_state" not in primary:
        primary["suggestion_state"] = {
            "accepted": [],
            "rejected": [],
            "applied": []
        }

    return primary["suggestion_state"]


def is_suggestion_accepted(primary, key):
    state = init_suggestion_state(primary)
    return key in state["accepted"]


def is_suggestion_rejected(primary, key):
    state = init_suggestion_state(primary)
    return key in state["rejected"]


def mark_suggestion_accepted(primary, key):
    state = init_suggestion_state(primary)

    if key not in state["accepted"]:
        state["accepted"].append(key)


def mark_suggestion_rejected(primary, key):
    state = init_suggestion_state(primary)

    if key not in state["rejected"]:
        state["rejected"].append(key)
