PIPE_OPTIONS = [
    {"size": "1 in", "max_gpm": 25},
    {"size": "1.25 in", "max_gpm": 40},
    {"size": "1.5 in", "max_gpm": 60},
    {"size": "2 in", "max_gpm": 100},
    {"size": "2.5 in", "max_gpm": 160},
    {"size": "3 in", "max_gpm": 250},
]


def suggest_best_pipe_for_branch(branch):
    suggestions = []

    name = branch.get("name", "Branch")
    current_pipe = branch.get("pipe_size", "")
    gpm = float(branch.get("gpm", 0) or branch.get("flow_gpm", 0) or 0)
    velocity = float(branch.get("velocity_fps", 0) or 0)
    friction_loss = float(branch.get("friction_loss_psi", 0) or branch.get("loss_psi", 0) or 0)

    if not gpm:
        return suggestions

    best_pipe = None

    for pipe in PIPE_OPTIONS:
        if gpm <= pipe["max_gpm"]:
            best_pipe = pipe["size"]
            break

    if not best_pipe:
        best_pipe = "3 in plus"

    should_suggest = False

    if current_pipe and best_pipe != current_pipe:
        should_suggest = True

    if velocity >= 6 or friction_loss >= 8:
        should_suggest = True

    if should_suggest:
        suggestions.append({
            "type": "pipe_optimizer",
            "label": f"{name} best pipe suggestion",
            "message": f"For about {gpm:.1f} GPM, suggested branch pipe is {best_pipe}. Current pipe is {current_pipe or 'not set'}.",
            "confidence": "medium",
            "icon": "🧮",
            "reason": "Suggested from branch flow bands, then cross-checked against velocity and friction-loss warning thresholds."
        })

    return suggestions
