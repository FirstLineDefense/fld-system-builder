import copy
from branches import calculate_manifold
from hydraulic_intelligence import calculate_pipe_velocity_fps


def get_pipe_by_name(library, pipe_name):
    for pipe in library.get("pipes", []):
        if pipe.name == pipe_name:
            return pipe
    return None


def sorted_pipes(library):
    return sorted(
        library.get("pipes", []),
        key=lambda pipe: pipe.diameter_in
    )


def get_larger_pipes(library, current_pipe_name):
    current_pipe = get_pipe_by_name(library, current_pipe_name)

    if not current_pipe:
        return []

    larger = [
        pipe for pipe in sorted_pipes(library)
        if pipe.diameter_in > current_pipe.diameter_in
    ]

    # Prefer same material + same schedule first
    preferred = []
    secondary = []

    current_material = getattr(current_pipe, "material", "")
    current_wall = getattr(current_pipe, "wall_type", "")

    for pipe in larger:
        same_material = getattr(pipe, "material", "") == current_material
        same_wall = getattr(pipe, "wall_type", "") == current_wall

        if same_material and same_wall:
            preferred.append(pipe)
        else:
            secondary.append(pipe)

    return preferred + secondary
    current_pipe = get_pipe_by_name(library, current_pipe_name)

    if not current_pipe:
        return []

    return [
        pipe for pipe in sorted_pipes(library)
        if pipe.diameter_in > current_pipe.diameter_in
    ]


def get_branch_result(manifold, branch_number):
    for branch in manifold.get("branch_results", []):
        if int(branch.get("branch_number", 0)) == int(branch_number):
            return branch
    return None


def summarize_branch(branch_result):
    if not branch_result:
        return {
            "final_pressure_psi": 0,
            "pressure_margin_psi": 0,
            "flow_gpm": 0,
            "velocity_fps": 0,
            "passed": False
        }

    pipe = branch_result.get("pipe")
    flow_gpm = branch_result.get("flow", {}).get("total_flow_gpm", 0)
    diameter = pipe.diameter_in if pipe else 0

    return {
        "final_pressure_psi": branch_result.get("final_pressure_psi", 0),
        "pressure_margin_psi": branch_result.get("pressure_margin_psi", 0),
        "flow_gpm": flow_gpm,
        "velocity_fps": calculate_pipe_velocity_fps(flow_gpm, diameter),
        "passed": branch_result.get("passed", False)
    }


def score_manifold(manifold):
    operating = manifold.get("operating_modes", {})
    modes = operating.get("modes", [])

    passed_modes = len([mode for mode in modes if mode.get("passed")])
    failed_modes = len([mode for mode in modes if not mode.get("passed")])
    failing_branches = manifold.get("failing_branch_count", 0)

    worst_branch = manifold.get("worst_branch")
    worst_margin = worst_branch.get("pressure_margin_psi", 0) if worst_branch else 0

    score = 0
    score += passed_modes * 100
    score -= failed_modes * 150
    score -= failing_branches * 100
    score += worst_margin

    if operating.get("last_line_passed"):
        score += 300
    else:
        score -= 500

    return score


def run_manifold(input_data, library, pump, branches_override=None, max_ports_override=None):
    branches = branches_override if branches_override is not None else input_data.get("branches", [])
    minimum_pressure_margin_psi = input_data.get("minimum_pressure_margin_psi", 20)
    max_simultaneous_ports = max_ports_override

    if max_simultaneous_ports is None:
        max_simultaneous_ports = int(input_data.get("max_simultaneous_ports", 1))

    return calculate_manifold(
        branches,
        pump,
        library,
        minimum_pressure_margin_psi,
        max_simultaneous_ports
    )


