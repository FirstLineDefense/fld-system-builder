from optimization_constraints import evaluate_constraints


def candidate_passes_constraints(candidate):
    constraints = evaluate_constraints(candidate)

    if not constraints:
        return True

    for constraint in constraints:
        if not constraint.get("passed", False):
            return False

    return True


def filter_valid_candidates(candidates):
    valid = []
    rejected = []

    for candidate in candidates:
        if candidate_passes_constraints(candidate):
            valid.append(candidate)
        else:
            rejected.append(candidate)

    return {
        "valid": valid,
        "rejected": rejected
    }


def summarize_candidate_filtering(candidates):
    result = filter_valid_candidates(candidates)

    valid_count = len(result["valid"])
    rejected_count = len(result["rejected"])

    return [{
        "type": "candidate_filtering",
        "label": "Constraint filtering",
        "message": (
            f"{valid_count} valid candidates, "
            f"{rejected_count} rejected candidates."
        ),
        "confidence": "high",
        "icon": "🧪",
        "reason": (
            "Candidates failing runtime or architecture "
            "constraints are automatically removed from "
            "optimizer evolution cycles."
        )
    }]
