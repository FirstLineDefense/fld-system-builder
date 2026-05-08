CURRENT_MUTATION_SCALE = 1.0


def set_mutation_scale(scale):
    global CURRENT_MUTATION_SCALE

    CURRENT_MUTATION_SCALE = max(
        0.25,
        min(
            3.0,
            float(scale)
        )
    )


def get_current_mutation_scale():
    return CURRENT_MUTATION_SCALE
