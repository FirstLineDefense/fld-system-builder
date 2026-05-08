from targeted_mutation import (
    apply_targeted_mutation
)

from branch_mutation import (
    mutate_branch_hydraulics
)

from component_targets import (
    identify_weak_components
)

from hydraulic_recalculation import (
    recalculate_candidate_hydraulics
)

from exploratory_mutation import (
    maybe_apply_exploratory_mutation
)


def run_adaptive_mutation(candidate):
    weak = identify_weak_components(
        candidate
    )

    mutated = candidate

    if "branch_diameter" in weak:
        mutated = mutate_branch_hydraulics(
            mutated
        )

    before_primary = (
        mutated.get("primary", {})
        or {}
    )

    before_branches = (
        before_primary.get("branches", [])
        or []
    )

    before_branch = (
        before_branches[0]
        if before_branches
        else {}
    )

    before_velocity = before_branch.get(
        "velocity_fps"
    )

    before_gpm = before_branch.get(
        "target_gpm"
    )

    mutated = apply_targeted_mutation(
        mutated
    )

    mutated = recalculate_candidate_hydraulics(
        mutated
    )

    after_primary = (
        mutated.get("primary", {})
        or {}
    )

    after_branches = (
        after_primary.get("branches", [])
        or []
    )

    after_branch = (
        after_branches[0]
        if after_branches
        else {}
    )

    after_velocity = after_branch.get(
        "velocity_fps"
    )

    after_gpm = after_branch.get(
        "target_gpm"
    )

    print()
    print("=== MUTATION DEBUG ===")
    print("Before Velocity:", before_velocity)
    print("After Velocity:", after_velocity)
    print("Before GPM:", before_gpm)
    print("After GPM:", after_gpm)

    mutated = maybe_apply_exploratory_mutation(
        mutated
    )

    mutated["adaptive_targets"] = weak

    return mutated