def test_single_branch_pipe_upgrades(input_data, library, pump, baseline_manifold):
    trials = []

    if not pump:
        return trials

    baseline_branches = input_data.get("branches", [])
    preferred_velocity_fps = float(input_data.get("preferred_velocity_fps", 8))
    minimum_pressure_margin_psi = float(input_data.get("minimum_pressure_margin_psi", 20))

    for branch in baseline_branches:
        if not branch.get("active"):
            continue

        branch_number = branch.get("branch_number")
        current_pipe_name = branch.get("pipe_name")
        current_pipe = get_pipe_by_name(library, current_pipe_name)
        larger_pipes = get_larger_pipes(library, current_pipe_name)

        if not current_pipe:
            continue

        baseline_branch_result = get_branch_result(baseline_manifold, branch_number)
        baseline_summary = summarize_branch(baseline_branch_result)

        baseline_margin = baseline_summary["pressure_margin_psi"]
        baseline_velocity = baseline_summary["velocity_fps"]

        minimum_viable_found = False

        for pipe in larger_pipes:
            trial_branches = copy.deepcopy(baseline_branches)

            for trial_branch in trial_branches:
                if int(trial_branch.get("branch_number", 0)) == int(branch_number):
                    trial_branch["pipe_name"] = pipe.name

            trial_manifold = run_manifold(
                input_data,
                library,
                pump,
                branches_override=trial_branches
            )

            trial_branch_result = get_branch_result(trial_manifold, branch_number)
            trial_summary = summarize_branch(trial_branch_result)

            margin_gain = trial_summary["pressure_margin_psi"] - baseline_margin
            velocity_reduction = baseline_velocity - trial_summary["velocity_fps"]

            pressure_ok = trial_summary["pressure_margin_psi"] >= minimum_pressure_margin_psi
            velocity_ok = trial_summary["velocity_fps"] <= preferred_velocity_fps
            trial_passed = trial_summary["passed"]

            minimum_viable = False

            if trial_passed and pressure_ok and velocity_ok and not minimum_viable_found:
                minimum_viable = True
                minimum_viable_found = True

            pipe_cost_delta = max(pipe.unit_cost - current_pipe.unit_cost, 0)

            oversize_penalty = 0
            if trial_summary["velocity_fps"] < preferred_velocity_fps * 0.5:
                oversize_penalty = 25

            diminishing_returns = False
            if velocity_ok and trial_summary["velocity_fps"] < preferred_velocity_fps * 0.75:
                diminishing_returns = True

            engineering_reasoning = []

            if velocity_ok:
                engineering_reasoning.append(
                    f"Meets preferred velocity target of {preferred_velocity_fps:.1f} ft/s."
                )
            else:
                engineering_reasoning.append(
                    f"Does not yet meet preferred velocity target of {preferred_velocity_fps:.1f} ft/s."
                )

            if pressure_ok:
                engineering_reasoning.append(
                    f"Maintains required pressure margin of {minimum_pressure_margin_psi:.1f} PSI."
                )
            else:
                engineering_reasoning.append(
                    f"Does not maintain required pressure margin of {minimum_pressure_margin_psi:.1f} PSI."
                )

            if minimum_viable:
                engineering_reasoning.append(
                    "This is the minimum viable pipe upgrade that satisfies both pressure and velocity targets."
                )

            if diminishing_returns:
                engineering_reasoning.append(
                    "Larger pipe sizes may provide diminishing returns beyond this point."
                )

            if pipe.wall_type == current_pipe.wall_type:
                engineering_reasoning.append(
                    f"Preserves current wall type: {pipe.wall_type}."
                )

            if pipe.material == current_pipe.material:
                engineering_reasoning.append(
                    f"Preserves current material: {pipe.material}."
                )

            if pipe_cost_delta <= 0:
                engineering_reasoning.append(
                    "No added pipe unit-cost penalty compared with current pipe."
                )
            else:
                engineering_reasoning.append(
                    f"Adds approximately ${pipe_cost_delta:.2f}/ft compared with current pipe."
                )

            value_score = 0
            value_score += margin_gain * 2
            value_score += velocity_reduction * 10

            if trial_passed and not baseline_summary["passed"]:
                value_score += 100

            if pressure_ok:
                value_score += 30

            if velocity_ok:
                value_score += 50

            if minimum_viable:
                value_score += 100

            if diminishing_returns:
                value_score += 10

            value_score -= pipe_cost_delta * 2
            value_score -= oversize_penalty

            if margin_gain > 1 or velocity_reduction > 0.5 or trial_passed != baseline_summary["passed"]:
                trials.append({
                    "type": "single_branch_pipe_upgrade",
                    "branch_number": branch_number,
                    "current_pipe": current_pipe_name,
                    "recommended_pipe": pipe.name,
                    "baseline_margin_psi": baseline_margin,
                    "trial_margin_psi": trial_summary["pressure_margin_psi"],
                    "margin_gain_psi": margin_gain,
                    "baseline_velocity_fps": baseline_velocity,
                    "trial_velocity_fps": trial_summary["velocity_fps"],
                    "velocity_reduction_fps": velocity_reduction,
                    "baseline_passed": baseline_summary["passed"],
                    "trial_passed": trial_passed,
                    "pressure_ok": pressure_ok,
                    "velocity_ok": velocity_ok,
                    "minimum_viable": minimum_viable,
                    "diminishing_returns": diminishing_returns,
                    "oversize_penalty": oversize_penalty,
                    "pipe_cost_delta_per_ft": pipe_cost_delta,
                    "value_score": value_score,
                    "engineering_reasoning": engineering_reasoning,
                    "score": score_manifold(trial_manifold),
                    "recommendation": f"Upgrade Branch {branch_number} from {current_pipe_name} to {pipe.name}."
                })

    trials = sorted(
        trials,
        key=lambda item: (
            item["minimum_viable"],
            item["velocity_ok"],
            item["pressure_ok"],
            item["value_score"],
            item["trial_passed"],
            item["score"]
        ),
        reverse=True
    )

    return trials


