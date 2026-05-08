from domain.design_state import (
    clone_primary,
)

from engines.constraint_violation_engine import (
    detect_constraint_violations,
)

from hydraulic_recalculation import (
    recalculate_candidate_hydraulics,
)

from engines.scoring_engine import (
    get_design_score,
)


PIPE_STEPS = [
    0.5,
    1.0,
    1.5,
    2.0,
    2.5,
    3.0,
    3.5,
    4.0,
]


def _next_pipe_size(current_size):
    for pipe_size in PIPE_STEPS:
        if pipe_size > current_size:
            return pipe_size

    return current_size


def auto_apply_safe_fixes(primary):
    original_primary = clone_primary(primary)
    candidate_primary = clone_primary(primary)

    changes = []

    violations = detect_constraint_violations(
        candidate_primary
    )

    branches = candidate_primary.get("branches", []) or []
    pump = candidate_primary.get("pump", {}) or {}
    motor = candidate_primary.get("motor", {}) or {}

    total_branch_gpm = sum(
        branch.get("target_gpm", 0) or 0
        for branch in branches
    )

    for violation in violations:
        constraint = violation.get("constraint", "")

        if constraint in [
            "excessive_velocity",
            "elevated_velocity",
        ]:
            for branch in branches:
                velocity = branch.get("velocity_fps", 0) or 0

                if velocity > 7:
                    current_size = branch.get("pipe_diameter_in", 1.0) or 1.0
                    new_size = _next_pipe_size(current_size)

                    if new_size != current_size:
                        branch["pipe_diameter_in"] = new_size
                        changes.append(
                            f"Branch {branch.get('branch_number', 'unknown')} pipe increased from {current_size} in to {new_size} in"
                        )

        elif constraint == "pump_capacity":
            if total_branch_gpm:
                current_gpm = pump.get("gpm", 0) or 0
                new_gpm = round(total_branch_gpm * 1.15, 1)

                if new_gpm > current_gpm:
                    pump["gpm"] = new_gpm
                    changes.append(
                        f"Pump capacity increased from {current_gpm} GPM to {new_gpm} GPM"
                    )

        elif constraint == "motor_power":
            current_hp = motor.get("hp", 0) or 0
            pump_gpm = pump.get("gpm", 0) or 0

            recommended_hp = round(
                max(
                    3 * max(pump_gpm / 100, 1),
                    5
                ),
                1
            )

            if recommended_hp > current_hp:
                motor["hp"] = recommended_hp
                changes.append(
                    f"Motor increased from {current_hp} HP to {recommended_hp} HP"
                )

    candidate_primary["branches"] = branches
    candidate_primary["pump"] = pump
    candidate_primary["motor"] = motor

    candidate = {
        "primary": candidate_primary
    }

    candidate = recalculate_candidate_hydraulics(
        candidate
    )

    candidate_primary = candidate["primary"]

    original_score = get_design_score(
        original_primary
    ).get("overall_score", 0)

    auto_applied_score = get_design_score(
        candidate_primary
    ).get("overall_score", 0)

    improvement = round(
        auto_applied_score - original_score,
        2
    )

    if improvement > 0:
        status = "auto-applied candidate improved the design"
    elif improvement == 0:
        status = "auto-applied candidate matched the design"
    else:
        status = "auto-applied candidate did not improve the design"

    return {
        "status": status,
        "original_score": original_score,
        "auto_applied_score": auto_applied_score,
        "improvement": improvement,
        "changes": changes,
        "original_primary": original_primary,
        "auto_applied_primary": candidate_primary,
    }
