from weighted_score import (
    calculate_weighted_design_score
)

from adaptive_mutation_engine import (
    run_adaptive_mutation
)

from candidate_constraints import (
    evaluate_candidate_constraints
)


def evaluate_mutation(candidate):
    primary_before = (
        candidate.get("primary", {}) or {}
    )

    before = calculate_weighted_design_score(
        primary_before
    )

    mutated = run_adaptive_mutation(
        candidate
    )

    constraint_result = evaluate_candidate_constraints(
        mutated
    )

    primary_after = (
        mutated.get("primary", {}) or {}
    )

    if not constraint_result.get("passed"):
        after = {
            "overall_score": 0,
            "constraint_result": constraint_result
        }
    else:
        after = calculate_weighted_design_score(
            primary_after
        )
        after["constraint_result"] = constraint_result

    before_score = before["overall_score"]
    after_score = after["overall_score"]

    improvement = round(
        after_score - before_score,
        2
    )

    return {
        "original_score": before_score,
        "mutated_score": after_score,
        "improvement": improvement,
        "improved": improvement > 0,
        "constraint_result": after.get("constraint_result", {}),
        "candidate": mutated
    }
