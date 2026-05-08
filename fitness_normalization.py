def normalize_score(
    value,
    ideal,
    tolerance,
    max_score=100
):
    """
    Returns proportional score based on
    distance from ideal target.
    """

    deviation = abs(value - ideal)

    if deviation >= tolerance:
        return 0

    ratio = 1 - (deviation / tolerance)

    return round(
        ratio * max_score,
        2
    )


def inverse_normalize_score(
    value,
    max_acceptable,
    max_score=100
):
    """
    Lower values are better.
    Example:
    velocity
    friction loss
    """

    if value >= max_acceptable:
        return 0

    ratio = 1 - (value / max_acceptable)

    return round(
        ratio * max_score,
        2
    )
