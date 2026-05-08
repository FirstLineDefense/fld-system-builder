def explain_branch_optimization(branch):
    reasons = []

    name = branch.get("name", "Branch")

    pipe_size = branch.get("pipe_size", "")
    gpm = float(branch.get("gpm", 0) or branch.get("flow_gpm", 0) or 0)
    velocity = float(branch.get("velocity_fps", 0) or 0)
    friction_loss = float(branch.get("friction_loss_psi", 0) or branch.get("loss_psi", 0) or 0)

    if velocity >= 8:
        reasons.append({
            "type": "branch_reasoning",
            "label": f"{name} velocity concern",
            "message": f"{name} is running about {velocity:.1f} ft/sec. Upsizing the pipe should reduce velocity, turbulence, and friction loss.",
            "confidence": "high",
            "icon": "🌊",
            "reason": "Branch velocity above 8 ft/sec is a strong indicator that the pipe is hydraulically stressed."
        })

    elif velocity >= 6:
        reasons.append({
            "type": "branch_reasoning",
            "label": f"{name} velocity watch",
          "message": f"{name} is running about {velocity:.1f} ft/sec. This may be acceptable, but upsizing could improve margin.",
            "confidence": "medium",
            "icon": "🌊",
            "reason": "Branch velocity between 6 and 8 ft/sec is usable but not ideal for a resilient wildfire system."
        })

    if friction_loss >= 15:
        reasons.append({
            "type": "branch_reasoning",
            "label": f"{name} friction loss concern",
            "message": f"{name} is losing about {friction_loss:.1f} psi in the branch. Upsizing the pipe is likely the best first optimization.",
            "confidence": "high",
            "icon": "📉",
            "reason": "High branch friction loss reduces delivered sprinkler pressure and wastes pump energy."
        })

    elif friction_loss >= 8:
        reasons.append({
            "type": "branch_reasoning",
            "label": f"{name} friction loss watch",
            "message": f"{name} is losing about {friction_loss:.1f} psi. This is worth watching if the system is pressure constrained.",
            "confidence": "medium",
            "icon": "📉",
            "reason": "Moderate branch loss can become important when elevation gain or long pipe runs are also present."
        })

    if gpm and pipe_size:
        reasons.append({
            "type": "branch_reasoning",
            "label": f"{name} branch context",
            "message": f"{name} is carrying about {gpm:.1f} GPM through {pipe_size}. Optimization should compare pipe upsizing against pump pressure margin.",
            "confidence": "medium",
            "icon": "🧠",
            "reason": "Branch optimization should consider flow, pipe size, velocity, friction loss, and available pump pressure together."
        })

    return reasons
