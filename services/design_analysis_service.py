from domain.design_validation import (
    validate_primary,
)

from engines.constraint_violation_engine import (
    detect_constraint_violations,
)

from services.scoring_service import (
    get_design_score,
)

from services.auto_apply_service import (
    get_auto_apply_result,
)


def analyze_design(primary):
    validation_errors = validate_primary(
        primary
    )

    if validation_errors:
        return {
            "validation_errors": validation_errors,
            "violations": [],
            "score": {
                "overall_score": 0
            },
            "auto_apply": {},
        }

    violations = detect_constraint_violations(
        primary
    )

    score = get_design_score(
        primary
    )

    auto_apply = get_auto_apply_result(
        primary
    )

    return {
        "violations": violations,
        "score": score,
        "auto_apply": auto_apply,
    }
