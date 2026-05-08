SURVIVOR_POOL = []


def store_survivor(result):
    if result.get("improved"):
        SURVIVOR_POOL.append(
            result["candidate"]
        )

    return len(SURVIVOR_POOL)


def get_survivors():
    return SURVIVOR_POOL
