from copy import deepcopy


def normalize_primary(primary):
    primary = deepcopy(primary or {})

    primary.setdefault("pump", {})
    primary.setdefault("motor", {})
    primary.setdefault("branches", [])

    pump = primary["pump"]
    motor = primary["motor"]
    branches = primary["branches"]

    pump.setdefault("gpm", 0)

    motor.setdefault("hp", 0)

    normalized_branches = []

    for i, branch in enumerate(branches, 1):
        branch = deepcopy(branch or {})

        branch.setdefault(
            "branch_number",
            i
        )

        branch.setdefault(
            "target_gpm",
            0
        )

        branch.setdefault(
            "velocity_fps",
            0
        )

        branch.setdefault(
            "pipe_diameter_in",
            1.0
        )

        normalized_branches.append(branch)

    primary["branches"] = normalized_branches

    return primary


def clone_primary(primary):
    return deepcopy(
        normalize_primary(primary)
    )