def test_staged_port_reductions(input_data, library, pump):
    trials = []

    if not pump:
        return trials

    current_max_ports = int(input_data.get("max_simultaneous_ports", 1))

    if current_max_ports <= 1:
        return trials

    for proposed_ports in range(current_max_ports - 1, 0, -1):
        manifold = run_manifold(
            input_data,
            library,
            pump,
            max_ports_override=proposed_ports
        )

        trials.append({
            "type": "staged_port_reduction",
            "current_max_ports": current_max_ports,
            "recommended_max_ports": proposed_ports,
            "passed": manifold.get("passed", False),
            "last_line_passed": manifold.get("operating_modes", {}).get("last_line_passed", False),
            "total_flow_gpm": manifold.get("total_flow_gpm", 0),
            "score": score_manifold(manifold),
            "recommendation": f"Test staging the system at {proposed_ports} simultaneous manifold port(s)."
        })

    trials = sorted(
        trials,
        key=lambda item: (
            item["passed"],
            item["last_line_passed"],
            item["score"]
        ),
        reverse=True
    )

    return trials


def build_all_pipe_upgrade_trial(input_data, library, pump, baseline_manifold):
    if not pump:
        return None

    baseline_branches = input_data.get("branches", [])
    trial_branches = copy.deepcopy(baseline_branches)
    changes = []

    for branch in trial_branches:
        if not branch.get("active"):
            continue

        branch_number = branch.get("branch_number")
        current_pipe_name = branch.get("pipe_name")
        larger_pipes = get_larger_pipes(library, current_pipe_name)

        baseline_branch_result = get_branch_result(baseline_manifold, branch_number)
        baseline_summary = summarize_branch(baseline_branch_result)

        if not larger_pipes:
            continue

        current_velocity = baseline_summary["velocity_fps"]
        current_margin = baseline_summary["pressure_margin_psi"]

        if current_velocity <= 8 and current_margin >= 10:
            continue

        chosen_pipe = larger_pipes[0]
        branch["pipe_name"] = chosen_pipe.name

        changes.append({
            "branch_number": branch_number,
            "current_pipe": current_pipe_name,
            "recommended_pipe": chosen_pipe.name
        })

    if not changes:
        return None

    trial_manifold = run_manifold(
        input_data,
        library,
        pump,
        branches_override=trial_branches
    )

    return {
        "type": "combined_pipe_upgrade",
        "changes": changes,
        "passed": trial_manifold.get("passed", False),
        "last_line_passed": trial_manifold.get("operating_modes", {}).get("last_line_passed", False),
        "score": score_manifold(trial_manifold),
        "recommendation": "Upgrade all branches with high velocity or thin pressure margin by one pipe size and re-test.",
        "trial_total_flow_gpm": trial_manifold.get("total_flow_gpm", 0),
        "trial_failing_branch_count": trial_manifold.get("failing_branch_count", 0)
    }


