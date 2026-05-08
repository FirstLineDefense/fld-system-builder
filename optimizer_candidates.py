copy = None


def generate_branch_upsize_candidates(primary):
    actions = []
    branches = primary.get("branches", []) or []

    for branch in branches:
        name = branch.get("name", "Branch")
        velocity = float(branch.get("velocity_fps", 0) or 0)
        loss = float(branch.get("friction_loss_psi", 0) or branch.get("loss_psi", 0) or 0)

        if velocity >= 6 or loss >= 8:
            actions.append({
                "type": "branch_upsize",
                "branch": name,
                "reason": f"Upsize {name} to reduce velocity and friction loss.",
                "priority": "high" if velocity >= 8 or loss >= 15 else "medium"
            })

    return actions


def generate_optimization_candidates(primary):
    actions = []

    actions.extend(generate_branch_upsize_candidates(primary))

    return actions
