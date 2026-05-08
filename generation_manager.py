import random

from survivor_memory import (
    get_survivors
)


def seed_candidate(base_candidate):
    survivors = get_survivors()

    if not survivors:
        return base_candidate

    return random.choice(survivors)