def identify_governing_branch(manifold):
    worst = manifold.get("worst_branch")

    if not worst:
        return None

    return {
        "branch_number": worst.get("branch_number"),
        "role": worst.get("role"),
        "pipe_name": worst.get("pipe_name"),
        "pressure_margin_psi": worst.get("pressure_margin_psi"),
        "final_pressure_psi": worst.get("final_pressure_psi"),
        "required_terminal_pressure_psi": worst.get("required_terminal_pressure_psi"),
        "recommendation": "Treat this as the current governing branch. Improve this branch first before optimizing lower-priority branches."
    }


def optimize_hydraulic_design(input_data, library, pump, baseline_manifold):
    if not pump or not baseline_manifold:
        return {
            "status": "Not Available",
            "summary": "Optimizer could not run because no valid pump or manifold result was available.",
            "governing_branch": None,
            "pipe_upgrade_trials": [],
            "staged_port_trials": [],
            "combined_pipe_upgrade_trial": None,
            "best_actions": []
        }

    pipe_upgrade_trials = test_single_branch_pipe_upgrades(
        input_data,
        library,
        pump,
        baseline_manifold
    )

    staged_port_trials = test_staged_port_reductions(
        input_data,
        library,
        pump
    )

    combined_pipe_upgrade_trial = build_all_pipe_upgrade_trial(
        input_data,
        library,
        pump,
        baseline_manifold
    )

    governing_branch = identify_governing_branch(baseline_manifold)

    best_actions = []

    if governing_branch:
        best_actions.append({
            "priority": 1,
            "action": "Fix governing branch first",
            "details": governing_branch["recommendation"]
        })

    if pipe_upgrade_trials:
        best = pipe_upgrade_trials[0]
        best_actions.append({
            "priority": 2,
            "action": "Best pipe upgrade trial",
            "details": best["recommendation"]
        })

    if staged_port_trials:
        best_stage = staged_port_trials[0]
        best_actions.append({
            "priority": 3,
            "action": "Best staging trial",
            "details": best_stage["recommendation"]
        })

    if combined_pipe_upgrade_trial:
        best_actions.append({
            "priority": 4,
            "action": "Combined pipe upgrade trial",
            "details": combined_pipe_upgrade_trial["recommendation"]
        })

    if not best_actions:
        best_actions.append({
            "priority": 1,
            "action": "No obvious hydraulic optimization found",
            "details": "The current layout does not show a simple pipe-upsize or staging improvement. Next optimization should evaluate branch topology and device distribution."
        })

    return {
        "status": "Complete",
        "summary": "Optimizer tested pipe upsizing and staging alternatives against the current design.",
        "governing_branch": governing_branch,
        "pipe_upgrade_trials": pipe_upgrade_trials[:10],
        "staged_port_trials": staged_port_trials[:10],
        "combined_pipe_upgrade_trial": combined_pipe_upgrade_trial,
        "best_actions": best_actions
    }