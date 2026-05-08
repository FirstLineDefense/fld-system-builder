from weighted_score import (
    calculate_weighted_design_score,
)


def get_design_score(
    primary
):
    result = calculate_weighted_design_score(
        primary
    )

    if not isinstance(
        result,
        dict
    ):
        return {
            "overall_score": 0
        }

    return result
