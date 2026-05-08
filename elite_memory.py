ELITE = None
ELITE_SCORE = -1


def update_elite(result):
    global ELITE
    global ELITE_SCORE

    score = result.get(
        "mutated_score",
        0
    )

    if score > ELITE_SCORE:
        ELITE_SCORE = score
        ELITE = result["candidate"]

    return {
        "elite_score": ELITE_SCORE,
        "elite": ELITE
    }


def get_elite():
    return {
        "elite_score": ELITE_SCORE,
        "elite": ELITE
    }
