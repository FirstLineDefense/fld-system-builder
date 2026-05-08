import random


def random_multiplier(
    minimum=0.90,
    maximum=1.15
):
    return round(
        random.uniform(minimum, maximum),
        3
    )


def random_step(
    choices
):
    return random.choice(choices)
