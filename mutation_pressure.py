def get_mutation_scale(
    generation,
    stagnant_generations
):
    """
    Dynamic mutation scaling.

    More stagnation =
    more aggressive mutation.
    """

    base_scale = 1.0

    # gradual decay over time
    generation_factor = max(
        0.6,
        1.0 - (generation * 0.02)
    )

    # stagnation escape pressure
    stagnation_boost = (
        stagnant_generations * 0.15
    )

    scale = (
        base_scale
        * generation_factor
        + stagnation_boost
    )

    scale = min(3.0, scale)

    return round(scale, 2)
