import copy


def upsize_pipe(size):
    map = {
        "1 in": "1.25 in",
        "1.25 in": "1.5 in",
        "1.5 in": "2 in",
        "2 in": "2.5 in",
        "2.5 in": "3 in",
        "3 in": "3 in"
    }

    return map.get(size, size)


def apply_branch_pipe_upsize(primary, branch_name):
    primary = copy.deepcopy(primary)

    branches = primary.get("branches", []) or []

    for branch in branches:
        if branch.get("name", "") == branch_name:
            current = branch.get("pipe_size", "")

            if current:
                branch["pipe_size"] = upsize_pipe(current)

    return primary


def apply_optimization_action(primary, action):
    action_type = action.get("type", "")

    if action_type == "branch_upsize":
        return apply_branch_pipe_upsize(
            primary,
            action.get("branch", "")
        )

    return copy.deepcopy(primary)
