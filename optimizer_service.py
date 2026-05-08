from evolutionary_runtime import (
    run_evolution
)

from convergence_report import (
    summarize_evolution
)

from optimizer_candidate_adapter import (
    build_optimizer_candidate_from_input,
)

from weighted_score import (
    calculate_weighted_design_score,
)


def build_default_candidate():
    return {
        "primary": {
            "pump": {"gpm": 300},
            "motor": {"hp": 10},
            "runtime_minutes": 120,
            "water_gallons": 5000,
            "branches": [
                {
                    "target_gpm": 120,
                    "velocity_fps": 9,
                    "pipe_diameter_in": 1.0
                }
            ]
        }
    }


def run_optimizer_service(
    candidate=None,
    input_data=None,
    generations=20,
    population_size=20
):
    if candidate is None and input_data is not None:
        candidate = build_optimizer_candidate_from_input(
            input_data
        )

    if candidate is None:
        candidate = build_default_candidate()

    original_primary = candidate.get("primary", {})
    original_score = calculate_weighted_design_score(
        original_primary
    ).get("overall_score", 0)

    history = run_evolution(
        candidate,
        generations=generations,
        population_size=population_size
    )

    summary = summarize_evolution(
        history
    )

    true_improvement = round(
        summary.get("best_score", 0) - original_score,
        2
    )

    summary["original_input_score"] = original_score
    summary["true_total_improvement"] = true_improvement

    if true_improvement > 0:
        summary["optimizer_status"] = "optimizer improved the original input"
        summary["recommended_candidate_source"] = "evolved_candidate"
    else:
        original_branches = original_primary.get("branches", []) or []
        original_branch = original_branches[0] if original_branches else {}

        summary["optimizer_status"] = "original input remains best candidate"
        summary["recommended_candidate_source"] = "original_input"
        summary["starting_score"] = original_score
        summary["final_score"] = original_score
        summary["best_score"] = original_score
        summary["total_improvement"] = 0
        summary["true_total_improvement"] = 0
        summary["best_pump"] = original_primary.get("pump", {})
        summary["best_motor"] = original_primary.get("motor", {})
        summary["best_branch"] = original_branch
        summary["best_candidate_summary"] = {
            "pump_name": original_primary.get("pump", {}).get("name", "Original input pump"),
            "pump_gpm": original_primary.get("pump", {}).get("gpm"),
            "motor_name": original_primary.get("motor", {}).get("name", "Original input motor"),
            "motor_hp": original_primary.get("motor", {}).get("hp"),
            "branch_count": len(original_branches),
            "total_branch_gpm": sum(
                branch.get("target_gpm", 0) or 0
                for branch in original_branches
            ),
            "max_velocity_fps": max(
                [
                    branch.get("velocity_fps", 0) or 0
                    for branch in original_branches
                ],
                default=0
            ),
            "min_pressure_psi": None
        }

    return {
        "history": history,
        "summary": summary
    }
