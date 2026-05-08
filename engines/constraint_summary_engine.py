from engines.constraint_violation_service import (
    summarize_constraint_violations,
)


def build_constraint_summary(
    violations
):
    summary = summarize_constraint_violations(
        violations
    )

    return {
        "count": summary.get(
            "count",
            0
        ),
        "families": summary.get(
            "families",
            {}
        ),
        "violations": summary.get(
            "violations",
            []
        ),
    }
